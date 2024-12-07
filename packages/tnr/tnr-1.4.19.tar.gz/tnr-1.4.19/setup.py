from setuptools import setup, find_packages
import os
from setuptools.command.install import install

class InstallCommand(install):
    def initialize_options(self):
        install.initialize_options(self)
        if os.name == 'nt':  # Windows
            self.user = True

setup(
    name="tnr",
    version="1.4.19",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "Click>=8.0",
        "requests>=2.2",
        "cryptography>=40.0",
        "pathlib>=1.0.1",
        "packaging>=21.0",
        "paramiko==3.4.0",
        "yaspin==3.0.2",
        "scp==0.15.0",
        "rich-click==1.8.3",
        "rich==13.7.1",
    ],
    entry_points={"console_scripts": ["tnr=thunder.thunder:cli"]},
    cmdclass={
        'install': InstallCommand,
    },
)
# delete old dist folder first, and increment version number

# to build: python3 setup.py sdist bdist_wheel
# to distribute: twine upload dist/*
