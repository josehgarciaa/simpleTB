from setuptools import setup, find_packages

setup(
    name="simpleTB",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'GriSPy @ git+https://github.com/mchalela/GriSPy.git',
    ],
    author="Jose H. Garcia",
    author_email="josehugo.garcia@icn2.cat",
    description="A simple package that utilizes GriSPy, NumPy, and SciPy for computational tasks",
    license="MIT",
    keywords="example computational package",
    url="http://example.com/simpleTB",
)
