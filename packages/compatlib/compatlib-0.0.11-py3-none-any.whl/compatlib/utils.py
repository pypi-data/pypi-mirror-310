import json
import os
import re
import stat
import tempfile
from contextlib import contextmanager

import yaml


def read_json(filename):
    """
    Read json from file
    """
    return json.loads(read_file(filename))


def read_file(filename):
    """
    Read in a file content
    """
    with open(filename, "r") as fd:
        content = fd.read()
    return content


def write_json(content, filename):
    with open(filename, "w") as fd:
        fd.write(json.dumps(content, indent=4))


def write_file(content, filename, executable=False):
    with open(filename, "w") as fd:
        fd.write(content)

    # Make the file executable
    if executable:
        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def read_yaml(filename):
    """
    Read yaml from file
    """
    with open(filename, "r") as fd:
        content = yaml.safe_load(fd)
    return content


def write_yaml(obj, filename):
    """
    Read yaml to file
    """
    with open(filename, "w") as fd:
        yaml.dump(obj, fd)


@contextmanager
def workdir(dirname):
    """
    Provide context for a working directory, e.g.,

    with workdir(name):
       # do stuff
    """
    here = os.getcwd()
    os.chdir(dirname)
    try:
        yield
    finally:
        os.chdir(here)


def get_tmpdir(tmpdir=None, prefix="", create=True):
    """
    Get a temporary directory for an operation.
    """
    tmpdir = tmpdir or tempfile.gettempdir()
    prefix = prefix or "flux-metrics-api-tmp"
    prefix = "%s.%s" % (prefix, next(tempfile._get_candidate_names()))
    tmpdir = os.path.join(tmpdir, prefix)

    if not os.path.exists(tmpdir) and create is True:
        os.mkdir(tmpdir)

    return tmpdir


def pretty_print_list(listing):
    """
    Pretty print a list of json (python dictionaries)
    """
    # Prepare common format
    if not isinstance(listing, list):
        listing = [listing]
    result = ""
    for i, item in enumerate(listing):
        result += "".join(f"({k}:{v})," for k, v in item.items())
        if len(listing) > 1 and i != len(listing) - 1:
            result += "\n"
    return result.strip(",")


def recursive_find(base, pattern="*.*"):
    """
    Recursively find and yield directories matching a glob pattern.
    """
    for root, dirnames, filenames in os.walk(base):
        for dirname in dirnames:
            if not re.search(pattern, dirname):
                continue
            yield os.path.join(root, dirname)


def recursive_find_files(base, pattern="*.*"):
    """
    Recursively find and yield directories matching a glob pattern.
    """
    for root, _, filenames in os.walk(base):
        for filename in filenames:
            if not re.search(pattern, filename):
                continue
            yield os.path.join(root, filename)


def normalize_soname(path):
    """
    Normalize the path, meaning removing so library versions.
    """
    if ".so." in path:
        return path.split(".so.")[0] + ".so"
    return path
