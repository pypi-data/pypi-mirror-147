# flake8: noqa

import pathlib

import pytest

__author__ = "Taylor Monacelli"
__copyright__ = "Taylor Monacelli"
__license__ = "MPL-2.0"

directories = [
    r"C:\Program Files\Adobe\Common",
    r"C:\Program Files\Adobe\Common\Plug-ins",
    r"C:\Program Files\Adobe\Common\Plug-ins\7.0",
    r"C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore",
    r"C:\Program Files\Common Files\OFX\Plugins",
    r"C:\Program Files\Common Files\OFX\Plugins\SpectraPlugin.ofx.bundle",
    r"C:\Program Files\Common Files\OFX\Plugins\SpectraPlugin.ofx.bundle\Contents",
    r"C:\Program Files\Common Files\OFX\Plugins\SpectraPlugin.ofx.bundle\Contents\Resources",
    r"C:\Program Files\Common Files\OFX\Plugins\SpectraPlugin.ofx.bundle\Contents\Win64",
    r"C:\Program Files\Avid\AVX2_Plug-ins",
    r"C:\Program Files\Streambox\Spectra",
    r"C:\Program Files\Streambox\Spectra\dist",
    r"C:\ProgramData\Streambox\SpectraUI",
    r"C:\ProgramData\Streambox\SpectraUI\hash",
]

files = [
    r"C:\Program Files\Adobe\Common\Plug-ins\7.0\MediaCore\Spectra.prm",
    r"C:\Program Files\Common Files\OFX\Plugins\SpectraPlugin.ofx.bundle\Contents\Resources\com.Streambox.Spectra.png",
    r"C:\Program Files\Common Files\OFX\Plugins\SpectraPlugin.ofx.bundle\Contents\Win64\SpectraPlugin.ofx",
    r"C:\Program Files\Avid\AVX2_Plug-ins\Spectra.acf",
    r"C:\Program Files\Streambox\Spectra\control.ps1",
    r"C:\Program Files\Streambox\Spectra\control.psm1",
    r"C:\Program Files\Streambox\Spectra\disable-blackmagic.ps1",
    r"C:\Program Files\Streambox\Spectra\Encoder3.exe",
    r"C:\Program Files\Streambox\Spectra\Encoder5.exe",
    r"C:\Program Files\Streambox\Spectra\nssm.exe",
    r"C:\Program Files\Streambox\Spectra\Processing.NDI.Lib.x64.dll",
    r"C:\Program Files\Streambox\Spectra\sbxcmd.exe",
    r"C:\Program Files\Streambox\Spectra\service-error.log",
    r"C:\Program Files\Streambox\Spectra\service.log",
    r"C:\Program Files\Streambox\Spectra\dist\chromactivate.exe",
    r"C:\Program Files\Streambox\Spectra\dist\encassist.ini",
    r"C:\Program Files\Streambox\Spectra\dist\gdiplus.dll",
    r"C:\Program Files\Streambox\Spectra\dist\lib.zip",
    r"C:\Program Files\Streambox\Spectra\dist\msvcp71.dll",
    r"C:\Program Files\Streambox\Spectra\dist\MSVCR71.dll",
    r"C:\Program Files\Streambox\Spectra\dist\set_defaults.exe",
    r"C:\Program Files\Streambox\Spectra\dist\SpectraControlPanel.exe",
    r"C:\ProgramData\Streambox\SpectraUI\liveServers.xml",
    r"C:\ProgramData\Streambox\SpectraUI\settings.xml",
    r"C:\ProgramData\Streambox\SpectraUI\settings.xml.bak",
    r"C:\ProgramData\Streambox\SpectraUI\version.txt",
]


@pytest.mark.parametrize("path_str", files + directories)
def test_path_exists(path_str):
    assert pathlib.Path(path_str).exists()


@pytest.mark.parametrize("path_str", directories)
def test_path_exists(path_str):
    assert pathlib.Path(path_str).is_dir()


@pytest.mark.parametrize("path_str", files)
def test_paths_are_files(path_str):
    assert pathlib.Path(path_str).is_file()


@pytest.mark.parametrize("path_str", files)
def test_files_are_not_empty(path_str):
    path = pathlib.Path(path_str)
    if path.name not in ["service-error.log", "service.log"]:
        assert path.stat().st_size


@pytest.mark.parametrize("path_str", files)
def test_files_are_empty(path_str):
    path = pathlib.Path(path_str)
    if path.name in ["service-error.log", "service.log"]:
        assert path.stat().st_size == 0
