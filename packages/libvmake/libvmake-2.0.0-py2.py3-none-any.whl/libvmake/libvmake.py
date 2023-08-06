# Author:
# @author yuhuan
# @email uforgetmenot@yuhuans.cn
# @create date 2021-05-29 15:23:14
# @modify date 2021-07-29 23:23:20
# @desc vmake library

#!/usr/bin/env python3

# encoding: utf-8

import atexit
import base64
from contextlib import contextmanager
import locale
from posixpath import dirname
from tempfile import mkstemp
from typing import Any, Callable, Optional, Tuple
import logging
import shutil
import sys
import os
import argparse
import subprocess
import functools
import platform
import time
import selectors
import distro
import yaml
from pathlib import Path
import requests

try:
    import fcntl
except:
    pass

# define variables
root = os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0])))
cwd = os.getcwd()

# os.chdir(root)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s: %(message)s')
log = logging.getLogger("vmake")

linux = sys.platform == 'linux'
windows = sys.platform == "win32"
posix = os.name == 'posix'

# global functions


def current_file(*args):
    """get file path of current directory

    Returns:
        [type]: [description]
    """
    return os.path.join(root, *args)


def valid_str(s: str) -> bool:
    """check str is empty or not
    """
    return s is not None and s.strip() != ""


def get_bash() -> str:
    """get valid bash executable path

    Raises:
        Exception: raise exception if no valid bash found

    Returns:
        [str]: bash path 
    """
    bash = shutil.which('bash')
    if bash is None:
        raise Exception("no bash found")
    if windows:
        if 0 != os.system(f'{bash} -c \'test "Msys"="$(uname -o)"\''):
            raise Exception("no valid bash found")
        else:
            return bash
    else:
        return bash


def get_evelate():
    """Finding the directory of the python file and then joining it with the res folder and the elevate.exe file.

    Returns:
        str: the location of elevate executable
    """

    pyfiledir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    return os.path.join(pyfiledir, 'res', 'elevate.exe')


def get_gsudo():
    """ Getting the directory of the file and then joining it with the res folder and then the gsudo.exe file.

    Returns:
        str: the location of gsudo.exe executaable
    """

    pyfiledir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    return os.path.join(pyfiledir, 'res', 'gsudo.exe')


@contextmanager
def pushd(dir: str):
    """push the dir

    Args:
        dir (str): the directory to push
    """
    curdir = os.getcwd()
    try:
        os.chdir(dir)
        yield
    finally:
        os.chdir(curdir)


def posix_execute(cmd, shell=True, encoding="utf-8", stream_print=True, executable=None, workdir=None, check_result=True):
    """run command in the posix

    Args:
        cmd (str): the command to execute
        shell (bool, optional): whether run command in shell. Defaults to True.
        encoding (str, optional): the encoding of the output. Defaults to "utf-8".
        stream_print (bool, optional): whether print the command and outputs. Defaults to True.
        executable (str, optional): specify the shell executable. Defaults to None.
        workdir (str, optional): specify the work directory. Defaults to None.
        check_result (bool, optional): whether check the command return code is zero or not. Defaults to True.

    Raises:
        Exception: raise exception when error occurred

    Returns:
        tuple: (retcode, stdout, stderr)
    """
    curpath = os.getcwd()
    try:
        if workdir is not None:
            os.chdir(workdir)
        if stream_print:
            print(f"execute command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=shell,
                             encoding=encoding,
                             close_fds=True,
                             executable=executable
                             )

        stdout = []
        stderr = []
        try:
            selector = selectors.DefaultSelector()
        except (IOError, OSError):
            selector = selectors.PollSelector()
        selector.register(p.stdout, selectors.EVENT_READ)
        selector.register(p.stderr, selectors.EVENT_READ)
        if os.name == 'posix':
            fcntl.fcntl(p.stdout.fileno(), fcntl.F_SETFL, fcntl.fcntl(
                p.stdout.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)
            fcntl.fcntl(p.stderr.fileno(), fcntl.F_SETFL, fcntl.fcntl(
                p.stderr.fileno(), fcntl.F_GETFL) | os.O_NONBLOCK)
        while True:
            events = selector.select(1)
            for key, event in events:
                data = key.fileobj.read().strip()
                if data == '':
                    selector.unregister(key.fileobj)
                    continue
                if key.fileobj == p.stdout:
                    if stream_print:
                        sys.stdout.write(data + "\n")
                    stdout.extend(data.split('\n'))
                elif key.fileobj == p.stderr:
                    if stream_print:
                        sys.stdout.write(data + "\n")
                    stderr.extend(data.split('\n'))
            if (not events or not selector.get_map()) and p.poll() is not None:
                break
            elif not selector.get_map() and p.poll() is None:
                p.wait()
                break
        p.stdout.close()
        p.stderr.close()
        selector.close()
        p.returncode
    except Exception as e:
        raise Exception(f"execute cmd {cmd} failed: {e}")
    finally:
        if workdir is not None:
            os.chdir(curpath)
    if check_result and p.returncode != 0:
        raise Exception(
            f"execute cmd {cmd} failed with return code {p.returncode}")
    return (p.returncode, stdout, stderr)


def nt_execute(cmd, shell=True, encoding="utf-8", stream_print=True, executable=None, workdir=None, check_result=True):
    """run command in windows system

    Args:
        cmd (str): the command to execute
        shell (bool, optional): whether run command in shell. Defaults to True.
        encoding (str, optional): the encoding of the output. Defaults to "utf-8".
        stream_print (bool, optional): whether print the command and outputs. Defaults to True.
        executable (str, optional): specify the shell executable. Defaults to None.
        workdir (str, optional): specify the work directory. Defaults to None.
        check_result (bool, optional): whether check the command return code is zero or not. Defaults to True.

    Raises:
        Exception: raise Exception when error


    Returns:
        tuple: (retcode, stdout)

    """
    curpath = os.getcwd()
    try:
        if workdir is not None:
            os.chdir(workdir)
        if stream_print:
            print(f"execute command: {cmd}")
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=shell,
                             executable=executable,
                             encoding=None)

        def readline(cmd):
            for line in iter(p.stdout.readline, b''):
                if line == b"":
                    break
                else:
                    yield line.decode(encoding, 'ignore')  # strict
            while p.poll() is None:
                time.sleep(.1)
        stdout = []
        for line in readline(cmd):
            if line is not None:
                line.strip()
                stdout.append(line[0:-1])
                if stream_print:
                    print(line, end='')
        p.stdout.close()
    except Exception as e:
        raise Exception(f"execute cmd {cmd} failed: {e}")
    finally:
        if workdir is not None:
            os.chdir(curpath)
    if check_result and p.returncode != 0:
        raise Exception(
            f"execute cmd {cmd} failed with return code {p.returncode}")
    return (p.returncode, stdout, [])


def execute(cmd, shell=True, encoding=locale.getpreferredencoding(), stream_print=True, executable=None, workdir=None, check_result=1):
    """execute command in linux or windows system
    """
    if windows:
        return nt_execute(cmd, shell=shell, encoding=encoding, stream_print=stream_print, executable=executable, workdir=workdir, check_result=check_result)
    else:
        return posix_execute(cmd, shell=shell, encoding=encoding, stream_print=stream_print, executable=executable, workdir=workdir, check_result=check_result)


def get_github_gist(token, gist_id, filename):
    """get github gist content
    """
    response = requests.get(f"https://api.github.com/gists/{gist_id}", headers={
        "Authorization": f"token {token}"
    })
    return response.json()["files"][filename]['content']


def get_github_gists(token):
    """get github gist lists
    """
    response = requests.get(f"https://api.github.com/gists", headers={
        "Authorization": f"token {token}"
    })
    return response.json()


def pip_install(*args) -> bool:
    """pip install packages
    """
    pip_registry = os.environ.get('pip_registry')
    pip_registry_args = f"-i {pip_registry}" if valid_str(pip_registry) else ""
    return 0 == execute(f'{sys.executable} -m pip install {pip_registry_args} --no-input {" ".join(args)}')[0]


def downloads(url: str, file: str, ignoreError=False) -> Tuple[bool, Optional[str]]:
    """download to file from url
    """
    try:
        _file = file
        if not os.path.isdir(file):
            os.makedirs(os.path.dirname(file), exist_ok=True)
            # touch(file)
            _file = file
        else:
            _file = os.path.join(file, os.path.basename(url))
            # touch(_file)
        req = requests.get(url, allow_redirects=True)
        if req.status_code != 200:
            raise Exception(f"download status code {req.status_code}")
        open(_file, 'wb').write(req.content)
        if req is not None:
            req.close()
        return True, _file
    except Exception as e:
        log.error(f"download {url} failed: {e}")
        if not ignoreError:
            raise e
        return False, None


def assume(condition: bool, errmsg: str = None):
    """assert condition
    """
    if not condition:
        raise Exception(
            errmsg if errmsg is not None else f"execute task {action} failed")


def clean_venv():
    """clean venv directory
    """
    log.info("clean virtualenv")
    shutil.rmtree(os.path.join(root, ".venv"))


def get_venv_python():
    """get venv's python executable
    """
    return os.path.join(root, ".venv", "Scripts", "python.exe") if windows else os.path.join(root, '.venv', 'bin', 'python')


def create_venv_ifnot_exists():
    """create venv if not exists
    """
    log.info("create virtualenv")
    env_python = get_venv_python()
    if not os.path.exists(env_python):
        execute(f'{sys.executable} -m venv {os.path.join(root, ".venv")}')


def copydir(srcdir: str, destdir: str):
    """directory copy
    """
    for i in Path(srcdir).glob('*'):
        shutil.copy(i, destdir) if os.path.isfile(
            i) else shutil.copytree(i, os.path.join(destdir, os.path.basename(i)))


def abort(*args):
    """abort
    """
    log.error(f"error: {' '.join(args)} ... aborting")
    sys.exit(1)


def checkbin(bin: str) -> str:
    """check if executable exists
    """
    executable = shutil.which(bin)
    if executable is None:
        raise Exception(f"no binary {bin} found")
    return executable


def get_linuxuser(username: str) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    """get linux user's uid, gid, homedir by username, only suite for linux

    Args:
        username (str): specify linux username

    Returns: (uid, gid, homedir) return user's uid, gid, and home directory
    """
    if not posix:
        raise Exception("can not get linux user in this operation system")
    import pwd
    try:
        pwnam = pwd.getpwnam(username)
        return (pwnam.pw_uid, pwnam.pw_gid, pwnam.pw_dir)
    except KeyError:
        return (None, None, None)


def su(username: str) -> Tuple[int, int, str]:
    """change to another user, suite for linux only
    """
    uid, gid, homedir = get_linuxuser(username)
    if uid is None or gid is None or homedir is None:
        raise Exception("user is not exists")
    os.setegid(gid)
    os.seteuid(uid)
    return (uid, gid, homedir)


def checkroot():
    """check if current process is running with root or admin privilege
    """
    if windows:
        result = execute(
            'PowerShell -ExecutionPolicy Unrestricted -Command "& {$(New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)}"')
        if result[0] != 0 or result[1][0] != "True":
            raise Exception("check root privilege failed")
    else:
        if 0 != os.getuid():
            raise Exception("check root privilege failed")


def touch(file):
    """create file if not exists
    """
    if not os.path.exists(file):
        with open(file, mode='w', encoding='utf-8') as f:
            f.write('')


def ignore(cb: Callable, *args, **kwargs) -> Any:
    """ignore exceptions throwed by callback function execution
    """
    try:
        return functools.partial(cb, *args, **kwargs)()
    except Exception as e:
        log.error(f"ignore error occurred: {e}")


tasks = []


def task(help=''):
    """decorate the function indicate that it is a task function
    """
    def _task(f):
        tasks.append((f.__name__, help))

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = None
            try:
                result = f(*args, **kwargs)
            except Exception as e:
                print(
                    f"error: execute task {f.__name__} failed: {e}", file=sys.stderr)
                raise(e)
                # sys.exit(1)
            else:
                pass
                # print(f"ok: task {f.__name__} has been done, no error found")
            return result
        return wrapper
    return _task


def get_distribution() -> Tuple[Optional[str], Optional[int]]:
    """get distribution of my os
    """
    sys_distro = None
    sys_version = None

    try:
        if windows:
            sys_distro = "windows".lower().strip()
            sys_version = int(platform.win32_ver()[0])
        elif linux:
            sys_distro = distro.os_release_info()['id'].lower().strip()
            sys_version = int(distro.major_version())
        if sys_distro is None or len(sys_distro) == 0 or sys_version is None:
            raise Exception("get system distro failed")
        return (sys_distro, sys_version)
    except:
        raise Exception("get system distro failed")


action = None


# define parameters parser
def parse_args(callable: Callable[[argparse.ArgumentParser], None]) -> Tuple[argparse.Namespace, argparse.ArgumentParser]:
    """add argument parser

    Args:
        callable (Callable[[argparse.ArgumentParser], None]): the callback function to add custom parser.add_argument
        eg: 
            parser.add_argument("--arch", action="store",
                            help="specify architecture, value: 32 or 64(default)",
                            choices=['32', '64'],
                            default='64'
                            )
            parser.add_argument("--debug", action="store_true", default=False,
                                help="build debug library")
            parser.add_argument("--release", action="store_true", default=False,
                                help="build release library")

    Returns:
        argparse.Namespace: parsed arguments namespace
    """
    global action
    try:
        action = 'help' if sys.argv[1] == '-h' or sys.argv[1] == "--help" else sys.argv[1]
    except:
        log.error("no action specified ... aborting")
        sys.exit(1)

    _table = '\t'
    _line = '\n'
    parser = argparse.ArgumentParser(usage=f'''{os.path.basename(__file__)} <action> [optional_arguments]
action is one of:
{_line.join(map(lambda x: '    ' + x[0] + _table + x[1] , tasks))}''')
    functools.partial(callable, parser)()
    parsed_args = parser.parse_args(sys.argv[2:])

    return parsed_args, parser


def run_task():
    global action
    global tasks

    if action is None:
        raise Exception("action is invalid, you should call parse_args first")

    module = sys.modules["__main__"]
    if action not in map(lambda x: x[0], tasks):
        raise Exception(f"no action {action} registered")
    try:
        getattr(module, action)()
    except AttributeError:
        raise Exception(f"no action {action} found")


def check_pid(pid):
    """check if process with pid exists or not
    """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def write_tmpfile(suffix, content: bytes) -> str:
    """ write bytes to template file
    """
    fd, file = mkstemp(suffix=suffix, text=False)
    os.write(fd, content)
    os.close(fd)

    def clean():
        try:
            os.unlink(file)
        except:
            pass
    atexit.register(clean)
    return file


def execute_bash(command: str, super=False, encoding="utf-8", stream_print=True, executable=None, workdir=None, check_result=1) -> Tuple[int, list, list]:
    file = write_tmpfile('.sh', command.encode('utf-8').replace(b'\r\n', b'\n'))
    sudo = f"{get_gsudo()} -w " if sys.platform == "win32" else "sudo "
    return execute(f"{sudo if super else ''}bash {file}", shell=True, encoding=encoding, stream_print=stream_print, executable=executable, workdir=workdir, check_result=check_result)


def execute_wsl(command: str, distro=None, super=False, encoding="utf-8", stream_print=True, executable=None, workdir=None, check_result=1) -> Tuple[int, list, list]:
    file = write_tmpfile('.sh', command.encode('utf-8').replace(b'\r\n', b'\n'))
    log.info(f"script file is {file}")
    with pushd(os.path.dirname(file)):
        scriptroot = subprocess.check_output(
            f"wsl{'' if distro is None else (' ' + distro)} -e pwd", encoding='utf-8').replace('\n', '')
        scriptfile = f"{scriptroot}/{os.path.basename(file)}"

    return execute(f"wsl{'' if distro is None else (' ' + distro)} -e {'sudo' if super else ''} bash {scriptfile}", shell=True, encoding=encoding, stream_print=stream_print, executable=executable, workdir=workdir, check_result=check_result)


def execute_cmd(command: str, super=False, encoding=locale.getpreferredencoding(), stream_print=True, executable=None, workdir=None, check_result=1) -> Tuple[int, list, list]:
    file = write_tmpfile('.cmd', command.encode('utf-8').replace(b'\r\n', b'\n'))
    sudo = f"{get_gsudo()} -w "
    return execute(f"{sudo if super else ''}cmd /c {file}", shell=True, encoding=encoding, stream_print=stream_print, executable=executable, workdir=workdir, check_result=check_result)


def execute_powershell(command: str, super=False, encoding=locale.getpreferredencoding(), stream_print=True, executable=None, workdir=None, check_result=1) -> Tuple[int, list, list]:
    _command = base64.b64encode(command.encode('UTF-16LE')).decode('ascii')
    elevate = f"{get_gsudo()} -w "
    result = execute(
        f'{elevate if super else ""}powershell -NoLogo -executionpolicy bypass -encodedCommand {_command}', encoding=encoding, stream_print=stream_print, executable=executable, workdir=workdir, check_result=check_result)
    return result


def execute_powershell2(command: str, super=False, encoding=locale.getpreferredencoding(), stream_print=True, executable=None, workdir=None, check_result=1) -> Tuple[int, list, list]:
    file = write_tmpfile('.ps1', command.encode('utf-8').replace(b'\r\n', b'\n'))
    elevate = f"{get_gsudo()} -w "
    return execute(
        f'{elevate if super else ""}powershell -NoLogo -executionpolicy bypass -file {file}', encoding=encoding, stream_print=stream_print, executable=executable, workdir=workdir, check_result=check_result)
    return result


def download_github_release(repo: str, release_file: str, download_file: str) -> Tuple[bool, Optional[str]]:
    """download from github releases

    Args:
        repo (str)): the repo name 
        release_file (str): the release filename, it can contains 'tag', eg: "python-{tag}.exe"
        download_file (str): the download destination file

    Returns:
        Tuple[bool, Optional[str]]: (if download ok, error message or download file)
    """
    release_api_url = f"https://api.github.com/repos/{repo}/releases"
    tag_name: str = requests.get(release_api_url).json()[0]['tag_name']
    download_url = f"https://github.com/{repo}/releases/download/{tag_name}/{release_file.format(tag = tag_name.replace('v', ''))}"
    return downloads(download_url, download_file)
