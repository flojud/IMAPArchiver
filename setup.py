from setuptools import find_packages, setup

setup(
    name="IMAPArchiver",
    version="0.1.0",
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
