
import pathlib
import subprocess
import sys
from setuptools import find_packages, setup
from setuptools.command.install import install as _install


HERE = pathlib.Path(__file__).parent

VERSION = '0.0.4'
PACKAGE_NAME = 'consepsimdisc'
AUTHOR = 'Esteban Mendiola Tellez'
AUTHOR_EMAIL = 'mendiola_esteban@outlook.com'
URL = 'https://gitlab.com/TebanMT'

LICENSE = 'MIT'
DESCRIPTION = 'Library to compute conceptual distance by using DIS-C method'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = ''


INSTALL_REQUIRES = [
    'networkx',
    'numpy',
    'nltk',
    ]

class Install(_install):
    def run(self):
        _install.do_egg_install(self)
        import nltk
        nltk.download("wordnet")

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    #cmdclass={'install': Install},
    install_requires=INSTALL_REQUIRES,
    setup_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
