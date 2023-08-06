import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="commented_code",
    version="0.1.0",
    description="Mininal pylint addon to detect commented code.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/paulourbano-com/commented_code",
    author="Paulo Urbano",
    author_email="paulo@paulourbano.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["commented_code"],
    include_package_data=True,
    install_requires=["astroid", "pylint"],
)
