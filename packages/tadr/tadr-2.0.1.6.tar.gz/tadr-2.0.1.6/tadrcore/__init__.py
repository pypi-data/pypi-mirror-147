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

# Authentication
from .auth import check_failure
from .auth import init
from .auth import login
from .auth import receive_connection
from .auth import send_message

# Credentials
from .creds import add_refresh_token
from .creds import create_credentials
from .creds import dump_credentials
from .creds import get_credentials

# Globals
from .globals import Static, Globals

# Logger
from .logger import Log, LogEntry, Logger

# Main
from .main import tadr

# Misc
from .misc import check_message
