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

from qord.exceptions import (
    ClientSetupRequired,
    HTTPBadRequest,
    HTTPException,
    HTTPForbidden,
    HTTPNotFound,
    HTTPServerError,
)
from qord.project_info import __version__, __github__
from qord.core.ratelimits import Route, RatelimitHandler
from qord.internal.undefined import UNDEFINED

import aiohttp
import asyncio
import logging
import typing
import json as _json

if typing.TYPE_CHECKING:
    from qord.dataclasses.files import File

__all__ = (
    "RestClient",
)

_LOGGER = logging.getLogger(__name__)
_RATELIMIT_HIT_WARNING = "A ratelimit has been hit! Retrying this request after the delay of {retry_after}s."
_RATELIMIT_CLEAR_INFO  = "The ratelimit has been cleared, retrying the request now."
_GLOBAL_RATELIMIT_HIT_WARNING = "The global ratelimit has been hit! Further HTTP requests would " \
                                "be blocked for next {retry_after}s." # type: ignore
_GLOBAL_RATELIMIT_CLEAR_INFO  = "The global ratelimit is cleared. HTTP requests will not be blocked anymore."
_RATELIMIT_BUCKET_EXHAUSTED_DEBUG = "Requests limit has been reached for route {path!r}, " \
                                    "delaying further requests for {retry_after}s" # type: ignore


async def _release_lock(lock: asyncio.Lock, delay: float) -> None:
    await asyncio.sleep(delay)
    lock.release()


class RestClient:
    """REST handling implementation including ratelimits prevention and handling."""

    def __init__(self, *,
        session: typing.Optional[aiohttp.ClientSession] = None,
        session_owner: bool = True,
        max_retries: int = 5,
    ) -> None:

        if session and not isinstance(session, aiohttp.ClientSession):
            raise TypeError(f"Parameter 'session' must be an instance of aiohttp.ClientSession " \
                            f"object, Not {session.__class__!r}") # type: ignore

        if max_retries is None or max_retries == 0:
            max_retries = 1

        if not isinstance(max_retries, int) or max_retries > 5:
            raise TypeError(f"Parameter 'max_retries' must be an integer less than 5. " \
                            f"{max_retries!r} is not valid.") # type: ignore

        self.session = session
        self.session_owner: bool = session_owner
        self.ratelimit_handler = RatelimitHandler()
        self.token: typing.Optional[str] = None
        self.max_retries = max_retries or 5

    def _ensure_session(self) -> aiohttp.ClientSession:
        session = self.session

        if session and not session.closed:
            return session

        self.session = aiohttp.ClientSession()
        return self.session

    async def _resolve_response(self, response):
        if response.headers["Content-Type"] == "application/json":
            data = await response.json()
        else:
            data = await response.text()

        return data

    async def request(self, route: Route, reason: typing.Optional[str] = None, **options: typing.Any) -> typing.Any:
        session = self._ensure_session()

        token = self.token
        requires_auth = route.requires_auth
        path = route.path
        rl_path = route.ratelimit_path

        if requires_auth and token is None:
            raise ClientSetupRequired("No bot token is set yet to perform this request. " \
                                      "Client is not setup yet.") # type: ignore

        headers = options.pop("headers", dict())

        headers["User-Agent"] = f"DiscordBot ({__github__}, {__version__})"

        if requires_auth:
            headers["Authorization"] = f"Bot {token}"
        if reason is not None:
            headers["X-Audit-Log-Reason"] = reason

        handler = self.ratelimit_handler
        unlock = True
        lock = handler.get_lock(rl_path)

        await handler.wait_until_global_reset()
        await lock.acquire()

        for _ in range(self.max_retries):
            try:
                async with session.request(
                    route.method,
                    route.url,
                    headers=headers,
                    **options
                ) as response:

                    status = response.status
                    response_headers = response.headers

                    remaining = response_headers.get("X-Ratelimit-Remaining")
                    bucket = response_headers.get("X-Ratelimit-Bucket")

                    if bucket is not None:
                        # Store the bucket hash for this route.
                        handler.set_bucket(rl_path, bucket)

                    if remaining == "0" and status != 429:
                        # This header is always present in this case.
                        retry_after = float(response_headers["X-Ratelimit-Reset-After"])
                        msg = _RATELIMIT_BUCKET_EXHAUSTED_DEBUG.format(
                            path=path,
                            retry_after=retry_after
                        )
                        unlock = False # Prevent lock from releasing
                        _LOGGER.debug(msg)

                        coro = _release_lock(lock, retry_after)
                        asyncio.create_task(coro)

                    if status == 204:
                        # 204 *No Content*
                        return None

                    data = await self._resolve_response(response)

                    if status < 300:
                        return data

                    elif status == 429:
                        if response_headers.get("Via") is None:
                            # Missing the `Via` header usually indicates a CF ban.
                            raise HTTPException(response, data)

                        # data is always a valid JSON here.
                        retry_after = float(data["retry_after"]) # type: ignore
                        is_global = data.get("global", False) # type: ignore

                        if is_global:
                            msg = _GLOBAL_RATELIMIT_HIT_WARNING.format(retry_after=retry_after)
                            handler.set_global()
                        else:
                            msg = _RATELIMIT_HIT_WARNING.format(retry_after=retry_after)

                        _LOGGER.critical(msg)
                        await asyncio.sleep(retry_after)

                        if is_global:
                            msg = _GLOBAL_RATELIMIT_CLEAR_INFO
                            handler.reset_global()
                        else:
                            msg = _RATELIMIT_CLEAR_INFO

                        _LOGGER.info(msg)
                        continue

                    elif status == 400:
                        raise HTTPBadRequest(response, data)

                    elif status == 403:
                        raise HTTPForbidden(response, data)

                    elif status == 404:
                        raise HTTPNotFound(response, data)

                    elif status >= 500:
                        raise HTTPServerError(response, data)

                    # unhandleable status code, raise it.
                    raise HTTPException(response, data)
            finally:
                if unlock and lock is not None:
                    if lock.locked():
                        lock.release()

    async def close(self):
        if not self.session_owner and self.session is not None:
            await self.session.close()

        self.ratelimit_handler.clear()

    # ----- Gateway -----

    async def get_gateway(self):
        route = Route("GET", "/gateway", requires_auth=False)
        data = await self.request(route)
        return data

    async def get_bot_gateway(self):
        route = Route("GET", "/gateway/bot", requires_auth=True)
        data = await self.request(route)
        return data

    # ----- Users -----

    async def get_current_user(self):
        route = Route("GET", "/users/@me")
        data = await self.request(route)
        return data

    async def edit_current_user(self, json: typing.Dict[str, typing.Any]):
        route = Route("PATCH", "/users/@me")
        data = await self.request(route, json=json)
        return data

    async def get_user(self, user_id: int):
        route = Route("GET", "/users/{user_id}", user_id=user_id)
        data = await self.request(route)
        return data

    async def create_dm(self, recipient_id: int):
        route = Route("POST", "/users/@me/channels")
        json = {"recipient_id": recipient_id}
        data = await self.request(route, json=json)
        return data

    # ---- Guilds ----

    async def get_guild(self, guild_id: int, with_counts: bool = False):
        params = {"with_counts": int(with_counts)}
        route = Route("GET", "/guilds/{guild_id}", guild_id=guild_id)
        data = await self.request(route, params=params)
        return data

    async def leave_guild(self, guild_id: int):
        route = Route("DELETE", "/users/@me/guilds/{guild_id}", guild_id=guild_id)
        await self.request(route)

    # ---- Guilds Roles ----

    async def get_roles(self, guild_id: int):
        route = Route("GET", "/guilds/{guild_id}/roles", guild_id=guild_id)
        data = await self.request(route)
        return data

    async def create_role(self, guild_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("POST", "/guilds/{guild_id}/roles", guild_id=guild_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def edit_role_positions(self, guild_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("PATCH", "/guilds/{guild_id}/roles", guild_id=guild_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def edit_role(self, guild_id: int, role_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route(
            "PATCH", "/guilds/{guild_id}/roles/{role_id}",
            guild_id=guild_id, role_id=role_id
        )
        data = await self.request(route, json=json, reason=reason)
        return data

    async def delete_role(self, guild_id: int, role_id: int, reason: typing.Optional[str] = None):
        route =  Route(
            "DELETE", "/guilds/{guild_id}/roles/{role_id}",
            guild_id=guild_id, role_id=role_id
        )
        await self.request(route, reason=reason)

    # ---- Members ---- #

    async def get_guild_member(self, guild_id: int, user_id: int):
        route = Route(
            "GET", "/guilds/{guild_id}/members/{user_id}",
            guild_id=guild_id, user_id=user_id
        )
        data = await self.request(route)
        return data

    async def get_guild_members(self, guild_id: int, limit: int = UNDEFINED, after: int = UNDEFINED):
        route = Route("GET", "/guilds/{guild_id}/members", guild_id=guild_id)

        params = {}

        if limit is not UNDEFINED:
            params["limit"] = limit

        if after is not UNDEFINED:
            params["after"] = after

        data = await self.request(route, params=params)
        return data

    async def search_guild_members(self, guild_id: int, params: typing.Dict[str, typing.Any]):
        route = Route("GET", "/guilds/{guild_id}/members/search", guild_id=guild_id)
        data = await self.request(route, params=params)
        return data

    async def edit_guild_member(
        self,
        guild_id: int,
        user_id: int,
        json: typing.Dict[str, typing.Any],
        reason: typing.Optional[str] = None
    ):
        route = Route("PATCH", "/guilds/{guild_id}/members/{user_id}", guild_id=guild_id, user_id=user_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def edit_client_guild_member(
        self,
        guild_id: int,
        json: typing.Dict[str, typing.Any],
        reason: typing.Optional[str] = None
    ):
        route = Route("PATCH", "/guilds/{guild_id}/members/@me", guild_id=guild_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def add_guild_member_role(
        self,
        guild_id: int,
        user_id: int,
        role_id: int,
        reason: typing.Optional[str] = None
    ):
        route = Route(
            "PUT", "/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            guild_id=guild_id, user_id=user_id, role_id=role_id
        )
        data = await self.request(route, reason=reason)
        return data

    async def remove_guild_member_role(
        self,
        guild_id: int,
        user_id: int,
        role_id: int,
        reason: typing.Optional[str] = None
    ):
        route = Route(
            "DELETE", "/guilds/{guild_id}/members/{user_id}/roles/{role_id}",
            guild_id=guild_id, user_id=user_id, role_id=role_id
        )
        data = await self.request(route, reason=reason)
        return data

    async def kick_guild_member(
        self,
        guild_id: int,
        user_id: int,
        reason: typing.Optional[str] = None
    ):
        route = Route(
            "DELETE", "/guilds/{guild_id}/members/{user_id}",
            guild_id=guild_id, user_id=user_id
        )
        data = await self.request(route, reason=reason)
        return data

    # --- Guild Emojis --- #

    async def get_guild_emojis(self, guild_id: int):
        route = Route("GET", "/guilds/{guild_id}/emojis", guild_id=guild_id)
        data = await self.request(route)
        return data

    async def get_guild_emoji(self, guild_id: int, emoji_id: int):
        route = Route("GET", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id)
        data = await self.request(route)
        return data

    async def create_guild_emoji(self, guild_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("POST", "/guilds/{guild_id}/emojis", guild_id=guild_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def edit_guild_emoji(self, guild_id: int, emoji_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("PATCH", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def delete_guild_emoji(self, guild_id: int, emoji_id: int, reason: typing.Optional[str] = None):
        route = Route("DELETE", "/guilds/{guild_id}/emojis/{emoji_id}", guild_id=guild_id, emoji_id=emoji_id)
        data = await self.request(route, reason=reason)
        return data

    # --- Channels --- #

    async def get_guild_channels(self, guild_id: int):
        route = Route("GET", "/guilds/{guild_id}/channels", guild_id=guild_id)
        data = await self.request(route)
        return data

    async def create_guild_channel(self, guild_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("POST", "/guilds/{guild_id}/channels", guild_id=guild_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def get_channel(self, channel_id: int):
        route = Route("GET", "/channels/{channel_id}", channel_id=channel_id)
        data = await self.request(route)
        return data

    async def delete_channel(self, channel_id: int, reason: typing.Optional[str] = None):
        route = Route("DELETE", "/channels/{channel_id}", channel_id=channel_id)
        data = await self.request(route, reason=reason)
        return data

    async def edit_channel(self, channel_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("PATCH", "/channels/{channel_id}", channel_id=channel_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def set_permission_overwrite(
        self,
        channel_id: int,
        overwrite_id: int,
        json: typing.Dict[str, typing.Any],
        reason: typing.Optional[str] = None,
    ):
        route = Route("PUT", "/channels/{channel_id}/permissions/{overwrite_id}",
                      channel_id=channel_id, overwrite_id=overwrite_id)
        await self.request(route, json=json, reason=reason)

    async def remove_permission_overwrite(
        self,
        channel_id: int,
        overwrite_id: int,
        reason: typing.Optional[str] = None,
    ):
        route = Route("DELETE", "/channels/{channel_id}/permissions/{overwrite_id}",
                      channel_id=channel_id, overwrite_id=overwrite_id)
        await self.request(route, reason=reason)

    # --- Scheduled events --- #

    async def get_scheduled_events(self, guild_id: int, with_user_counts: bool = False):
        route = Route("GET", "/guilds/{guild_id}/scheduled-events", guild_id=guild_id)
        params = {"with_user_counts": int(with_user_counts)}
        data = await self.request(route, params=params)
        return data

    async def get_scheduled_event(self, guild_id: int, scheduled_event_id: int, with_user_counts: bool = False):
        route = Route("GET", "/guilds/{guild_id}/scheduled-events/{scheduled_event_id}",
                      guild_id=guild_id, scheduled_event_id=scheduled_event_id)

        params = {"with_user_counts": int(with_user_counts)}
        data = await self.request(route, params=params)
        return data

    async def create_scheduled_event(self, guild_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("POST", "/guilds/{guild_id}/scheduled-events", guild_id=guild_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def edit_scheduled_event(self, guild_id: int, scheduled_event_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("PATCH", "/guilds/{guild_id}/scheduled-events/{scheduled_event_id}",
                      guild_id=guild_id, scheduled_event_id=scheduled_event_id)

        data = await self.request(route, json=json, reason=reason)
        return data

    async def delete_scheduled_event(self, guild_id: int, scheduled_event_id: int, reason: typing.Optional[str] = None):
        route = Route("DELETE", "/guilds/{guild_id}/scheduled-events/{scheduled_event_id}",
                      guild_id=guild_id, scheduled_event_id=scheduled_event_id)

        await self.request(route, reason=reason)

    async def get_scheduled_event_users(
        self,
        guild_id: int,
        scheduled_event_id: int,
        after: int = UNDEFINED,
        before: int = UNDEFINED,
        with_member: bool = UNDEFINED,
        limit: int = UNDEFINED,
    ):
        route = Route("GET", "/guilds/{guild_id}/scheduled-events/{scheduled_event_id}/users",
                      guild_id=guild_id, scheduled_event_id=scheduled_event_id)

        params = {}

        if after is not UNDEFINED:
            params["after"] = after

        if before is not UNDEFINED:
            params["before"] = before

        if with_member is not UNDEFINED:
            params["with_member"] = int(with_member)

        if limit is not UNDEFINED:
            params["limit"] = limit

        data = await self.request(route, params=params)
        return data

    # --- Stage instance -- #

    async def create_stage_instance(self, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("POST", "/stage-instances")
        data = await self.request(route, json=json, reason=reason)
        return data

    async def get_stage_instance(self, channel_id: int):
        route = Route("GET", "/stage-instances/{channel_id}", channel_id=channel_id)
        data = await self.request(route)
        return data

    async def edit_stage_instance(self, channel_id: int, json: typing.Dict[str, typing.Any], reason: typing.Optional[str] = None):
        route = Route("PATCH", "/stage-instances/{channel_id}", channel_id=channel_id)
        data = await self.request(route, json=json, reason=reason)
        return data

    async def delete_stage_instance(self, channel_id: int, reason: typing.Optional[str] = None):
        route = Route("DELETE", "/stage-instances/{channel_id}", channel_id=channel_id)
        await self.request(route, reason=reason)

    # --- Messages --- #

    async def get_message(self, channel_id: int, message_id: int):
        route = Route(
            "GET", "/channels/{channel_id}/messages/{message_id}",
            channel_id=channel_id, message_id=message_id
        )
        data = await self.request(route)
        return data

    async def get_messages(
        self,
        channel_id: int,
        limit: int = UNDEFINED,
        after: int = UNDEFINED,
        before: int = UNDEFINED,
        around: int = UNDEFINED
    ):
        params = {}

        if limit is not UNDEFINED:
            params["limit"] = limit

        if after is not UNDEFINED:
            params["after"] = after

        if before is not UNDEFINED:
            params["before"] = before

        if around is not UNDEFINED:
            params["around"] = around

        route = Route("GET", "/channels/{channel_id}/messages", channel_id=channel_id)
        data = await self.request(route, params=params)
        return data

    async def get_pinned_messages(self, channel_id: int):
        route = Route("GET", "/channels/{channel_id}/pins", channel_id=channel_id)
        data = await self.request(route)
        return data

    async def send_message(
        self,
        channel_id: int,
        json: typing.Dict[str, typing.Any] = UNDEFINED,
        files: typing.List[File] = UNDEFINED,
    ):
        route = Route("POST", "/channels/{channel_id}/messages", channel_id=channel_id)

        if files is UNDEFINED:
            data = await self.request(route, json=json)
        else:
            form = aiohttp.FormData(quote_fields=False)

            attachments = []

            for index, file in enumerate(files):
                form.add_field(
                    f"files[{index}]",
                    file.content,
                    filename=file.proper_name,
                )

                attachment = {
                    "id": index,
                    "description": file.description,
                }
                attachments.append(attachment)

            if json is UNDEFINED:
                json = {}

            json["attachments"] = attachments
            form.add_field("payload_json", _json.dumps(json))

            data = await self.request(route, data=form)

        return data

    async def edit_message(
        self,
        channel_id: int,
        message_id: int,
        json: typing.Dict[str, typing.Any] = UNDEFINED,
        files: typing.List[File] = UNDEFINED,
    ):
        route = Route(
            "PATCH", "/channels/{channel_id}/messages/{message_id}",
            channel_id=channel_id, message_id=message_id
        )

        if files is UNDEFINED:
            data = await self.request(route, json=json)
        else:
            form = aiohttp.FormData(quote_fields=False)

            attachments = json.get("attachments", [])

            for index, file in enumerate(files):
                form.add_field(
                    f"files[{index}]",
                    file.content,
                    filename=file.proper_name,
                )

                attachment = {
                    "id": index,
                    "description": file.description,
                }
                attachments.append(attachment)

            if json is UNDEFINED:
                json = {}

            json["attachments"] = attachments
            form.add_field("payload_json", _json.dumps(json))

            data = await self.request(route, data=form)

        return data

    async def delete_message(self, channel_id: int, message_id: int):
        route = Route("DELETE", "/channels/{channel_id}/messages/{message_id}",
                      channel_id=channel_id, message_id=message_id)

        await self.request(route)

    async def trigger_typing(self, channel_id: int):
        route = Route("POST", "/channels/{channel_id}/typing", channel_id=channel_id)
        await self.request(route)

    async def crosspost_message(self, channel_id: int, message_id: int):
        route = Route("POST", "/channels/{channel_id}/messages/{message_id}/crosspost",
                      channel_id=channel_id, message_id=message_id)

        await self.request(route)

    # ---- Message Reactions ---- #

    async def get_reaction_users(
        self,
        channel_id: int,
        message_id: int,
        emoji: str,
        after: int = UNDEFINED,
        limit: int = UNDEFINED,
    ):
        route = Route("GET", "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}",
                      channel_id=channel_id, message_id=message_id, emoji=emoji)

        query = {}

        if after is not UNDEFINED:
            query["after"] = after
        if limit is not UNDEFINED:
            query["limit"] = limit

        data = await self.request(route, params=query)
        return data

    async def add_reaction(
        self,
        channel_id: int,
        message_id: int,
        emoji: str,
    ):
        route = Route("PUT", "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
                      channel_id=channel_id, message_id=message_id, emoji=emoji)
        await self.request(route)

    async def remove_own_reaction(
        self,
        channel_id: int,
        message_id: int,
        emoji: str,
    ):
        route = Route("DELETE", "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
                      channel_id=channel_id, message_id=message_id, emoji=emoji)
        await self.request(route)

    async def remove_user_reaction(
        self,
        channel_id: int,
        message_id: int,
        user_id: int,
        emoji: str,
    ):
        route = Route("DELETE", "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}",
                      channel_id=channel_id, message_id=message_id, emoji=emoji, user_id=user_id)
        await self.request(route)

    async def clear_reactions(
        self,
        channel_id: int,
        message_id: int,
    ):
        route = Route("DELETE", "/channels/{channel_id}/messages/{message_id}/reactions",
                      channel_id=channel_id, message_id=message_id)
        await self.request(route)

    async def clear_reactions_for_emoji(
        self,
        channel_id: int,
        message_id: int,
        emoji: str,
    ):
        route = Route("DELETE", "/channels/{channel_id}/messages/{message_id}/reactions/{emoji}",
                      channel_id=channel_id, message_id=message_id, emoji=emoji)
        await self.request(route)
