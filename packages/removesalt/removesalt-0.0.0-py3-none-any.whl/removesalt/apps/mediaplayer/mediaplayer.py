import argparse
import logging
import shutil

import omegaconf

from removesalt import build_guideline

log = logging.getLogger(__name__)


def setup(cfg):
    file_list = [
        "Microsoft.Expression.Interactions.dll",
        "Microsoft.Wpf.Interop.DirectX.dll",
        "Microsoft.Xaml.Behaviors.dll",
        "System.Windows.Interactivity.dll",
        "chroma2k35.bmp",
        "dxLib.dll",
    ]

    # choose 8bit or 10bit from cli: ...+app=mediaplayer app.sku=10bit
    file_list2 = cfg.app.skus[cfg.app.sku].source

    file_list.extend(file_list2)

    for relpath in file_list:
        src = cfg.app.bin_path / relpath
        dst = cfg.app.deploy / src.name
        log.debug(f"copying {src} to {dst}")
        shutil.copy(src, dst)

    cfg.app.ver_file.path_work.write_text(cfg.app.app.version)


def main(cfg):
    setup(cfg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)


class Mediaplayer(build_guideline.BuildGuideline):
    def gather_binaries(self, cfg: omegaconf.DictConfig):
        setup(cfg)

    def layout_s3(self, cfg: omegaconf.DictConfig):
        cfg.app.s3bucket.path_versioned.mkdir(exist_ok=True, parents=True)
        cfg.app.s3bucket.path_latest.mkdir(exist_ok=True, parents=True)

        shutil.copy(cfg.app.zip_versioned.path_work, cfg.app.s3bucket.path_versioned)
        shutil.copy(cfg.app.ver_file.path_work, cfg.app.s3bucket.path_versioned)
        shutil.copy(
            cfg.app.zip_not_versioned.path_work, cfg.app.s3bucket.path_versioned
        )

        if cfg.app.release:
            shutil.copy(
                cfg.app.zip_not_versioned.path_work, cfg.app.s3bucket.path_latest
            )
            shutil.copy(cfg.app.ver_file.path_work, cfg.app.s3bucket.path_latest)
