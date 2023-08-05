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
    Type,
    TypeVar,
    Awaitable

)

# pckages imports
import time
import asyncio
import threading
import json
import aiohttp
import requests
import websocket

# disspy imports
from .message import DisMessage
from .user import DisUser
from .channel import DisChannel
from .guild import DisGuild


class DisFlags:
    """
    The class for using intents in bots

    :methods:
        :method: default()
            Implements GUILD_MESSAGES and default intents
        :method: all()
            Implements all Gateway Intents
    """

    @staticmethod
    def default():
        return 512

    @staticmethod
    def all():
        """
            Implements:
                1.  GUILDS
                2.  GUILD_MEMBERS (Privileged intent)
                3.  GUILD_BANS
                4.  GUILD_EMOJIS_AND_STICKERS
                5.  GUILD_INTEGRATIONS
                6.  GUILD_WEBHOOKS
                7.  GUILD_INVITES
                8.  GUILD_VOICE_STATES
                9.  GUILD_PRESENCES (Privileged intent)
                10. GUILD_MESSAGES (Privileged intent)
                11. GUILD_MESSAGE_REACTIONS
                12. GUILD_MESSAGE_TYPING
                13. DIRECT_MESSAGES
                14. DIRECT_MESSAGE_REACTIONS
                15. DIRECT_MESSAGE_TYPING
                16. GUILD_SCHEDULED_EVENTS

            :return: int (integer value of intents)
        """
        return 98303


class JsonOutput(dict):
    _T = TypeVar("JsonOutput")

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    @property
    def __class__(self: _T) -> Type[_T]:
        return self._T


class Showflake:
    def __init__(self):
        print("Beta Message: Dont't use Showflake objects in your projects because it in dev!")


class _Rest:
    def __init__(self, token):
        self.token = token

    def _headers(self):
        return {'Authorization': f'Bot {self.token}'}

    def get(self, goal: str, id: int) -> JsonOutput:
        if goal.casefold() == 'guild':
            return JsonOutput(kwargs=requests.get(f'https://discord.com/api/v10/guilds/{str(id)}',
                              headers=self._headers()).json())

        elif goal.casefold() == 'channel':
            return JsonOutput(kwargs=requests.get(f'https://discord.com/api/v10/channels/{str(id)}',
                              headers=self._headers()).json())

        elif goal.casefold() == "user":
            return JsonOutput(kwargs=requests.get(f'https://discord.com/api/v10/users/{str(id)}',
                              headers=self._headers()).json())

    def fetch(self, channel_id, message_id) -> JsonOutput:
        _channel_id, _message_id = [str(channel_id), str(message_id)]
        _1part = "https://discord.com/api/v10/channels/"
        _2part = f"{_channel_id}/messages/{_message_id}"
        return JsonOutput(kwargs=requests.get(f"{_1part}{_2part}",
                          headers=self._headers()).json())

    async def send_message(self, channel_id, post):
        async with aiohttp.ClientSession() as s:
            await s.post(f'https://discord.com/api/v10/channels/{str(channel_id)}/messages', json=post,
                         headers=self._headers())


class _Gateway:
    def __init__(self, gateway_version: int, token: str, intents: int, activity: dict,
                 status: str, on_ready: Awaitable, on_messagec: Awaitable, register: Awaitable,
                 on_register: Awaitable):
        # Setting up connecting to Gateway
        self.gateway_version: int = gateway_version
        self.ws = websocket.WebSocket()
        self.intents = intents
        self.activity = activity
        self.status = status
        self.token = token
        self._rest = _Rest(token)

        self.on_ready = on_ready
        self.on_messagec = on_messagec
        self.register = register
        self.on_register = on_register

    def run(self):
        # Connecting to Gateway
        self.ws.connect(f"wss://gateway.discord.gg/?v={self.gateway_version}&encoding=json")

        # Parsing Opcode 10 Hello to Heartbeat Interval
        self.heartbeat_interval = self.get_responce()["d"]["heartbeat_interval"]

        # Setting up Opcode 1 Heartbeat
        heartbeat_thread = threading.Thread(target=self.heartbeat)
        heartbeat_thread.start()

        # Sending Opcode 2 Identify
        self.send_opcode_2()

        heartbeat_thread.join()

    def send_request(self, json_data):
        self.ws.send(json.dumps(json_data))

    def get_responce(self):
        responce = self.ws.recv()
        return json.loads(responce)

    async def register(self, d):
        return

    def on_ready(self):
        return

    def on_messagec(self, message: DisMessage):
        return

    def on_register(self):
        return

    def heartbeat(self):
        while True:
            self.heartbeat_events_create()

            time.sleep(self.heartbeat_interval / 1000)

    def heartbeat_events_create(self):
        self.send_opcode_1()
        event = self.get_responce()
        self._check(event)

    def send_opcode_1(self):
        self.send_request({"op": 1, "d": "null"})

    def send_opcode_2(self):
        self.send_request({"op": 2, "d": {"token": self.token,
                                          "properties": {"$os": "linux", "$browser": "dispy", "$device": "dispy"},
                                          "presence": {"activities": [self.activity],
                                                       "status": self.status, "since": 91879201, "afk": False},
                                          "intents": self.intents}})

    def _check(self, event: dict):
        if event["t"] == "READY":
            asyncio.run(self.register(event["d"]))
            asyncio.run(self.on_ready())
            asyncio.run(self.on_register())
            self.user_id = event["d"]["user"]["id"]

        if event["t"] == "MESSAGE_CREATE":
            if self._check_notbot(event):
                _message_id = int(event["d"]["id"])
                _channel_id = int(event["d"]["channel_id"])

                channel = DisChannel(_channel_id, self._rest)
                asyncio.run(self.on_messagec(channel.fetch(_message_id)))

    def _check_notbot(self, event: dict) -> bool:
        return self.user_id != event["d"]["author"]["id"]


class DisApi:
    def __init__(self, token):
        self.token = token

        self._g = None
        self._r = _Rest(self.token)

    def fetch(self, channel_id, id):
        return DisMessage(id, channel_id, DisApi(self.token))

    def run(self, gateway_version: int, intents: int, status, on_ready: Awaitable, on_messagec: Awaitable,
            on_register: Awaitable):
        if on_messagec is not None:
            self._on_message = on_messagec
        if on_ready is not None:
            self._on_ready = on_ready

        self._g = _Gateway(gateway_version, self.token, intents, {}, status, self._on_ready, self._on_message,
                           self._register, on_register)
        self._g.run()

    async def _on_message(self, message):
        pass

    async def _on_ready(self):
        pass

    async def _register(self, d):
        self.user: DisUser = self.get_user(d["user"]["id"], False)

    async def send_message(self, id, content, embed):
        if embed:
            await self._r.send_message(id, {"content": content, "embeds": [embed.tojson()]})
        else:
            await self._r.send_message(id, {"content": content})

    async def send_message(self, id, content, embeds):
        embeds_send_json = []
        if embeds:
            for e in embeds:
                embeds_send_json.append(e.tojson())

            await self._r.send_message(id, {"content": content, "embeds": embeds_send_json})
        else:
            await self._r.send_message(id, {"content": content})

    def get_user(self, id: int, premium_gets):
        return DisUser(id, self, premium_gets)

    def get_user_json(self, id: int) -> dict:
        return self._r.get("user", id)

    def get_guild_json(self, id: int) -> dict:
        return self._r.get("guild", id)

    def get_channel(self, id: int) -> DisChannel:
        return DisChannel(id, DisApi(self.token))

    def get_guild(self, id: int) -> DisGuild:
        """

        :param id: int
        """
        return DisGuild(id, self)
