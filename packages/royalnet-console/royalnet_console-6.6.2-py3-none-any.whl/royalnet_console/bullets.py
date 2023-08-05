"""
:class:`royalnet.engineer.proj.Bullet`\\ s for the :mod:`royalnet_console` frontend.
"""

from __future__ import annotations

import datetime
import getpass
import logging
import os

import async_property as ap
import click
import psutil
import royalnet.engineer as engi
import royalnet.royaltyping as t

log = logging.getLogger(__name__)


# Code
async def console_message(*,
                          text: str = None,
                          files: t.List[t.BinaryIO] = None) -> engi.Message:
    """
    Output text to the console and return the corresponding :class:`~.engi.Message`.

    :param text: The text of the message.
    :param files: A :class:`list` of files to attach to the message.
    :return: The sent :class:`.engi.Message`.
    """
    if files is None:
        files = []

    if len(files) > 0:
        raise engi.NotSupportedError("Console does not allow sending files.")

    log.debug("Sending message...")
    click.echo(text)

    log.debug("Creating message...")
    return ConsoleMessage(_text=text)


class ConsoleUser(engi.User):
    def __hash__(self) -> int:
        return os.getuid()

    @ap.async_property
    async def name(self) -> str:
        return getpass.getuser()

    async def slide(self) -> "engi.Channel":
        return ConsoleChannel()


class ConsoleChannel(engi.Channel):
    def __hash__(self) -> int:
        return os.getpid()

    @ap.async_property
    async def name(self) -> str:
        return psutil.Process(os.getpid()).name()

    @ap.async_property
    async def users(self) -> t.List[engi.User]:
        return [ConsoleUser()]

    async def send_message(self, *,
                           text: str = None,
                           files: t.List[t.BinaryIO] = None) -> engi.Message:
        return await console_message(text=text, files=files)


class ConsoleMessage(engi.Message):
    _instance_count: int = 0

    def __init__(self, _text: str, _timestamp: datetime.datetime = None):
        super().__init__()
        self._text: str = _text
        self._timestamp: datetime.datetime = _timestamp or datetime.datetime.now()
        self._instance_number: int = self._instance_count
        self._instance_count += 1

    def __hash__(self) -> int:
        return self._instance_number

    @ap.async_property
    async def text(self) -> str:
        return self._text

    @ap.async_property
    async def timestamp(self) -> datetime.datetime:
        return self._timestamp

    @ap.async_property
    async def channel(self) -> engi.Channel:
        return ConsoleChannel()

    async def reply(self, *,
                    text: str = None,
                    files: t.List[t.BinaryIO] = None) -> engi.Message:
        return await console_message(text=text, files=files)


class ConsoleMessageReceived(engi.MessageReceived):
    _instance_count: int = 0

    def __init__(self, _text: str, _timestamp: datetime.datetime = None):
        super().__init__()
        self._msg: ConsoleMessage = ConsoleMessage(_text=_text, _timestamp=_timestamp)
        self._instance_number: int = self._instance_count
        self._instance_count += 1

    def __hash__(self):
        return

    @ap.async_property
    async def message(self) -> ConsoleMessage:
        return self._msg


__all__ = (
    "ConsoleUser",
    "ConsoleChannel",
    "ConsoleMessage",
    "ConsoleMessageReceived",
)
