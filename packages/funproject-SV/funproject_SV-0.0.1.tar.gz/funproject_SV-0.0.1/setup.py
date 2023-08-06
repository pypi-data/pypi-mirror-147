from setuptools import setup

with open('README.md', "r") as fh:
    long_description = fh.read()

setup(
    name="funproject_SV",
    version='0.0.1',
    description="funproject_by_sv",
    py_modules=["check_pack/check_pack"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    extras_requires={
        "dev": [
            "pytest>=3.7"
        ]
    },
    url="https://sv.com",
    author= "SV",
    author_email="sv@ap.com"
)
