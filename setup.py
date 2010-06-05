from setuptools import setup, find_packages

from example import __version__ as VERSION


setup(
    name = 'coins',
    version = VERSION,
    description = 'Converts HM Treasury COINS text files to an SQLite database',
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
