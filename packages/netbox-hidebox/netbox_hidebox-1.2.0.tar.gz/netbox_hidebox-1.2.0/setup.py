import os.path
import codecs

from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='netbox_hidebox',
    version=get_version('netbox_hidebox/version.py'),
    description='Services for Netbox',
    url='',
    author='Sofien Aouni',
    author_email='contact@sofien.meme',
    maintainer='AOS',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)