import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '1.0.0'
PACKAGE_NAME = 'valid_input' 
AUTHOR = 'Héctor Martínez González'
AUTHOR_EMAIL = 'hector.xilxes@gmail.com'
URL = 'https://github.com/hectorxlxs'

LICENSE = 'MIT'
DESCRIPTION = "A simple lightweight library to avoid writting common input checks"
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = []

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)