import os
import zipfile


def main(cfg):
    os.chdir(cfg.app.bundle.wix_source.work.parent)
    with zipfile.ZipFile(cfg.app.zip_versioned.path_work, mode="w") as zf:
        zf.write(cfg.app.bundle.name)

    with zipfile.ZipFile(cfg.app.zip_not_versioned.path_work, mode="w") as zf:
        zf.write(cfg.app.bundle.name)

    # cfg.app.zip_not_versioned.path_work
    name = "spectra_win.zip"
    with zipfile.ZipFile(name, mode="w") as zf:
        zf.write(cfg.app.bundle.name)

    os.chdir(cfg.app.orig_cwd)
