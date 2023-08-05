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

# Typing imports
from typing import (
    Optional,
    TypeVar,
    Union,
    Type
)

# Package imports
from disspy import errs
from disspy.core import DisApi, DisFlags
from disspy.channel import DisChannel
from disspy.embed import DisEmbed
from disspy.guild import DisGuild
from disspy.user import DisUser
from disspy.types import DisBotStatus, DisBotEventType
from disspy.logger import Logger


System = {
    bool: bool
}


class _BaseBot:
    _T = TypeVar("_BaseBot")

    def __init__(self, token: str):
        self.token = token

    @property
    def __class__(self) -> Type[_T]:
        """
            Returns type of this class
            --------
            :return self._T (Type of class):
        """
        return self._T


class DisBot(_BaseBot):
    """
    Class for accessing and sending information in Discord

    Attributes:
        :var token: Token for accessing and sending info (Token from Discord Developer Portal).
        :var flags: Flags (Intents) for bot.
    """
    _T = TypeVar("DisBot")
    __parent__ = TypeVar("_BaseBot")

    def __init__(self, token: str, status: Optional[str] = None,
                 flags: Optional[Union[int, DisFlags]] = None):
        """
        Create bot

        :param token: Discord Developers Portal Bot Token
        :param status: Status that use in run()
        :param flags: Flags (Intents) for bot (default is 512)
        """

        super().__init__(token)

        if flags is None:
            self.intflags = DisFlags.default()
        else:
            self.intflags = flags

        self.status = status

        self._on_messagec = None
        self._on_ready = None

        self.user = None

        self._api = DisApi(token)

        self.isready = False

        self.logger = Logger()
        self.__classname__ = "DisBot"

        self.__slots__ = [self._api, self._on_ready, self._on_messagec, self.token,
                          self.user, self.isready, self.status]

    @property
    def __class__(self) -> Type[_T]:
        """
            Returns type of this class
            --------
            :return self._T (Type of class):
        """
        return self._T

    async def _on_register(self):
        self.user: DisUser = self._api.user

    def on(self, type: Union[DisBotEventType, str]):
        """
        This method was created for changing on_ready and on_message method that using in runner

        :param type: Type of event
        :return: None (wrapper)
        """

        __methodname__ = f"{self.__classname__}.on()"

        if isinstance(type, DisBotEventType):
            self.logger.log(f"Error! In method {__methodname__} was moved invalid argument! Argument type is DisBotEventType, but in method have to type is str!")

        def wrapper(func):
            if type == "messagec":
                self._on_messagec = func
            elif type == "ready":
                self._on_ready = func
            else:
                self.logger.log(f"Error! In method {__methodname__} was moved invalid event type!")
                raise errs.BotEventTypeError("Invalid type of event!")

        return wrapper

    def run(self, status: Union[DisBotStatus, str] = None):
        """
        Running bot

        :param status: Status for bot user
        :return: None
        """
        __methodname__ = f"{self.__classname__}.on()"

        if isinstance(status, DisBotStatus):
            self.logger.log(f"Error! In method {__methodname__} was moved invalid argument! Argument type is DisBotStatus, but in method have to type is str!")
            raise errs.InvalidArgument("Invalid argument type!")

        self.isready = True

        if status is None and self.status is None:
            self.status = "online"
        elif status is not None and self.status is None:
            self.status = status
        elif status is not None and self.status is not None:
            raise errs.BotStatusError("You typed status and in run() and in __init__()")

        self._runner(self.status, 10)

    def _runner(self, status, version: int) -> None:
        self._api.run(version, self.intflags, status, self._on_ready, self._on_messagec, self._on_register)

        return 0  # No errors

    def disconnect(self):
        self._dissconnenter()

    def close(self):
        self._dissconnenter()

    def _dissconnenter(self):
        for _var in self.__slots__:
            del _var

    async def send(self, channel_id: int, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None):
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embeds=embeds)
        else:
            raise errs.InternetError("Bot is not ready!")

    async def send(self, channel_id: int, content: Optional[str] = None, embed: Optional[DisEmbed] = None):
        if self.isready:
            channel = self.get_channel(channel_id)
            await channel.send(content=content, embed=embed)
        else:
            raise errs.InternetError("Bot is not ready!")

    def get_channel(self, id: int) -> DisChannel:
        return self._api.get_channel(id)

    def get_guild(self, id: int) -> DisGuild:
        return self._api.get_guild(id)

    def get_user(self, id: int, premium_gets: System[bool] = True) -> DisUser:
        return self._api.get_user(id, premium_gets)
