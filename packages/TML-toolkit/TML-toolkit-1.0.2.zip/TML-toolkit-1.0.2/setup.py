import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='TML-toolkit',
    version='1.0.2',
    author="Sigurd Solberg",
    author_email="sigroll@gmail.com",
    description='Tools for topological machine learning',
    packages=setuptools.find_packages(where="src"),
    py_modules=[""], #name of python files in my library
    package_dir={'': 'src'},
)