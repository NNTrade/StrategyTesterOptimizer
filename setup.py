# coding: utf-8
import pkg_resources
import setuptools
import os
from pathlib import Path

VERSION = "0.16.0"

file_path = os.path.join(Path('.'), "requirements.txt")
with open(file_path) as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

lib = "NNTrade.strategy_tester_optimizer"

libs = [f"{lib}.{pkg}" for pkg in setuptools.find_packages(where="src")]
libs.append(lib)

setuptools.setup(
    name=lib,
    version=VERSION,
    description="Framework for testing and optimizing strategies",
    author_email="insonus.k@gmail.com",
    url="https://github.com/NNTrade/StrategyTesterOptimizer",
    keywords=[],
    install_requires=install_requires,
    packages=libs,
    package_dir={lib: 'src'},
    include_package_data=True,
    long_description="""\
    Strategy optimizer tool, based on book 'Design, testing and optimisation of trading system' by Robert Pardo
    """
)
