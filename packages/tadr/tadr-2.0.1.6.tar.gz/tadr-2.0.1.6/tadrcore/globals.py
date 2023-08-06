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

from os import environ, makedirs
from os.path import expanduser, isdir
from sys import platform
from time import time
from typing import Dict

global Globals, VERSION
VERSION = "2.0.1.6"


class Static:
    """Class containing all static variables and config options.

    Attributes;
        - AUTHORS (list); list of users to reply to.
        - LIMIT (int); the number of messages to look back through.
        - LOG_UPDATES (boolean); whether or not to output log details to a file.
        - MESSAGES (list); list of phrases to reply to.
        - OS (str); the user's operating system.
        - PATHS (dictionary); the locations of the data and config folders.
        - REPLY (string); the message to reply with.
        - SLEEP (int); the number of seconds to wait between checks.
        - SPLITTER (str); the character to split messages by when searching.
        - START_TIME (int); the unix timestamp at which the program started running.
        - VERBOSE (boolean); whether or not to send desktop notifications when replying.
        - VERSION (str); the version number of TADR.

    Methods;
        - define_paths(str, str) -> Dict[str, str]; defines the locations of the data
        and config folders.
    """
    def __init__(self) -> None:
        self.AUTHORS = ["transcribersofreddit"]
        self.LIMIT = 10
        self.LOG_UPDATES = True
        self.MESSAGES = ["⛔ Sorry, I **can't find** your transcription on the post"]
        self.OS = platform
        self.PATHS = self.define_paths(expanduser("~"), self.OS)
        self.REPLY = (
            "done -- this was an automated action; please contact me with any"
            " questions."
        )
        self.SLEEP = 10
        self.SPLITTER = "."
        self.START_TIME = time()
        self.VERBOSE = True
        self.VERSION = VERSION

    def define_paths(self, home: str, os: str) -> Dict[str, str]:
        """Detects OS and defines the appropriate save paths for the config and data.
        Exits on detecting an unspported OS. Supported OS's are: Linux, MacOS, Windows.

        :param home:  The path to the user's home folder.
        :param os:    The user's operating system.
        :return: A string dictionary containing the newly defined save paths.
        """
        os = "".join(list(os)[:3])

        # Route for a supported operating system
        if os in ["dar", "lin", "win"]:

            paths = (
                {
                    "config": environ["APPDATA"] + "\\tadr",
                    "data": environ["APPDATA"] + "\\tadr\data"
                } if os == "win" else {
                    "config": f"{home}/.config/tadr",
                    "data": f"{home}/.tadr/data"
                }
            )

            # Create any missing paths/directories
            for path in paths:
                if not isdir(paths[path]):
                    print(f"DEBUG: Making path: {paths[path]}")
                    makedirs(path, exist_ok=True)
            return paths

        # Exit if the operating system is unsupported
        else:
            print(f"FATAL: Unsupported operating system: {os}, exiting.")
            exit()


Globals = Static()