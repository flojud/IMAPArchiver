# IMAPArchiver

Hello, fellow developers! 👋 

Have you ever found yourself in a situation where your IMAP mailbox is getting a bit too full, and you're concerned about losing important data? The IMAPArchiver is here to help you keep your mailbox organized and ensure that no email goes missing.

This handy script was designed to address the issue of a full IMAP mailbox while ensuring that no data is lost. By exporting your emails to a local folder, you can safely backup your email data and store it in cloud storage solutions like OneDrive. This enables easy access to old documents and provides a reliable backup solution for your important emails.

The IMAPArchiver allows you to export emails from an IMAP mailbox to a local folder. It provides a user-friendly command-line interface with various options to customize the export process.


## Features

- Export emails from an IMAP mailbox to a local folder.
- Filter emails based on the specified year.
- Support for SSL connection.
- Option to skip specific IMAP folders.
- Verbose logging and debug mode for detailed output.

## Usage

Getting started is easy! Simply clone the repository, install any required dependencies, configure the script with your IMAP server details and desired options, and run the script. Your emails will be safely exported to the specified local folder, ready for backup or archiving.


1. Clone the repository:

    ```
    git clone https://github.com/flojud/IMAPArchiver.git
    ```

2. Navigate to the cloned directory:

    ```
    cd IMAPArchiver
    ```

3. The project includes a Makefile to streamline common tasks:
    - `make clean`: Removes the virtual environment and any cached Python files.
    - `make install`: Creates a virtual environment, activates it, and installs the dependencies listed in `requirements.txt`.
    - `make run`: Activates the virtual environment and runs the `main.py` script with specified command-line arguments.


4. Run the script with appropriate command-line arguments:

    ```
    make run -s <IMAP_server_address> -u <username> -p <password> -d <export_folder_path> [-y <year_to_filter_emails>] [--ssl] [--port <port_number>] [--skip <comma_separated_folders_to_skip>] [--verbose] [--debug]
    ```

    Example:

    ```
    make run -s imap.example.com -u john@example.com -p secret -d /path/to/export_folder -y 2022 --ssl --skip "Spam,Trash" --verbose
    ```

## Command-line Arguments

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
