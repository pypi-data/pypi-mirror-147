import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="quicktimekeeper",
    version="1.0.0",
    description="Quickly time functions easily",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/DarkWolf2244/QuickTimer",
    author="DarkWolf",
    author_email="darkwolfx2244@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["quicktimekeeper"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "realpython=quicktimekeeper.__main__:main",
        ]
    },
)