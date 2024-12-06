from setuptools import find_packages, setup

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="petehr",
    packages=find_packages(include=["petehr"]),
    version="0.0.1",
    description="Python Toolkit for EHR Processing",
    long_description=long_description,
    url="https://github.com/apvidul/petehr",
    long_description_content_type="text/markdown",
    author="Vidul Ayakulangara Panickan",
    install_requires=[],
    python_requires=">=3.6",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
