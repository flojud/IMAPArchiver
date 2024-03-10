# IMAPArchiver

Have you ever found yourself in a situation where your IMAP mailbox is getting a bit too full, and you're concerned about losing important data?

The IMAPArchiver is here to ensure that no email goes missing. By exporting your emails to a local folder, you can safely backup your email data and store it in cloud storage solutions.

This enables easy access to old documents and provides a reliable backup solution for your important emails.

## Features

- Export emails from an IMAP mailbox to a local folder.
- Filter emails based on the specified year.
- Support for SSL connection.
- Option to skip specific IMAP folders.
- Verbose logging and debug mode for detailed output.

## Usage

Getting started is easy! Simply install IMAPArvchiver and configure the script with your IMAP server details and desired options, and run it. Your emails will be safely exported to the specified local folder, ready for backup or archiving.

Install:

```
pip install imaparchiver
```

Run IMAPArchiver with appropriate command-line arguments:

- `--server -s`: IMAP server address (required).
- `--user -u`: Username for IMAP authentication (required).
- `--password -p`: Password for IMAP authentication (required).
- `--destination -d`: Export folder path where emails will be saved (required).
- `--year -y`: Year to filter emails (optional).
- `--ssl`: Use SSL connection (optional).
- `--port`: Port number of the IMAP server (optional).
- `--skip`: Comma-separated list of IMAP folders to skip (optional).
- `--verbose`: Enable verbose logging (optional).
- `--debug`: Print debug output (optional).

Example:

```
imaparchiver -s imap.example.com -u john@example.com -p secret -d /path/to/export_folder -y 2022 --ssl --skip "Spam,Trash" --verbose
```

## Contribute

I welcome contributions from the community! If you've found a bug, have a feature request, or want to contribute code improvements, please submit an issue or pull request to this repository.

- Fork this repository.
- Create a branch: git checkout -b development.
- Make your changes and commit them: git commit -m '<commit_message>'
- Push to the original branch: git push origin flojud/IMAPArchiver
- Create the pull request.

Keep your mailbox organized and your data safe with the IMAPArchiver. Happy exporting!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
