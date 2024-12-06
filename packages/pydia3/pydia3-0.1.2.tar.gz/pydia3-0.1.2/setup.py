from setuptools import setup, find_packages
import platform

setup(
    name="pydia3",
    version="0.1.2",
    description="Python interface for Microsoft's Debug Interface Access (DIA) SDK.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Michael K. Steinberg",
    author_email="m.kuper.steinberg@gmail.com",
    url="https://github.com/Michael-K-Stein/pydia",
    license="MIT",  # Update with your license
    packages=find_packages(),
    package_data={
        "pydia": ["*.pyd"] if platform.system() == "Windows" else ["*.so"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.12",
)
