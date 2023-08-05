import logging
import pathlib
import shutil

import jinja2
import omegaconf
import pkg_resources

log = logging.getLogger(__name__)


def get_templates_path(cfg: omegaconf.DictConfig):
    package = __name__.split(".")[0]
    TEMPLATES_PATH = pathlib.Path(
        pkg_resources.resource_filename(package, cfg.app.wix.templates_dir)
    )
    return TEMPLATES_PATH


def main(cfg):
    for thing in [
        cfg.app.app,
        cfg.app.bundle,
    ]:
        loader = jinja2.FileSystemLoader(searchpath=get_templates_path(cfg))
        env = jinja2.Environment(loader=loader, keep_trailing_newline=True)
        template = env.get_template(thing.wix_source.template.name)
        rendered = template.render(data=cfg.app)
        thing.wix_source.work.write_text(rendered)

    shutil.copy(
        get_templates_path(cfg) / ".." / cfg.app.theme_file.name,
        cfg.app.theme_file.path_work,
    )
    shutil.copy(
        get_templates_path(cfg) / ".." / cfg.app.localization_file.name,
        cfg.app.localization_file.path_work,
    )
