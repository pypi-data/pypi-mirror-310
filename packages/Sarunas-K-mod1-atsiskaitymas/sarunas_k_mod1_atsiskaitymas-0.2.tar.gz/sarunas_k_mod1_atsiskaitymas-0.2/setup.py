import setuptools
from docutils.nodes import version
from setuptools import setup, find_packages
from setuptools.command.install import install

setup(
    name = "Sarunas_K_mod1_atsiskaitymas",
    version = '0.2',
    author="Sarunas K",
    description="Crawler Duino.lt/Skonis_ir_kvapas.lt",
    packages= setuptools.find_packages(where="."),
    install_requires = [
        'requests == 2.32.3',
        'lxml >= 5.3.0',
        'datetime >= 5.5'
    ],
    python_requires=">=3.10"



)