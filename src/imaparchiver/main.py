import argparse
import email
import imaplib
import os
import re
import time
from datetime import datetime
from email import message

VERBOSE = False
DEBUG = False


class EmailStats:
    """
    A class to represent statistics related to email processing.

    Attributes:
    - total_folders (int): Total number of email folders processed.
    - total_messages (int): Total number of messages processed.
    - matched_year_messages (int): Number of messages matched with a specific year.
    - start_time (float): Time when the statistics tracking started.
    """

    def __init__(self):
        """
        Initializes EmailStats with default values for attributes.
        """
        self.total_folders = 0
        self.total_messages = 0
        self.matched_year_messages = 0
        self.start_time = time.time()

    def increment_folders(self):
        """
        Increment the total_folders attribute by 1.
        """
        self.total_folders += 1

    def increment_messages(self):
        """
        Increment the total_messages attribute by 1.
        """
        self.total_messages += 1

    def increment_matched_year_messages(self):
        """
        Increment the matched_year_messages attribute by 1.
        """
        self.matched_year_messages += 1

    def print_stats(self):
        """
        Print the statistics related to email processing, including total folders,
        total messages, messages matched with a specific year, and elapsed time.
        """
        duration = time.time() - self.start_time
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        print("Total Folders:", self.total_folders)
        print("Total Messages:", self.total_messages)
        print("Messages Matched the Year:", self.matched_year_messages)
        print(
            "Elapsed time: {:02}:{:02}:{:02}".format(
                int(hours), int(minutes), int(seconds)
            )
        )


def parse_date(date_str: any) -> str:
    """
    Parse the given date string into a datetime object.

    Parameters:
    - date_str (any): A date string to be parsed.

    Returns:
    - str: A string representation of the parsed date in datetime format.

    If the input date_str is an instance of email.header.Header, it is converted
    to a string before parsing. If the parsing fails, a warning message is printed,
    and None is returned.

    Example usage:
    ```
    parsed_date = parse_date("Wed, 06 Mar 2024 12:30:00 +0000")
    ```
    """
    if isinstance(date_str, email.header.Header):
        date_str = str(date_str)
    date_tuple = email.utils.parsedate(date_str)
    if not date_tuple:
        print("Warning: Failed to parse date > " + date_str + " < Skipping this email.")
        return
    return datetime(*date_tuple[:6])


def sanitize_string(input_str: str) -> str:
    """
    Sanitize the input string by removing special characters, excess spaces,
    and invalid characters.

    Parameters:
    - input_str (str): The string to be sanitized.

    Returns:
    - str: The sanitized string.

    The function performs the following operations:
    1. Strips leading and trailing whitespace.
    2. Converts the string to lowercase.
    3. Removes special characters except for alphabets, numbers, spaces, '@', and '.'.
    4. Replaces consecutive spaces with a single space.
    5. Replaces spaces with hyphens.
    6. Handles special cases for strings starting or ending with '.', ':', or '.lock'.
    7. Removes invalid characters '*', ':', '<', '>', '/', '\', '|'.
    8. Handles special names like '.lock', 'CON', 'PRN', etc., returning "no-name" if found.
    9. Limits the length of the string to 128 characters.

    Example usage:
    ```
    sanitized_str = sanitize_string("Hello! This is a Sample String 123.")
    ```
    """
    input_str = input_str.strip()
    input_str = input_str.lower()
    input_str = re.sub(r"[^a-z0-9\s@.]", "", input_str)
    input_str = re.sub(r"\s+", " ", input_str)
    input_str = input_str.replace(" ", "-")

    if input_str.startswith("."):
        input_str = input_str.lstrip(".")

    if input_str.endswith("."):
        input_str = input_str.rstrip(".")

    if input_str.startswith(":"):
        input_str = input_str.lstrip(":")

    invalid_chars = r"[\*:<>/\\|]"
    input_str = re.sub(invalid_chars, "", input_str)

    invalid_names = [
        ".lock",
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM0",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT0",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
        "_vti_",
        "desktop.ini",
    ]
    if input_str.startswith("~$") or input_str in invalid_names:
        return "no-name"

    max_char = 128
    if len(input_str) > max_char:
        input_str = input_str[-max_char:]
    return input_str


def parse_sender_email(sender: any) -> str:
    """
    Parse the sender email address from the given sender information.

    Parameters:
    - sender (any): The sender information from which the email address will be parsed.

    Returns:
    - str: The parsed sender email address.

    The function attempts to extract the email address enclosed in angle brackets
    from the sender information using a regular expression. It then sanitizes
    the extracted email address using the sanitize_string function. If extraction
    or sanitization fails, it returns None.

    Example usage:
    ```
    sender_email = parse_sender_email("John Doe <john.doe@example.com>")
    ```
    """
    try:
        if isinstance(sender, email.header.Header):
            sender = str(sender)
        sender_email_match = re.search(r"<([^>]+)>", sender)
        sender_email = sender_email_match.group(1) if sender_email_match else None
        sender_email = sanitize_string(sender_email)
    except KeyError:
        if DEBUG:
            print(f"Warning: sender KeyError {sender}. Will set to None.")
        sender_email = None
    except AttributeError:
        if DEBUG:
            print(f"Warning: sender AttributeError {sender}.")
        sender_email = sanitize_string(sender)
    return sender_email


def mkdir_email_folder(
    base_dir: str, date_obj: datetime, year_dir: str, email_dir: str
):
    """
    Create a directory for storing emails based on the provided parameters.

    Parameters:
    - base_dir (str): The base directory where the email folder will be created.
    - date_obj (datetime): The date object representing the date of the email.
    - year_dir (str): The directory name representing the year.
    - email_dir (str): The directory name representing the email type or category.

    Returns:
    - str: The path of the created email folder.

    The function constructs the folder path using the base directory, year directory,
    email directory, and date directory (derived from the date object). It then creates
    the folder path using os.makedirs, ensuring that the directories are created
    recursively if they do not exist.

    Example usage:
    ```
    folder_path = mkdir_email_folder("/path/to/base_dir", datetime.now(), "2024", "inbox")
    ```
    """
    date_dir = date_obj.strftime("%Y-%m-%d")
    folder_path = os.path.join(base_dir, f"{year_dir}/{email_dir}/{date_dir}/")
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def normalize_subject(subject: str) -> str:
    """
    Normalize the subject string by handling empty subjects and sanitizing special characters.

    Parameters:
    - subject (str): The subject string to be normalized.

    Returns:
    - str: The normalized subject string.

    If the subject is empty, it is replaced with "no-subject". The function then
    sanitizes the subject string using the sanitize_string function to remove
    special characters and ensure consistency.

    Example usage:
    ```
    normalized_subject = normalize_subject("RE: Hello!")
    ```
    """
    if not subject:
        if DEBUG:
            print(f"Warning: no subject given. Fallback to no-subject")
        subject = "no-subject"

    subject = sanitize_string(str(subject))
    return subject


def normalize_filename(filename: str) -> str:
    """
    Normalize the filename by handling empty filenames and sanitizing special characters.

    Parameters:
    - filename (str): The filename to be normalized.

    Returns:
    - str: The normalized filename.

    If the filename is empty, it is replaced with "no-name". The function then
    splits the filename into parts based on '.' and sanitizes each part using
    the sanitize_string function. Finally, it joins the sanitized parts with
    '.' and returns the normalized filename.

    Example usage:
    ```
    normalized_filename = normalize_filename("document_123.txt")
    ```
    """
    if not filename:
        filename = "no-name"
    if "." in filename:
        filename_parts = filename.split(".")
        filename = (
            ".".join([sanitize_string(part) for part in filename_parts[:-1]])
            + "."
            + sanitize_string(filename_parts[-1])
        )
    else:
        filename = sanitize_string(filename)

    return filename


def save_message(raw_email: str, msg_path: str) -> None:
    """
    Save the raw email content to a file.

    Parameters:
    - raw_email (str): The raw email content to be saved.
    - msg_path (str): The file path where the email will be saved.

    Returns:
    - None

    The function writes the raw email content to the specified file path in binary mode.

    Example usage:
    ```
    save_message(raw_email_content, "/path/to/email.msg")
    ```
    """
    with open(msg_path, "wb") as f:
        f.write(raw_email)


def save_attachments(msg: message.EmailMessage, folder_path: str) -> None:
    """
    Save attachments from an email message to the specified folder path.

    Parameters:
    - msg (message.EmailMessage): The email message containing attachments.
    - folder_path (str): The folder path where attachments will be saved.

    Returns:
    - None

    The function iterates through the parts of the email message and saves attachments
    to the specified folder path. It normalizes the filenames using the normalize_filename
    function and writes the attachment content to files.

    Example usage:
    ```
    save_attachments(email_message, "/path/to/attachments_folder")
    ```
    """
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            if DEBUG:
                print(f"Warning: Attachment Part iy type multipart. Skipping.")
            continue

        if part.get("Content-Disposition") is None:
            if DEBUG:
                print(f"Warning: Expected to be displayed inline. Skipping.")
            continue

        filename = part.get_filename()
        if filename:
            filename = normalize_filename(filename)
            attachment_path = os.path.join(folder_path, filename)
            payload = part.get_payload(decode=True)
            if payload is not None:
                with open(attachment_path, "wb") as f:
                    f.write(payload)
            else:
                if DEBUG:
                    print(
                        f"Warning: Payload is None for attachment {filename}. Skipping."
                    )
        else:
            if DEBUG:
                print(f"Warning: Filename is None. Skipping.")


def export_emails(
    imap_server: str,
    username: str,
    password: str,
    destination: str,
    year: int = None,
    use_ssl: bool = False,
    port: int = None,
    verbose: bool = False,
    debug: bool = False,
    skip: str = None,
):
    """
    Export emails from an IMAP server to the specified destination folder.

    Parameters:
    - imap_server (str): The IMAP server address.
    - username (str): The username for accessing the IMAP server.
    - password (str): The password for accessing the IMAP server.
    - destination (str): The folder path where emails will be exported.
    - year (int): The year to filter emails. If None, all emails are exported.
    - use_ssl (bool): Indicates whether to use SSL/TLS for the IMAP connection.
    - port (int): The port number for the IMAP connection.
    - verbose (bool): Indicates whether to print verbose output.
    - debug (bool): Indicates whether to print debug output.
    - skip (str): Comma-separated list of folders to skip during export.

    Returns:
    - None

    The function connects to the IMAP server using the provided credentials and iterates
    through each folder to export emails. It filters emails based on the specified year
    and skips folders specified in the 'skip' parameter. For each email, it saves the
    raw message and attachments to the destination folder.

    Example usage:
    ```
    export_emails("imap.example.com", "username", "password", "/path/to/destination", year=2023, use_ssl=True, verbose=True)
    ```
    """
    global VERBOSE, DEBUG
    VERBOSE = verbose
    DEBUG = debug

    stats = EmailStats()

    if use_ssl:
        if port:
            connection = imaplib.IMAP4_SSL(imap_server, port)
        else:
            connection = imaplib.IMAP4_SSL(imap_server)
    else:
        if port:
            connection = imaplib.IMAP4(imap_server, port)
        else:
            connection = imaplib.IMAP4(imap_server)

    if DEBUG:
        connection.debug = 4

    if VERBOSE:
        print("Logging in...")

    connection.login(username, password)

    if VERBOSE:
        print("Logged in successfully.")

    result, _ = connection.select()

    if result != "OK":
        print(f"Warning: Failed to select mailbox. Error: {result}")
        connection.close()
        connection.logout()
        exit(1)

    _, folders = connection.list()

    for folder_info in folders:
        stats.increment_folders()

        _, folder_name = folder_info.decode("utf-8").split('" "')
        folder_name = folder_name.strip('"')

        if VERBOSE:
            print("Select folder: " + folder_name)

        if folder_name in skip.split(","):
            continue

        connection.select(folder_name)

        try:
            _, message_ids = connection.search(None, "ALL")
        except imaplib.IMAP4.error as e:
            result, _ = connection.select()

            if result != "OK":
                print(
                    f"Warning: Failed to reselect mailbox after error. Error: {result}"
                )
                continue
            else:
                _, message_ids = connection.search(None, "ALL")

        message_ids = message_ids[0].split()

        for message_id in message_ids:
            stats.increment_messages()

            _, msg_data = connection.fetch(message_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            try:
                date_obj = parse_date(msg["Date"])
            except ValueError:
                print(
                    "Warning: Failed to parse date > "
                    + msg["Date"]
                    + " < Skipping this email."
                )
                exit(1)

            if date_obj and year and date_obj.year != year:
                continue

            stats.increment_matched_year_messages()
            sender_email = parse_sender_email(msg["From"])
            folder_path = mkdir_email_folder(
                destination, date_obj, date_obj.year, sender_email
            )
            subject = normalize_subject(msg["Subject"])
            save_message(raw_email, os.path.join(folder_path, f"{subject}.eml"))
            save_attachments(msg, folder_path)

    connection.close()
    connection.logout()
    stats.print_stats()


def run():
    parser = argparse.ArgumentParser(description="Export emails from an IMAP mailbox.")
    parser.add_argument("--server", "-s", required=True, help="IMAP server address")
    parser.add_argument("--user", "-u", required=True, help="Username")
    parser.add_argument("--password", "-p", required=True, help="Password")
    parser.add_argument("--destination", "-d", required=True, help="Export folder path")
    parser.add_argument(
        "--year", "-y", type=int, help="Optional: Year to filter emails"
    )
    parser.add_argument(
        "--ssl", action="store_true", help="Optional: Use SSL connection"
    )
    parser.add_argument("--port", type=int, help="Optional: Port of server")
    parser.add_argument(
        "--skip", help="Optional: Comma seperated list of imap folders to skip"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    parser.add_argument("--debug", action="store_true", help="Print debug output")

    args = parser.parse_args()

    export_emails(
        args.server,
        args.user,
        args.password,
        args.destination,
        args.year,
        args.ssl,
        args.port,
        args.verbose,
        args.debug,
        args.skip,
    )
