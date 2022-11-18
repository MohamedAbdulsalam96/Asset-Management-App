from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in asset_management/__init__.py
from asset_management import __version__ as version

setup(
	name="asset_management",
	version=version,
	description="Asset Management Application ",
	author="Lithe-Tech Limited",
	author_email="vinetech@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
