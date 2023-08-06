from vogue import __version__ as version
from setuptools import setup, find_packages

try:
    with open("requirements.txt", "r") as f:
        install_requires = [x.strip() for x in f.readlines()]
except IOError:
    install_requires = []

setup(
    name="vogue",
    version=version,
    url="https://github.com/Clinical-Genomics/vogue",
    author="Maya Brandi",
    author_email="maya.brandi@scilifelab.se",
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": ["vogue=vogue.commands:cli"],
    },
)
