import argparse
import logging
import shutil

import omegaconf

from removesalt import build_guideline, template

log = logging.getLogger(__name__)


def setup(cfg):
    appdir = cfg.app.bin_path / "app"

    files = [
        appdir / x
        for x in [
            "controlpanel.exe",
            "encassist.ini",
            "chromactivate.exe",
            "sb-hd-bmp.bmp",
        ]
    ]
    for file in files:
        shutil.copy(file, cfg.app.deploy)

    src = appdir / "WinDecoder.exe"
    dst = cfg.app.deploy / "decoder.exe"
    shutil.copy(src, dst)

    files = [
        cfg.app.installer_source_path / x
        for x in [
            "nssm.exe",
            "service.ps1",
            "cleanlogs.ps1",
        ]
    ]
    for file in files:
        log.debug(f"copy {file.resolve()} to {cfg.app.deploy.resolve()}")
        shutil.copy(file, cfg.app.deploy)

    curl = cfg.app.deploy / "curl"
    curl.mkdir(exist_ok=True, parents=True)
    files = [
        appdir / "curl" / x
        for x in [
            "curl.exe",
            "libeay32.dll",
            "libssl32.dll",
            "msvcr90.dll",
        ]
    ]
    for file in files:
        shutil.copy(file, curl)

    cfg.app.ver_file.path_work.write_text(cfg.app.app.version)

    templates_path = template.get_templates_path(cfg)
    p1 = templates_path / "custom_actions.wxs"
    log.debug(cfg.app.components.container.actions)
    log.debug(type(cfg.app.components.container.actions))
    shutil.copy(p1, cfg.app.components.container.actions.path_work)


def main(cfg):
    setup(cfg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)


class Iris(build_guideline.BuildGuideline):
    def gather_binaries(self, cfg: omegaconf.DictConfig):
        setup(cfg)

    def layout_s3(self, cfg: omegaconf.DictConfig):
        cfg.app.s3bucket.path_versioned.mkdir(exist_ok=True, parents=True)
        cfg.app.s3bucket.path_latest.mkdir(exist_ok=True, parents=True)

        # s3/win/0.0.1/streambox_iris_win_0.0.1.zip
        # s3/win/0.0.1/verstion.txt
        # s3/win/0.0.1/streambox_iris_win.zip
        shutil.copy(cfg.app.zip_versioned.path_work, cfg.app.s3bucket.path_versioned)
        shutil.copy(cfg.app.ver_file.path_work, cfg.app.s3bucket.path_versioned)
        shutil.copy(
            cfg.app.zip_not_versioned.path_work, cfg.app.s3bucket.path_versioned
        )

        # s3/latest/win/streambox_iris_quickstart.pdf
        # s3/latest/win/streambox_iris_win.zip
        # s3/latest/win/version.txt
        shutil.copy(cfg.app.quickstart.path_source, cfg.app.s3bucket.path_latest)
        if cfg.app.release:
            shutil.copy(
                cfg.app.zip_not_versioned.path_work, cfg.app.s3bucket.path_latest
            )
            shutil.copy(cfg.app.ver_file.path_work, cfg.app.s3bucket.path_latest)
