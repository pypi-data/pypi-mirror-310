import logging
import sysconfig
import os
import re
import subprocess
import sys
import venv
from pathlib import Path
from tabnanny import check

from .const import DEFAULT_EMBEDME_PATH, get_embedme_package

logging.basicConfig(level=logging.INFO)

_LOGGER = logging.getLogger("embedmeio")


def find_executable(executable, path=DEFAULT_EMBEDME_PATH):
    bindir = "Scripts" if sys.platform == "win32" else "bin"
    executable = executable + ".exe" if sys.platform == "win32" else executable
    file = (path / bindir / executable)
    if file.exists() and os.access(file, os.X_OK):
        return str(file)
    return None

def check_venv():
    # First check for the presence of embedmeio. If present, we have a suitable environment to run

    try:
        from esphome.embedmeio import __version__ as embedme_version
        _LOGGER.debug("Found embedmeio version %s", embedme_version)
        return True
    except:
        pass

# Are we running in a venv?
    if sys.prefix != sys.base_prefix:
        # if esphome is installed, it's not the right one
        try:
            from esphome.const import __version__ as esphome_version
            _LOGGER.error(
                """EmbedMe should be run in a venv with the EmbedMe version of esphome installed.
                This venv (%s) has a different version of esphome (%s) installed", sys.prefix
                """, sys.prefix, esphome_version
            )
            return False
        except:
            pass
    return False


def ask(prompt):
    prompt = re.sub(r"\n +", "\n", prompt)
    response = input(prompt + " (y/n)? ").strip().lower()
    if response != "y" and response != "yes":
        return False
    return True


def get_env():
    env = os.environ.copy()
    env["PATH"] = f"{DEFAULT_EMBEDME_PATH}/bin:{os.environ['PATH']}"
    env["PYTHONPATH"] = str(DEFAULT_EMBEDME_PATH)
    env["PYTHONEXEPATH"] = str(sys.executable)
    env["VIRTUAL_ENV"] = str(DEFAULT_EMBEDME_PATH)
    return env





def activate_venv():
    import os

    if not DEFAULT_EMBEDME_PATH.exists() or not DEFAULT_EMBEDME_PATH.is_dir():
        return False
    py_executable = find_executable("python")
    if not py_executable:
        return False

    embedme_main = find_executable("embedmeio")
    if not embedme_main:
        return False

    _LOGGER.info("Activating EmbedMe venv in %s", DEFAULT_EMBEDME_PATH)
    env = get_env()
    os.environ.update(env)
    os.execv(py_executable, ["embedmeio", "-m", "embedmeio", *sys.argv[1:]])

def create_venv():
    if not ask(f"""
            EmbedMe requires a venv to run; a custom venv can be created in this folder:

            {DEFAULT_EMBEDME_PATH}.

            Do you want to create a venv in that location for future use"""):
        return False

    if DEFAULT_EMBEDME_PATH.exists():
        if not ask(
                f"""
            Folder {DEFAULT_EMBEDME_PATH} already exists, do you want to overwrite it"""
        ):
            return False
    builder = venv.EnvBuilder(
        with_pip=True,
        clear=True,
        symlinks=True,
    )
    builder.create(DEFAULT_EMBEDME_PATH)  # type: ignore
    _LOGGER.info("EmbedMe venv created in %s", DEFAULT_EMBEDME_PATH)
    _LOGGER.info("Installing EmbedMe in %s", DEFAULT_EMBEDME_PATH)
    py_executable = find_executable("python")
    subprocess.run([py_executable, "-m", "pip", "install", get_embedme_package()], env=get_env())
    return True


def run_embedme():
    from esphome.__main__ import run_esphome
    from esphome.core import EsphomeError

    try:
        return run_esphome(sys.argv)
    except EsphomeError as e:
        _LOGGER.error(e)
        return 1
    except KeyboardInterrupt:
        return 1


def main():
    if check_venv():
        return run_embedme()
    activate_venv()
    # if activate_venv returns, it was not activated
    if not create_venv():
        return 1
    activate_venv()
    # Should not return
    return 1


if __name__ == "__main__":
    sys.exit(main())
