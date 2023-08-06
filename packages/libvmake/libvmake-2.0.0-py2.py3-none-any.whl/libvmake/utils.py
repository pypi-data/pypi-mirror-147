
import sys
import pathlib
import shutil
import functools
from hashlib import md5
import json
import os
from typing import Optional
from urllib.parse import urlparse
import io
import jinja2


def md5sum(str):
    m = md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()


def private(f):
    """标记函数为私有，仅适用于开发者本人的系统配置
    """
    @functools.wraps(f)
    def func(*args, **kwargs):
        return f(*args, **kwargs)
    return func


def unset_proxy():
    try:
        del os.environ['HTTP_PROXY']
    except:
        pass
    try:
        del os.environ['HTTPS_PROXY']
    except:
        pass
    try:
        del os.environ['NO_PROXY']
    except:
        pass


def set_proxy(proxy: Optional[str], noproxy: Optional[list] = None) -> None:
    if proxy is None or proxy.strip() == "":
        proxy = ""
    else:
        try:
            urlparse(proxy)
        except:
            raise Exception('invalid proxy url')

    if proxy == "":
        unset_proxy()
    else:
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        _noproxy = [] if noproxy is None else noproxy
        os.environ["NO_PROXY"] = ",".join(_noproxy)


def copy_template(src, dest, context, encoding="utf-8"):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(src, 'r', encoding=encoding) as f:
        jinja2.Template(f.read()).stream(
            context=context).dump(dest, encoding=encoding)
        return True


def copy_templates(src_dir, dest_dir, context, encoding="utf-8"):
    for root, _, files in os.walk(src_dir):
        for _file in files:
            file = os.path.join(root, _file)
            relative_file = pathlib.Path(file).relative_to(src_dir)
            dest_file = os.path.join(dest_dir, relative_file)
            copy_template(file, dest_file, context=context, encoding=encoding)


def copy_files(src_dir, dest_dir):
    for root, _, files in os.walk(src_dir):
        for _file in files:
            file = os.path.join(root, _file)
            relative_file = pathlib.Path(file).relative_to(src_dir)
            dest_file = os.path.join(dest_dir, relative_file)
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy(file, dest_file)
