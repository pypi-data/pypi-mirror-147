import inspect
import logging
import platform
import shlex
import shutil
import subprocess
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import omegaconf
from giftmaster import signtool

import removesalt.sign
from removesalt import bundle, s3, template

log = logging.getLogger(__name__)


@dataclass
class ShellCommand:
    name: str
    command: List[str]
    cfg: omegaconf.DictConfig


def run(cmdobj):
    log.debug(cmdobj.name)
    log.debug(shlex.join(cmdobj.command))

    if cmdobj.cfg.app.wix.dry_run:
        return

    if platform.system() != "Windows":
        return

    proc = subprocess.Popen(
        cmdobj.command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, err = proc.communicate()
    return_code = proc.poll()
    out = out.decode(sys.stdin.encoding)
    err = err.decode(sys.stdin.encoding)
    log.debug(out)
    log.debug(f"{proc.returncode=}")

    ex = subprocess.CalledProcessError(
        return_code, cmd=shlex.join(cmdobj.command), output=out
    )
    ex.stdout, ex.stderr = out, err

    """
    error LGHT0204 : ICE57: Component 'IrisControlPanelShortcutComponent'
    has both per-user data and a keypath that can be either per-user or
    per-machine.
    204
    """

    if proc.returncode not in [0, 204]:
        raise ex


class BuildGuideline(ABC):
    def build(self, cfg: omegaconf.DictConfig):
        self.report_s3_endpoints(cfg)
        self.setup_common(cfg)
        self.gather_binaries(cfg)
        if cfg.app.run_signtool:
            self.sign(cfg)
        self.fill_templates(cfg)
        self.wix_heat(cfg)  # create .wxs from heat dir harvest
        self.wix_candle(cfg)  # create .wixobj from .wxs
        self.wix_light(cfg)  # create .msi from .wixobj
        if cfg.app.run_signtool:
            self.sign(cfg)
        self.wix_bundle(cfg)  # create bundle .exe from .msi
        self.wix_light2(cfg)  # output bundle.exe
        if cfg.app.run_signtool:
            self.sign(cfg)
            self.wix_unsign_bundle(cfg)
            self.wix_insignia_deatch(cfg)
            self.sign(cfg)
            self.wix_insignia_reattach(cfg)
            self.sign(cfg)
        self.create_zips(cfg)
        self.layout_s3(cfg)
        # self.s3sync(cfg)

    def report_s3_endpoints(self, cfg: omegaconf.DictConfig):
        if not cfg.app.stop_all_uploads:
            logging.debug(cfg.app.artifacts.url.versioned)

        if cfg.app.release:
            logging.debug(cfg.app.artifacts.url.latest)

    def setup_common(self, cfg: omegaconf.DictConfig):
        cfg.app.deploy.mkdir(parents=True, exist_ok=True)
        cfg.app.work1.mkdir(parents=True, exist_ok=True)

        shutil.copy(cfg.app.icon.path_source, cfg.app.icon.path_work)
        shutil.copy(cfg.app.splash_image.path_source, cfg.app.splash_image.path_work)

    @abstractmethod
    def gather_binaries(self, cfg: omegaconf.DictConfig):
        pass

    @abstractmethod
    def layout_s3(self, cfg: omegaconf.DictConfig):
        pass

    def fill_templates(self, cfg: omegaconf.DictConfig):
        template.main(cfg)

    def wix_heat(self, cfg: omegaconf.DictConfig) -> None:
        for name in cfg.app.components.build_order:
            component = cfg.app.components.container[name]

            if not component.single_file:
                cmd = [
                    "heat",
                    "dir",
                    str(component.deploy),
                    "-out",
                    str(component.path_work),
                    "-cg",
                    component.group,
                    "-dr",
                    component.root_dir,
                    "-var",
                    "var.SourceFilesDir",
                    "-ag",
                    "-g1",
                    "-srd",
                    "-suid",
                    "-sreg",
                    "-arch",
                    "x64",
                    "-nologo",
                ]

                fcn_name = inspect.currentframe().f_code.co_name
                sc = ShellCommand(fcn_name, cmd, cfg)
                run(sc)

    def wix_candle(self, cfg: omegaconf.DictConfig) -> None:
        for name in cfg.app.components.build_order:
            component = cfg.app.components.container[name]

            cmd = [
                "candle",
                "-out",
                str(component.path_work.with_suffix(".wixobj")),
                str(component.path_work),
            ]

            if cfg.app.sku:
                cmd.extend(
                    [
                        f"-dMySku={str(cfg.app.sku)}",
                    ]
                )

            cmd.extend(
                [
                    f"-dSourceFilesDir={str(component.deploy)}",
                ]
            )

            cmd.extend(
                [
                    "-ext",
                    "WixUtilExtension",
                    "-arch",
                    "x64",
                    "-nologo",
                ]
            )

            fcn_name = inspect.currentframe().f_code.co_name
            sc = ShellCommand(fcn_name, cmd, cfg)
            run(sc)

    def wix_light(self, cfg: omegaconf.DictConfig) -> None:
        wixobj_paths = []
        for name in cfg.app.components.build_order:
            component = cfg.app.components.container[name]
            path = component.path_work.with_suffix(".wixobj")
            wixobj_paths.append(str(path))

        cmd = [
            "light",
            "-out",
            str(cfg.app.msi.path_work),
            *wixobj_paths,
            "-ext",
            "WixUtilExtension",
            "-ext",
            "WixUIExtension",
            "-spdb",
            "-nologo",
        ]

        fcn_name = inspect.currentframe().f_code.co_name
        sc = ShellCommand(fcn_name, cmd, cfg)
        run(sc)

    def wix_bundle(self, cfg: omegaconf.DictConfig) -> None:
        cmd = [
            "candle",
            "-out",
            str(cfg.app.bundle.wix_source.work.with_suffix(".wixobj")),
            str(cfg.app.bundle.wix_source.work),
            f"-dMsiPath={str(cfg.app.msi.path_work)}",
            f"-dThemeFile={str(cfg.app.theme_file.path_work)}",
            f"-dLocalizationFile={str(cfg.app.localization_file.path_work)}",
            "-ext",
            "WixBalExtension",
            "-ext",
            "WixUtilExtension",
            "-arch",
            "x64",
            "-nologo",
        ]

        fcn_name = inspect.currentframe().f_code.co_name
        sc = ShellCommand(fcn_name, cmd, cfg)
        run(sc)

    def wix_light2(self, cfg: omegaconf.DictConfig) -> None:
        cmd = [
            "light",
            "-out",
            str(cfg.app.bundle.bin),
            str(cfg.app.bundle.wix_source.work.with_suffix(".wixobj")),
            f"-dMsiPath={str(cfg.app.msi.path_work)}",
            f"-dThemeFile={str(cfg.app.theme_file.path_work)}",
            f"-dLocalizationFile={str(cfg.app.localization_file.path_work)}",
            "-ext",
            "WixBalExtension",
            "-spdb",
            "-nologo",
        ]

        fcn_name = inspect.currentframe().f_code.co_name
        sc = ShellCommand(fcn_name, cmd, cfg)
        run(sc)

    def wix_insignia_deatch(self, cfg: omegaconf.DictConfig) -> None:
        cmd = [
            "insignia",
            "-ib",
            str(cfg.app.bundle.bin),
            "-o",
            str(cfg.app.engine),
        ]

        fcn_name = inspect.currentframe().f_code.co_name
        sc = ShellCommand(fcn_name, cmd, cfg)
        run(sc)

    def wix_insignia_reattach(self, cfg: omegaconf.DictConfig) -> None:
        cmd = [
            "insignia",
            "-ab",
            str(cfg.app.engine),
            str(cfg.app.bundle.bin),
            "-o",
            str(cfg.app.bundle.bin),
        ]

        fcn_name = inspect.currentframe().f_code.co_name
        sc = ShellCommand(fcn_name, cmd, cfg)
        run(sc)

    def sign(self, cfg: omegaconf.DictConfig) -> None:
        removesalt.sign.sign_files(cfg.app.work1.parent)

    def wix_unsign_bundle(self, cfg: omegaconf.DictConfig) -> None:
        # signtool remove /s bundle.exe
        cmd = signtool.unsign_cmd(cfg.app.bundle.bin)
        fcn_name = inspect.currentframe().f_code.co_name
        sc = ShellCommand(fcn_name, cmd, cfg)
        run(sc)

    def hook1(self) -> None:
        pass

    def hook2(self) -> None:
        pass

    def create_zips(self, cfg: omegaconf.DictConfig):
        bundle.main(cfg)

    def s3sync(self, cfg: omegaconf.DictConfig):
        s3.main(cfg)
