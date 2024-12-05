from setuptools import find_packages, setup

setup(
    name="ehrt",
    packages=find_packages(include=["ehrt"]),
    version="0.1.3",
    description="EHR Processing Toolkit",
    author="Vidul Ayakulangara Panickan",
    install_requires=[],
    python_requires=">=3.6",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
