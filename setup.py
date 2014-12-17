from setuptools import setup, find_packages

requirements = [
        "requests",
        "beautifulsoup4",
        "html5lib",
        ]

setup(
        name="libfa",
        version="0.0.0",
        packages=find_packages(),

        install_requires=requirements,
        )
