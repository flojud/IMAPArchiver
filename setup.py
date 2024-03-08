import configparser
import os

from setuptools import find_packages, setup


def get_version():
    config = configparser.ConfigParser()

    base_folder = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(base_folder, ".bumpversion.cfg")
    config.read(config_file)
    current_version = config.get("bumpversion", "current_version")

    print("Current working directory ", os.getcwd())
    print("Reading version from ", config_file)
    print("Current version ", current_version)

    return current_version


setup(
    name="IMAPArchiver",
    version=get_version(),
    packages=find_packages(),
    install_requires=[],
    author="flojud",
    author_email="dev.flojud@gmail.com",
    description="The IMAPArchiver is a command-line tool that exports emails from your IMAP mailbox to a local folder, helping you keep your mailbox organized and your data backed up.",
    keywords="imap email export backup archive",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/flojud/IMAPArchiver",
    project_urls={
        "Bug Tracker": "https://github.com/flojud/IMAPArchiver/issues",
    },
    entry_points={
        "console_scripts": [
            "imaparchiver = main:main",
        ],
    },
    python_requires=">=3.11",
    license="MIT",
)
