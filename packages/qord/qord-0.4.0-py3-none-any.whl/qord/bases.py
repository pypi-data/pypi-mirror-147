# MIT License

# Copyright (c) 2022 Izhar Ahmad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from qord.models.messages import Message
from qord.internal.undefined import UNDEFINED
from qord.internal.helpers import compute_snowflake
from qord.internal.context_managers import TypingContextManager

from abc import ABC, abstractmethod
from datetime import datetime
import typing

if typing.TYPE_CHECKING:
    from qord.dataclasses.allowed_mentions import AllowedMentions
    from qord.dataclasses.embeds import Embed
    from qord.dataclasses.files import File
    from qord.dataclasses.message_reference import MessageReference
    from qord.flags.messages import MessageFlags
    from qord.core.rest import RestClient


__all__ = (
    "BaseMessageChannel",
)


class BaseMessageChannel(ABC):
    """A base class that implements support for messages managament.

    Almost all classes that support the :class:`Message` related operations
    inherit this class. The most common example is :class:`TextChannel`.
    """
    _rest: RestClient

    @abstractmethod
    async def _get_message_channel(self) -> typing.Any:
        raise NotImplementedError

    async def fetch_message(self, message_id: int) -> Message:
        """Fetches a :class:`Message` from the provided message ID.

        Parameters
        ----------
        message_id: :class:`builtins.int`
            The ID of message to fetch.

        Returns
        -------
        :class:`Message`
            The fetched message.

        Raises
        ------
        HTTPNotFound
            Invalid or unknown message ID passed. Message might be deleted.
        HTTPForbidden
            Missing permissions to fetch that message.
        HTTPException
            The fetching failed.
        """
        channel = await self._get_message_channel()
        data = await self._rest.get_message(channel_id=channel.id, message_id=message_id)
        return Message(data, channel=channel)

    async def fetch_pins(self) -> typing.List[Message]:
        """Fetches the messages that are currently pinned in the channel.

        Returns
        -------
        List[:class:`Message`]
            The pinned messages in the channel.

        Raises
        ------
        HTTPForbidden
            Missing permissions to fetch the pins.
        HTTPException
            The fetching failed.
        """
        channel = await self._get_message_channel()
        data = await self._rest.get_pinned_messages(channel_id=channel.id)
        return [Message(item, channel=channel) for item in data]

    async def messages(
        self,
        limit: typing.Optional[int] = 100,
        after: typing.Union[datetime, int] = UNDEFINED,
        before: typing.Union[datetime, int] = UNDEFINED,
        around: typing.Union[datetime, int] = UNDEFINED,
        oldest_first: bool = False,
    ) -> typing.AsyncIterator[Message]:
        """An async iterator for iterating through the channel's messages.

        Requires the :attr:`~Permissions.read_message_history` permission as
        well as :attr:`~Permissions.view_channels` permission in the given channel.

        ``after``, ``before``, ``around`` and ``oldest_first`` are all mutually
        exclusive parameters.

        Parameters
        ----------
        limit: Optional[:class:`builtins.int`]
            The number of messages to fetch. If ``None`` is given, All
            messages are fetched from the channel. Defaults to ``100``.
        after: Union[:class:`datetime.datetime`, :class:`builtins.int`]
            For pagination, To fetch messages after this message ID or time.
        before: Union[:class:`datetime.datetime`, :class:`builtins.int`]
            For pagination, To fetch messages before this message ID or time.
        around: Union[:class:`datetime.datetime`, :class:`builtins.int`]
            For pagination, To fetch messages around this message ID or time.
            Requires the limit to be greater than ``100``.
        oldest_first: :class:`builtins.bool`
            Whether to fetch the messages in reversed order i.e
            oldest message to newer messages.

        Yields
        ------
        :class:`Message`
            The message from the channel.
        """
        channel = await self._get_message_channel()

        if any((
            before and after,
            before and around,
            after and around,
        )):
            raise TypeError("around, before and after are mutually exclusive.")

        if oldest_first:
            after = 0
            before = UNDEFINED
            around = UNDEFINED

        if isinstance(after, datetime):
            after = compute_snowflake(after)
        if isinstance(before, datetime):
            before = compute_snowflake(before)
        if isinstance(around, datetime):
            around = compute_snowflake(around)

        while limit is None or limit > 0:
            if limit is None:
                current_limit = 100
            else:
                current_limit = min(limit, 100)

            data = await self._rest.get_messages(
                channel.id,
                limit=current_limit,
                after=after,
                before=before,
                around=around,
            )

            if limit is not None:
                limit -= current_limit

            if not data:
                break

            if oldest_first:
                data.reverse()
                after = int(data[-1]["id"])
            else:
                before = int(data[-1]["id"])

            for m in data:
                yield Message(m, channel=channel)

    # TODO: Add the remaining fields support here.
    async def send(
        self,
        content: str = UNDEFINED,
        *,
        tts: bool = UNDEFINED,
        allowed_mentions: AllowedMentions = UNDEFINED,
        message_reference: MessageReference = UNDEFINED,
        flags: MessageFlags = UNDEFINED,
        embed: Embed = UNDEFINED,
        file: File = UNDEFINED,
        embeds: typing.List[Embed] = UNDEFINED,
        files: typing.List[File] = UNDEFINED,
    ):
        """Sends a message to the channel.

        If channel is a text based guild channel, This requires the
        :attr:`~Permissions.send_messages` permission in the channel.

        For direct messages channel, No specific permission is required
        however relevant user must share a guild with the bot and the bot
        must not be blocked by the user.

        Parameters
        ----------
        content: :class:`builtins.str`
            The content of message.
        allowed_mentions: :class:`AllowedMentions`
            The mentions to allow in the message's content.
        flags: :class:`MessageFlags`
            The message flags for the sent message. Bots can only
            apply the :attr:`~MessageFlags.suppress_embeds` flag.
            Other flags are unsupported.
        embed: :class:`Embed`
            The embed to include in message, cannot be mixed with ``embeds``.
        embeds: List[:class:`Embed`]
            The list of embeds to include in the message, cannot be mixed with ``embed``.
        file: :class:`File`
            The file to include in message, cannot be mixed with ``files``.
        files: List[:class:`File`]
            The list of file attachments to send in message, cannot be mixed with ``file``.
        tts: :class:`builtins.bool`
            Whether the sent message is a Text-To-Speech message.

        Returns
        -------
        :class:`Message`
            The message that was sent.

        Raises
        ------
        TypeError
            Invalid arguments passed.
        HTTPForbidden
            You are not allowed to send message in this channel.
        HTTPBadRequest
            The message has invalid data.
        HTTPException
            The sending failed for some reason.
        """
        if embed is not UNDEFINED and embeds is not UNDEFINED:
            raise TypeError("embed and embeds parameters cannot be mixed.")

        if file is not UNDEFINED and files is not UNDEFINED:
            raise TypeError("file and files parameters cannot be mixed.")

        json = {}

        if content is not UNDEFINED:
            json["content"] = content

        if tts is not UNDEFINED:
            json["tts"] = tts

        if flags is not UNDEFINED:
            json["flags"] = flags.value

        if allowed_mentions is not UNDEFINED:
            json["allowed_mentions"] = allowed_mentions.to_dict()

        if message_reference is not UNDEFINED:
            json["message_reference"] = message_reference.to_dict()

        if file is not UNDEFINED:
            files = [file]

        if embed is not UNDEFINED:
            if embed is None:
                json["embeds"] = []
            else:
                json["embeds"] = [embed.to_dict()]

        if embeds is not UNDEFINED:
            if embeds is None:
                json["embeds"] = []
            else:
                json["embeds"] = [embed.to_dict() for embed in embeds]

        channel = await self._get_message_channel()
        data = await self._rest.send_message(
            channel_id=channel.id,
            json=json,
            files=files,
        )
        return Message(data, channel=channel)

    async def trigger_typing(self) -> None:
        """Triggers the typing indicator in the channel.

        The typing indicator would automatically disappear after few seconds
        or once a message is sent in the channel.

        .. tip::
            Consider using :meth:`.typing` for a convenient context manager interface
            for triggering typing indicators.

        Raises
        ------
        HTTPException
            Triggering typing failed.
        """
        channel = await self._get_message_channel()
        await self._rest.trigger_typing(channel_id=channel.id)

    def typing(self) -> TypingContextManager:
        """Returns a context manager interface for triggering typing indicator in a channel.

        Example::

            async with channel.typing():
                # Typing indicator will appear until the context manager
                # is entered. Perform something heavy in this clause
                ...
        """
        return TypingContextManager(channel=self)
