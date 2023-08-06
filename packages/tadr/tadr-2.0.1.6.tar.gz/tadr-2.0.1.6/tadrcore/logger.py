"""
    Copyright (C) 2021-present, Murdo B. Maclachlan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.

    Contact me at murdomaclachlan@duck.com
"""

from datetime import datetime
from gi import require_version
require_version("Notify", "0.7")
from gi.repository import Notify
from gi.repository.GLib import GError
from time import time
from typing import List, Union
from .globals import Globals

global Globals


class Logger:
    """Class for controlling the entirety of logging. The logging works on a scope-based
    system where (almost) every message has a defined scope, and the scopes are each
    associated with a specific value between 0 and 2 inclusive. The meanings of the
    values are as follows:

    - 0: disabled, do not print to console or save to log file
    - 1: enabled, print to console but do not save to log file
    - 2: maximum, print to console and save to log file

    Attributes;
        - log (hidden, list): contains all log entries, each one an instance of LogEntry
        - scopes (hidde, dictionary): contains all scopes and their associated values

    Methods;
        - get(str, str) -> Union[List[str], str]: get entries from the log
    """
    def __init__(
        self: object,
        debug=0, error=2, fatal=2, info=1, warning=2
    ) -> None:
        self.__log = []
        self.__notify = Notify
        self.__notify.init("Clone Finder")
        self.__scopes = {
            "DEBUG":   debug,   # information for debugging the program
            "ERROR":   error,   # errors the program can recover from
            "FATAL":   fatal,   # errors that mean the program cannot continue
            "INFO":    info,    # general information for the user
            "WARNING": warning  # things that could cause errors later on
        }

    def get(
            self: object,
            mode: str = "all", scope: str = None
        ) -> Union[List[str], str]:
        """Returns item(s) in the log. What entries are returned can be controlled by
        passing optional arguments.

        :param mode: Optional; 'all' or 'recent'
        :param scope: Optional; if passed, oly entries with matching scope will be returned.
        :return: a single log entry, list of log entries, or an empty string on a failure.
        """
        if scope is None:
            # Tuple indexing provides a succint way to determine what to return
            return (self.__log, self.__log[len(self.__log)-1])[mode == "recent"]
        else:
            # Return all log entries with a matching scope
            if mode == "all":
                data = []
                for i in self.__log:
                    if i.scope == scope:
                        data.append(i)
                # Allows us to return an empty string to indicate failure if no entries
                # were found
                return data if len(data) > 0 else ""
            # Return the most recent log entry with a matching scope; for this purpose,
            # we reverse the list then iterate through it.
            elif mode == "recent":
                for i in self.__log.reverse():
                    if i.scope == scope:
                        return self.__log[i]
                return ""
            else:
                self.new("Unknown mode passed to Logger.get().", "WARNING")
                return ""

    def get_time(self: object, method: str = "time") -> str:
        """Gets the current time and parses it to a human-readable format.

        :param method: The method to calculate the timestamp; either 'time' or 'date'.
        :return: a single date string in either format 'YYYY-MM-DD HH:MM:SS', or format
                 'YYYY-MM-DD'
        """
        if method == "time":
            return datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")
        elif method == "date":
            return datetime.fromtimestamp(time()).strftime("%Y-%m-%d")
        else:
            print("ERROR: Bad method passed to Logger.get_time().")

    def notify(self: object, message: str) -> None:
        """Display a desktop notification with a given message.

        This method implements a try-except to catch a GError I've been experiencing
        recently and can't find the cause of. Something in GLib seems to crash whenever
        I display a notification with a Python notification library, despite the fact
        that the notification goes through successfully anyway. Since it has no bearing
        on the program function, this code ignores the error.

        :param message: The message to display in the notification.
        """
        try:
            self.__notify.Notification.new(message).show()
        except GError:
            pass

    def new(
            self: object,
            message: str, scope: str, do_not_print: bool = False
        ) -> bool:
        """Initiates a new log entry and prints it to the console. Optionally, if
        do_not_print is passed as True, it will only save the log and will not print
        anything (unless the scope is 'NOSCOPE'; these messages are always printed).

        :param message:       The messaage to log.
        :param scope:         The scope of the message (e.g. debug, error, info).
        :param do_not_print:  Optional; False by default.
        :return: boolean success status.
        """
        if scope in self.__scopes or scope == "NOSCOPE":
            # Create and save the log entry
            entry = LogEntry(message, scope, self.get_time())
            self.__log.append(entry)
            # A select few messages have no listed scope and should always be printed
            if scope == "NOSCOPE":
                print(entry.rendered)
                return True
            # If the scope's value is 1 or greater it should be printed
            elif self.__scopes[scope]:
                print(entry.rendered if not do_not_print else None)
                return True
        else:
            self.new("Unknown scope passed to Logger.new()", "WARNING")
        return False

    def output(self: object) -> None:
        """Write all log entries with scopes set to save to a log file in a data folder
        in the working directory, creating the folder and file if they do not exist.
        The log files are marked with the date, so each new day, a new file will be
        created.
        """
        with open(
            f"{Globals.PATHS['data']}/log-{self.get_time(method='date')}.txt", "at+"
        ) as log_file:
            for line in self.__log:
                try:
                    if self.__scopes[line.scope] == 2:
                        log_file.write(line.rendered + "\n")
                except KeyError:
                    pass


class LogEntry:
    """Represents a single entry within the log, storing its timestamp, scope and
    message. This makes it easier to select certain log entries using the
    Logger.get() method.

    Attributes:
    - message (str): the information conveyed by the entry
    - scope (str): the scope of the entry
    - timestamp (str): the formatted time at which the entry was created
    - rendered (str): the full rendered message that will be printed to the user or
                      saved to the log file
    """
    def __init__(self: object, message: str, scope: str, timestamp: str):
        self.message = message
        self.scope = scope
        self.timestamp = timestamp
        self.rendered = (
            f"[{timestamp}] {scope}: {message}"
            if scope != "NOSCOPE" else
            f"{message}"
        )


global Log
Log = Logger()
