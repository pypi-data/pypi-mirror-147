from hydra import compose, initialize

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"


def test_with_initialize() -> None:
    with initialize(config_path="../src/removesalt/conf"):
        # config is relative to a module
        cfg = compose(
            config_name="config.yaml",
            overrides=[
                r"bin_path=C:\Users\Administrator\Downloads\streambox_iris-master"
            ],
        )
        assert (
            cfg.app.bin_path
            == r"C:\Users\Administrator\Downloads\streambox_iris-master"
        )
