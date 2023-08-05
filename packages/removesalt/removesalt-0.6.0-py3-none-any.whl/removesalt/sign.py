import logging
from pathlib import Path
from typing import List

import giftmaster.skeleton


def myfun(x, check):
    for item in check:
        z = str(Path(item)).lower()
        if z in str(x):
            return True
    return False


def get_files_to_sign(*roots: List[str]) -> List[str]:
    paths = set()
    for root_path in roots:
        for path in list(Path(root_path).rglob("*")):
            paths.add(path)

    # filter on only file types and substrings in paths
    dirs = set(filter(lambda _str: Path(_str).is_dir(), paths))
    symlinks = set(filter(lambda _str: Path(_str).is_symlink(), paths))
    paths_filtered = paths - dirs - symlinks

    ignore = set()

    extensions_to_ignore = [
        ".bat",
        ".bmp",
        ".cfg",
        ".envrc",
        ".git",
        ".gitignore",
        ".go",
        ".ico",
        ".ini",
        ".log",
        ".md",
        ".mod",
        ".py",
        ".pyc",
        ".pdf",
        ".png",
        ".sum",
        ".tmpl",
        ".tox",
        ".txt",
        ".venv",
        ".wixobj",
        ".wxl",
        ".wxs",
        ".xml",
        ".yml",
        ".venv",
        ".zip",
    ]

    ignore |= set(filter(lambda x: myfun(x, extensions_to_ignore), paths_filtered))
    paths_filtered -= ignore
    logging.debug(paths_filtered)
    return list(paths_filtered)


def sign_files(*basedirs: List[Path]) -> None:
    paths_filtered = []
    for basedir in basedirs:
        paths_filtered += get_files_to_sign(basedir)

    file_list = list(paths_filtered)
    signtool_candidates = [r"C:\Program*\Windows Kits\*\bin\*\x64\signtool.exe"]
    batch_size = 10
    dry_run = None
    giftmaster.skeleton.client(file_list, signtool_candidates, batch_size, dry_run)
