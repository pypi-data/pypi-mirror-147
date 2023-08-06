import os
from setuptools import setup, find_packages
import shutil
from hashlib import sha512

SCRIPTS_PATH = 'build_scripts'
EXECUTABLES_PATHS = ['/tilesetgenerator/data/scope.sh']

def hash_file(path):
    with open(path, 'rb') as fobj:
        return sha512(fobj.read()).digest()

def scripts_hack(*scripts):
    ''' Hack around `pip install` temporary directories '''
    if not os.path.exists(SCRIPTS_PATH):
        os.makedirs(SCRIPTS_PATH)
    scripts_path = []
    for src_path, basename in scripts:
        dest_path = os.path.join(SCRIPTS_PATH, basename)
        if not os.path.exists(dest_path) or \
                (os.path.exists(src_path) and hash_file(src_path) != hash_file(dest_path)):
            shutil.copy(src_path, dest_path)
        scripts_path += [dest_path]
    return scripts_path

setup(
    name = "tilesetgenerator",
    version = "0.1.1",
    description = "Generates a tilemap from a few template images",
    url = "https://gitlab.com/john_t/tile-set-generator",
    author = "John Toohey",
    author_email = "john_t@mailo.com",
    license = "GPL3",
    packages = find_packages(include = ["tilesetgenerator", "tilesetgenerator.*"]),
    install_requires = ["pillow"],
    scripts = scripts_hack(("tilesetgenerator/__init__.py", "tilesetgenerator")),
    classifiers = [
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Build Tools"
    ]
)
