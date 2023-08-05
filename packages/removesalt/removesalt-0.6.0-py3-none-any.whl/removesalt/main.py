import logging
import pathlib

import hydra
import omegaconf
from omegaconf import OmegaConf

import removesalt.apps.iris.iris as iris
import removesalt.apps.mediaplayer.mediaplayer as mediaplayer
import removesalt.apps.spectra.spectra as spectra
from removesalt import build_guideline

OmegaConf.register_new_resolver("lower", lambda x: str(x).lower())
OmegaConf.register_new_resolver("path", pathlib.Path)
OmegaConf.register_new_resolver(
    "orig_cwd", lambda: pathlib.Path(hydra.utils.get_original_cwd())
)

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"


log = logging.getLogger(__name__)


# Auxiliary function
def client_call(
    build_guideline: build_guideline.BuildGuideline, cfg: omegaconf.DictConfig
):
    build_guideline.build(cfg)


@hydra.main(config_path="conf", config_name="config")
def my_app(cfg: omegaconf.DictConfig) -> None:
    log.info("Starting script...")

    for key in logging.Logger.manager.loggerDict:
        print(key)

    if cfg.app.installer_name == "spectra":
        client_call(spectra.Spectra(), cfg)
    if cfg.app.installer_name == "iris":
        client_call(iris.Iris(), cfg)
    if cfg.app.installer_name == "mediaplayer":
        client_call(mediaplayer.Mediaplayer(), cfg)

    log.info("Script ends here")


if __name__ == "__main__":
    my_app()
