from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="PyExpPlotting-andnp",
    url="https://github.com/andnp/PyExpPlotting.git",
    author="Andy Patterson",
    author_email="andnpatterson@gmail.com",
    packages=find_packages(exclude=["tests*"]),
    package_data={"PyExpPlotting": ["py.typed"]},
    version="0.8.1",
    license="MIT",
    description="A few plotting utilities to go with PyExpUtils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=[
        "matplotlib>=2.2.3",
        "numba>=0.52.0",
        "scipy>=1.5.4",
        "pyexputils-andnp>=3.1.0",
    ],
    extras_require={
        "dev": [
            "mypy>=0.770",
            "flake8",
            "commitizen",
            "pre-commit",
            "pipenv-setup[black]",
            "build",
            "twine",
        ],
    },
)
