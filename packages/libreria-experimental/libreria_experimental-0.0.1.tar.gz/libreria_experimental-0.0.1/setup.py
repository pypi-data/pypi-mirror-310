from setuptools import setup, find_packages
with open("README.md", "r") as f:
    description_md=f.read()
setup(name='libreria_experimental',
version='0.1',
packages=find_packages(where='libreria_experimental'),
install_requires=["sympy",
"matplotlib",
"numpy",
"statistics",
"scipy",
"mathematica"],
long_description=description_md,
long_description_content_type="text/markdown")

