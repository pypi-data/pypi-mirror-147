import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="contact",
    version="1.0.5",
    description="Saves the contact and fetches the name on entering number",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/baggageai/fraudcop",
    author="Abhishek Pandey",
    author_email="abhi526691shek@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["contact"],
    include_package_data=True,
    install_requires=["pymongo", "Flask", "certifi", ],
    entry_points={
        "console_scripts": [
            "contact=contact.__main__:main",
        ]
    },
)