import argparse
import distutils.dir_util
import distutils.file_util
import logging
import shutil
import subprocess

import omegaconf
import saltgang
import saltgang.encassist
import saltgang.settings

from removesalt import build_guideline, template

log = logging.getLogger(__name__)


class Spectra(build_guideline.BuildGuideline):
    def gather_binaries(self, cfg: omegaconf.DictConfig):
        setup(cfg)

    def layout_s3(self, cfg: omegaconf.DictConfig):
        cfg.app.s3bucket.path_versioned.mkdir(exist_ok=True, parents=True)
        cfg.app.s3bucket.path_latest.mkdir(exist_ok=True, parents=True)

        shutil.copy(cfg.app.zip_versioned.path_work, cfg.app.s3bucket.path_versioned)
        shutil.copy(cfg.app.ver_file.path_deploy, cfg.app.s3bucket.path_versioned)
        shutil.copy(
            cfg.app.zip_not_versioned.path_work, cfg.app.s3bucket.path_versioned
        )

        guides = cfg.app.bin_path / "docs/s3"
        dst = cfg.app.s3bucket.path_latest
        distutils.dir_util.copy_tree(str(guides), str(dst))


def generate_encassist_ini(cfg):
    parser = argparse.ArgumentParser()
    saltgang.settings.add_arguments(parser)
    args = parser.parse_args(
        [
            "--outpath",
            str(cfg.app.spectra.encassist.ini.deploy),
            "--yaml-path",
            str(cfg.app.spectra.encassist.yml.work_path),
            "--ini",
        ]
    )
    saltgang.settings.main(args)


def generate_encassist_yml(cfg):
    parser = argparse.ArgumentParser()
    saltgang.encassist.add_arguments(parser)
    args = parser.parse_args(
        [
            "--outpath",
            str(cfg.app.spectra.encassist.yml.work_path),
            "--config-basedir",
            str(cfg.app.spectra.encassist.gitclone),
            "--sku",
            cfg.app.sku.lower(),
        ]
    )
    saltgang.encassist.main(args)


def generate_set_defaults_exe(cfg):
    parser = argparse.ArgumentParser()
    saltgang.settings.add_arguments(parser)
    args = parser.parse_args(
        [
            "--outpath",
            str(cfg.app.spectra.encassist.set_defaults.src_path),
            "--yaml-path",
            str(cfg.app.spectra.encassist.yml.work_path),
            "--go",
        ]
    )
    saltgang.settings.main(args)

    # build set_defaults.exe
    paths = [
        cfg.app.bin_path / "installer/set_defaults/go.mod",
        cfg.app.bin_path / "installer/set_defaults/go.sum",
    ]
    for path in paths:
        dst = cfg.app.work1 / path.name
        distutils.file_util.copy_file(str(path), str(dst))

    # go fmt
    proc = subprocess.run(
        f"go fmt {cfg.app.spectra.encassist.set_defaults.src_path}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    log.debug(proc.returncode)

    if proc.returncode == 0:
        log.debug(proc.returncode)
    else:
        log.debug(proc.stdout + proc.stderr)

    # go build
    proc = subprocess.run(
        "go build",
        shell=True,
        cwd=cfg.app.spectra.encassist.set_defaults.src_path.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    log.debug(proc.returncode)

    if proc.returncode == 0:
        log.debug(proc.returncode)
    else:
        log.debug(proc.stdout + proc.stderr)

    dst = cfg.app.spectra.encassist.set_defaults.deploy_path
    src = cfg.app.spectra.encassist.set_defaults.bin_path
    distutils.file_util.copy_file(str(src), str(dst))


def setup(cfg):
    # component: C:\Program Files\Avid\AVX2_Plug-ins\Spectra.acf
    src = cfg.app.bin_path / "avid"
    dst = cfg.app.deploy2
    distutils.dir_util.copy_tree(str(src), str(dst))

    # component: C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore\Spectra.prm
    src = cfg.app.bin_path / "adobe"
    dst = cfg.app.deploy3
    distutils.dir_util.copy_tree(str(src), str(dst))

    # component: C:\ProgramData\Streambox\SpectraUI
    src = cfg.app.bin_path / "spectraui"
    dst = cfg.app.deploy4
    distutils.dir_util.copy_tree(str(src), str(dst))
    cfg.app.ver_file.path_deploy.write_text(cfg.app.app.version)
    (cfg.app.ver_file.path_deploy.parent / "hash/.gitkeep").unlink(missing_ok=True)

    # component: C:\Program Files\Common Files\OFX\Plugins\SpectraPlugin.ofx.bundle\Contents\Win64\SpectraPlugin.ofx # noqa: E501
    src = cfg.app.bin_path / "ofx"
    dst = cfg.app.deploy5
    distutils.dir_util.copy_tree(str(src), str(dst))

    # component: C:\Program Files\Streambox\Spectra
    src = cfg.app.bin_path / "app"
    dst = cfg.app.deploy
    distutils.dir_util.copy_tree(str(src), str(dst))
    generate_encassist_yml(cfg)  # generate encassist.yml and then encassist.ini
    generate_encassist_ini(cfg)  # don't run until dist folder exists

    templates_path = template.get_templates_path(cfg)
    act = templates_path / "custom_actions.wxs"
    shutil.copy(act, cfg.app.components.container.actions.path_work)

    generate_encassist_yml(cfg)
    generate_set_defaults_exe(cfg)


def main(cfg):
    setup(cfg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)
