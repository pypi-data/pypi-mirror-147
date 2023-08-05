"""
MIT License

Copyright (c) 2022 itttgg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Imports
from .client import DisBot, DisBotStatus
from .errs import UserNitroTypeError, InternetError, BotPrefixError, MissingPerms, InvalidArgument, BotEventTypeError, BotStatusError
from .guild import DisGuild
from .channel import DisChannel
from .embed import DisEmbed, DisField, DisColor
from .message import DisMessage
from .user import DisUser
from .core import DisApi, DisFlags, JsonOutput, Showflake
from .types import DisBotEventType, DisBotStatus
from .logger import Logger

"""
    Main information about dispy
    
    :var: __version__ -> Version of dipsy
    :var: __github__ -> Link to github repo
    :var: __packagename__ -> Name of package 
"""

__version__ = "0.1dev"
__minpythonver__ = "3.6"
__github__ = "https://github.com/itttgg/dispy"
__stablever__ = "https://github.com/itttgg/dispy/releases/tag/0.1a2"
__description__ = "Dispy - package for creating bots."
__packagename__ = "dispy"
