import argparse

from main import export_emails


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
