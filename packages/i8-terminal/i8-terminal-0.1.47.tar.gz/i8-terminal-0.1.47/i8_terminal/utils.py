import codecs
import os
from typing import Any

from i8_terminal.config import USER_SETTINGS


def read(rel_path: str) -> str:
    """
    Read a file.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version() -> Any:
    """
    Read version from a file.
    """
    for line in read("version.txt").splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def is_user_logged_in() -> bool:
    if not USER_SETTINGS.get("i8_core_api_key") or not USER_SETTINGS.get("i8_core_token"):
        return False
    return True
