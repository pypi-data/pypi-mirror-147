# rerpypt - setup

from setuptools import setup
from os.path import exists


if exists("README.md"):
    with open("README.md", "r") as f:
        long_description = f.read()
else:
    long_description = "..."


with open(f"reprypt/__init__.py", "r") as f:
    text = f.read()
    version = text.split('__version__ = "')[1].split('"')[0]


requires = []


setup(
    name='reprypt',
    version=version,
    description='Encryption Module',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://tasuren.github.io/reprypt/',
    author='tasuren',
    author_email='tasuren5@gmail.com',
    license='MIT',
    keywords='encrypt decrypt encryption',
    packages=["reprypt"],
    entry_points={
        "console_scripts": [
            "reprypt = reprypt.__main__:main"
        ]
    },
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
