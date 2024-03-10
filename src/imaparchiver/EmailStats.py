import time


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
