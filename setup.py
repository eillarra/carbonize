from os import path
from setuptools import setup


with open(path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="carbonize",
    version="0.1.0",
    url="https://github.com/eillarra/carbonize",
    author="eillarra",
    author_email="eneko@illarra.com",
    license="MIT",
    description="A collection of carbon footprint calculators.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="calculator co2 carbon greenhouse emissions footprint",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    packages=["carbonize"],
    package_data={"carbonize": ["data/*.pkl", "py.typed"]},
    python_requires=">=3.7",
    zip_safe=False,
)
