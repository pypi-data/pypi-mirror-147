from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read()

def requirements(requirements_file):
    """Look through the requirements file to fetch requirements."""
    with open(requirements_file) as f:
        return f.read().splitlines()

setup(
    name="codepiper",
    version=version,
    author="Gaggle Devops",
    author_email="devops@gaggle.net",
    description="Tools for AWS CodePipeline.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaggle-net/codepiper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires="~=3.8",
    install_requires=requirements("requirements/requirements.in"),
    packages=find_packages(exclude=["*.tests", "tests.*", "tests", "*.tests.*"]),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "codepiper=codepiper.cli:main",
        ]
    },
)
