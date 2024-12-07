from setuptools import setup, Extension, find_packages
import numpy as np

with open ("README.md", "r") as f:
    long_description = f.read()

c_module = Extension(
    name="gixpy_c",
    sources=["source\\gixpy.c"],
    include_dirs=[np.get_include()],
    language="c",
)

setup(
    packages=find_packages(include=["source", "source.*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    ext_modules=[c_module],
)