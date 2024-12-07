#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import shutil
import subprocess
from os import path

import setuptools
from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install

from hakkero import __version__

version = int(setuptools.__version__.split(".")[0])
assert version > 30, "requires setuptools > 30"

this_directory = path.abspath(path.dirname(__file__))


def fetch_requirements(filename):
    with open(filename, "r") as fd:
        return [r.strip() for r in fd.readlines()]


def fetch_readme():
    with open("README.md", encoding="utf-8") as fin:
        return fin.read()


class CustomInstall(install):
    def run(self):
        exe = self.compile_cpp()
        shutil.move(exe, os.path.join(self.build_lib, "hakkero/lib"))
        install.run(self)

    @staticmethod
    def compile_cpp():
        exe_path = "hakkero/lib/turboshuf"

        compile_cmd = ["g++"]
        source_files = ["hakkero/lib/turboshuf.cc"]
        compile_cmd.extend(source_files)
        compile_cmd.extend(["-o", exe_path])
        compile_cmd.extend(["-std=c++11", "-Wall", "-O3"])

        subprocess.check_call(compile_cmd)

        os.chmod(exe_path, 0o755)

        return exe_path


setup(
    name="hakkero-dataloader",
    url="https://github.com/ericxsun/hakkero-dataloader",
    keywords="Pytorch LM dataloader",
    version=__version__,
    long_description=fetch_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["examples", "tests"]),
    zip_safe=False,
    install_requires=fetch_requirements("requirements.txt"),
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#universal-wheels
    options={"bdist_wheel": {"universal": "1"}},
    entry_points={"console_scripts": ["hakkero=hakkero.dataset.indexify:main"]},
    cmdclass={"install": CustomInstall},
)
