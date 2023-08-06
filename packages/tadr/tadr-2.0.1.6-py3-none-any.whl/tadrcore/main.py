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

from time import sleep
from .auth import init
from .globals import Globals
from .logger import Log
from .misc import check_message

global Globals, Log


def tadr() -> None:
    """The main program function.
    """
    Log.new(f"Running Auto Done Replier version {Globals.VERSION}.", "NOSCOPE")

    Log.new("Initialising Reddit instance...", "INFO")
    reddit = init()

    message_ids = []

    # Main program loop
    while True:

        # Fetch messages
        Log.new("Checking messages...", "INFO")
        for message in reddit.inbox.comment_replies(limit=Globals.LIMIT):

            # Main check, replying to message if necessary
            # The one second delay should ensure only 1 reply is ever needed
            if check_message(message, message_ids):
                Log.new(
                    f"Replying to message at: https://www.reddit.com{message.context}",
                    "INFO"
                )
                if Globals.VERBOSE:
                    Log.notify(f"Replying to message at: {message.id}")
                sleep(1)
                message.reply(Globals.REPLY)

        # Extra logs / functions depending on settings
        Log.new(f"Messages checked so far: \n{message_ids}", "DEBUG")
        if Globals.LOG_UPDATES:
            Log.new("Updating log...", "INFO")
            Log.output()
        Log.new(f"Finished checking messages, waiting {Globals.SLEEP} seconds.", "INFO")

        sleep(Globals.SLEEP)
