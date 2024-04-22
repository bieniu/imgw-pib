"""Setup module for imgw-pib."""

from pathlib import Path

from setuptools import setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "0.0.1"

setup(
    name="imgw_pib",
    version=VERSION,
    author="Maciej Bieniek",
    description="Python wrapper for IMGW-PIB API.",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/bieniu/imgw-pib",
    license="Apache-2.0 License",
    packages=["imgw_pib"],
    package_data={"imgw_pib": ["py.typed"]},
    python_requires=">=3.12",
    install_requires=["aiohttp>=3.8.0"],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Typing :: Typed",
    ],
)
