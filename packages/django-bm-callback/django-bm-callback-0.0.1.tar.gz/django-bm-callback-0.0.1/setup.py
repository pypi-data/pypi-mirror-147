
from setuptools import setup, find_packages

__version__ = '0.0.1'

with open('requirements.txt') as f:
    requires = f.read().splitlines()


url = 'https://github.com/MykolaBerkosha/bm-callback'


setup(
    name='django-bm-callback',
    version=__version__,
    description='Django callback app',
    long_description='',
    author='Mykola Berkosha',
    author_email='mberkosa@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, __version__),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=requires
)
