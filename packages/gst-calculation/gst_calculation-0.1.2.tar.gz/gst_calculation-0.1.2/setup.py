from setuptools import setup
from setuptools import find_packages
import subprocess
import os

# gst_remote_version = (
#     subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
#     .stdout.decode("utf-8")
#     .strip()
# )

# if "-" in gst_remote_version:
#     # when not on tag, git describe outputs: "1.3.3-22-gdf81228"
#     # pip has gotten strict with version numbers
#     # so change it to: "1.3.3+22.git.gdf81228"
#     # See: https://peps.python.org/pep-0440/#local-version-segments
#     v,i,s = gst_remote_version.split("-")
#     gst_remote_version = v + "+" + i + ".git." + s

# print(gst_remote_version)

# assert "-" not in gst_remote_version
# assert "." in gst_remote_version

# assert os.path.isfile("gst_calculation/version.py")
# with open("gst_calculation/VERSION", "w", encoding="utf-8") as fh:
#     fh.write(f"{gst_remote_version}\n")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name = 'gst_calculation',
	version = '0.1.2',
	description = 'This package contains Greedy String Tiling calculation',
	long_description=long_description,
    long_description_content_type="text/markdown",
	author = 'Tomy Widjaja',
	author_email = 'tomywid77@gmail.com',
	url = 'https://github.com/tomytw/gst-calculation', 
	packages = find_packages(exclude=('tests*', 'testing*')),
    package_data={"gst_calculation": ["VERSION"]},
	python_requires='>=3.7',
	classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
		"Topic :: Scientific/Engineering :: Artificial Intelligence",
		"Topic :: Text Processing :: General"
    ],
)