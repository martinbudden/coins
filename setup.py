from setuptools import setup, find_packages

from coins import __version__ as VERSION


setup(
    name = 'coins',
    version = VERSION,
    description = 'Utilities to read HM Treasury COINS files, and to convert to more useful formats',
    author = 'Martin Budden',
    author_email = '',
    platforms = 'Posix; MacOS X; Windows',
    scripts = ['example_script'],
    packages = find_packages(exclude=['test']),
    install_requires = [
        'example_require'],
    include_package_data = True,
    zip_safe = False
    )
