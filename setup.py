import os
from setuptools import setup

class makeEnv:
    def run(self):
        os.mkdir("data")

setup(
    name="file_checker",
    version="1.0.0",
    author="Khitsko Konstantin",
    author_email="khitsko.konstantin@gmail.com",
    description=("Tool for generate random files, analyze and storage data"),
    license="BSD",
    keywords="example documentation tutorial",
    url="http://packages.python.org/an_example_pypi_project",
    # long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)


