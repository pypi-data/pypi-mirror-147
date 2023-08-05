__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"


from ohno.logger import logger
from subprocess import Popen, PIPE, STDOUT
import os


def which(software=None, strip_newline=True):
    """get_install will return the path to where Singularity (or another
    executable) is installed.
    """
    if software is None:
        software = "singularity"
    cmd = ["which", software]
    try:
        result = run_command(cmd)
        if strip_newline is True:
            result["message"] = result["message"].strip("\n")
        return result

    except:  # FileNotFoundError
        return None


def get_userhome():
    """get the user home based on the effective uid. If import of pwd fails
    (not supported for Windows) then fall back to environment variable.
    """
    try:
        import pwd

        return pwd.getpwuid(os.getuid())[5]
    except:
        return os.environ.get("HOME") or os.environ.get("HOMEPATH")


def get_user():
    """Get the name of the user. We first try to import pwd, but fallback to
    extraction from the environment.
    """
    try:
        import pwd

        return pwd.getpwuid(os.getuid())[0]
    except:
        return os.environ.get("USER") or os.environ.get("USERNAME")


def check_install(software, quiet=True, command="--version"):
    """check_install will attempt to run the singularity command, and
    return True if installed. The command line utils will not run
    without this check.

    Parameters
    ==========
    software: the software to check if installed
    quiet: should we be quiet? (default True)
    command: the command to use to check (defaults to --version)
    """
    cmd = [software, command]
    try:
        version = run_command(cmd, software)
    except:  # FileNotFoundError
        return False
    if version:
        if not quiet and version["return_code"] == 0:
            version = version["message"]
            logger.info("Found %s version %s" % (software.upper(), version))
        return True
    return False


def get_installdir():
    """get_installdir returns the installation directory of the application"""
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def run_command(cmd, sudo=False, stream=False):
    """run_command uses subprocess to send a command to the terminal.

    Parameters
    ==========
    cmd: the command to send, should be a list for subprocess
    error_message: the error message to give to user if fails,
    if none specified, will alert that command failed.

    """
    stdout = PIPE if not stream else None
    if sudo is True:
        cmd = ["sudo"] + cmd

    try:
        output = Popen(cmd, stderr=STDOUT, stdout=stdout)

    except FileNotFoundError:
        cmd.pop(0)
        output = Popen(cmd, stderr=STDOUT, stdout=PIPE)

    t = output.communicate()[0], output.returncode
    output = {"message": t[0], "return_code": t[1]}

    if isinstance(output["message"], bytes):
        output["message"] = output["message"].decode("utf-8")

    return output


def confirm_action(question, force=False):
    """confirm if the user wants to perform a certain action

    Parameters
    ==========
    question: the question that will be asked
    force: if the user wants to skip the prompt
    """
    if force is True:
        return True

    response = input(question)
    while len(response) < 1 or response[0].lower().strip() not in "ynyesno":
        response = input("Please answer yes or no: ")

    if response[0].lower().strip() in "no":
        return False

    return True


def confirm_uninstall(filename, force=False):
    """confirm if the user wants to uninstall a module

    Parameters
    ==========
    filename: the file that will be removed
    force: if the user wants to skip the prompt
    """
    return confirm_action(
        "Are you sure you want to uninstall {}".format(filename), force
    )
