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

from qord.core.cache import GuildCache
from qord.models.base import BaseModel
from qord.models.roles import Role
from qord.models.guild_members import GuildMember
from qord.models.channels import _guild_channel_factory, GuildChannel, VoiceChannel, StageChannel
from qord.models.emojis import Emoji
from qord.models.scheduled_events import ScheduledEvent
from qord.models.stage_instances import StageInstance
from qord.flags.system_channel import SystemChannelFlags
from qord.enums import EventPrivacyLevel, EventEntityType
from qord.internal.undefined import UNDEFINED
from qord.internal.mixins import Comparable, CreationTime
from qord.internal.helpers import (
    compute_snowflake,
    get_optional_snowflake,
    create_cdn_url,
    get_image_data,
    compute_shard_id,
    parse_iso_timestamp,
    BASIC_STATIC_EXTS,
    BASIC_EXTS,
)

from datetime import datetime
import typing


if typing.TYPE_CHECKING:
    from qord.core.shard import Shard
    from qord.core.client import Client
    from qord.flags.permissions import Permissions
    from qord.models.channels import CategoryChannel, TextChannel


__all__ = (
    "Guild",
)


class Guild(BaseModel, Comparable, CreationTime):
    """Representation of a Discord guild entity often referred as "Server" in the UI.

    |supports-comparison|

    Attributes
    ----------
    id: :class:`builtins.int`
        The snowflake ID of this guild.
    name: :class:`builtins.str`
        The name of this guild.
    afk_timeout: :class:`builtins.int`
        The AFK timeout after which AFK members are moved to designated AFK
        voice channel. ``0`` means no timeout.
    premium_subscription_count: :class:`builtins.int`
        The number of nitro boosts this guild has.
    preferred_locale: :class:`builtins.str`
        The chosen language for this guild.
    widget_enabled: :class:`builtins.bool`
        Whether guild has widget enabled.
    large: :class:`builtins.bool`
        Whether guild is marked as large.
    unavailable: :class:`builtins.bool`
        Whether guild is unavailable due to an outage.
    premium_progress_bar_enabled: :class:`builtins.bool`
        Whether guild has premium progress bar or server boosts progress
        bar enabled.
    features: :class:`builtins.str`
        The list of string representations of features of this guild. Complete
        list of valid features with meanings can be found here:

        https://discord.com/developers/docs/resources/guild#guild-object-guild-features
    system_channel_flags: :class:`SystemChannelFlags`
        The system channel flags for this guild.
    member_count: typing.Optional[:class:`builtins.int`]
        The member count of this guild.
    max_presences: typing.Optional[:class:`builtins.int`]
        The maximum number of presences for this guild, This is generally ``None``
        except for guilds marked as large.
    max_members: typing.Optional[:class:`builtins.int`]
        The maximum number of members for this guild.
    max_video_channel_users: typing.Optional[:class:`builtins.int`]
        The maximum number of video channel users for this guild.
    approximate_member_count: typing.Optional[:class:`builtins.int`]
        The approximated member count for this guild.
    approximate_presence_count: typing.Optional[:class:`builtins.int`]
        The approximated presences count for this guild.
    vanity_invite_code: typing.Optional[:class:`builtins.str`]
        The vanity invite code for this guild. To get complete URL, see
        :attr:`.vanity_invite_url`
    description: typing.Optional[:class:`builtins.str`]
        The description of this guild, if any.
    joined_at: typing.Optional[:class:`datetime.datetime`]
        The datetime representation of time when the bot had joined this guild.
    icon: typing.Optional[:class:`builtins.str`]
        The icon hash of this guild. If guild has no icon set, This is ``None``.
        See :meth:`.icon_url` to retrieve the URL to this.
    banner: typing.Optional[:class:`builtins.str`]
        The banner hash of this guild. If guild has no banner set, This is ``None``.
        See :meth:`.banner_url` to retrieve the URL to this.
    splash: typing.Optional[:class:`builtins.str`]
        The splash hash of this guild. If guild has no splash set, This is ``None``.
        See :meth:`.splash_url` to retrieve the URL to this.
    discovery_splash: typing.Optional[:class:`builtins.str`]
        The discovery splash hash of this guild. If guild has no discovery splash set,
        This is ``None``. See :meth:`.discovery_splash_url` to retrieve the URL to this.
    owner_id: typing.Optional[:class:`builtins.int`]
        The ID of owner of this guild.
    afk_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of designated AFK voice channel of this guild or ``None`` if no
        channel is set.
    widget_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of channel designated to be shown on guild's widget or ``None`` if no
        channel is set.
    application_id: typing.Optional[:class:`builtins.int`]
        The ID of application or bot that created this guild or ``None`` if guild is not
        created by an application or bot.
    system_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of channel designated for the system messages or ``None`` if no
        channel is set.
    rules_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of channel marked as rules channel in community guilds or ``None`` if no
        channel is set.
    public_updates_channel_id: typing.Optional[:class:`builtins.int`]
        The ID of channel designated for moderator updates community guilds or
        ``None`` if no channel is set.
    verification_level: :class:`builtins.int`
        The verification level value of this guild. See :class:`VerificationLevel`
        for more information about this.
    notification_level: :class:`builtins.int`
        The message notification level value of this guild. See :class:`NotificationLevel`
        for more information about this.
    explicit_content_filter: :class:`builtins.int`
        The explicit content filter level value of this guild. See :class:`ExplicitContentFilter`
        for more information about this.
    mfa_level: :class:`builtins.int`
        The 2FA requirement value of this guild. See :class:`MFALevel` for more information
        about this.
    premium_tier: :class:`builtins.int`
        The premium tier or server boosts level value of this guild. See
        :class:`PremiumTier` for more information about this.
    nsfw_level: :class:`builtins.int`
        The NSFW level value of this guild.  See :class:`NSFWLevel` for more information
        about this.
    """
    if typing.TYPE_CHECKING:
        # These are here to avoid cluttering in main code.
        id: int
        name: str
        afk_timeout: int
        premium_subscription_count: int
        preferred_locale: str
        widget_enabled: bool
        large: bool
        unavailable: bool
        premium_progress_bar_enabled: bool
        features: typing.List[str]
        system_channel_flags: SystemChannelFlags
        verification_level: int
        nsfw_level: int
        explicit_content_filter: int
        mfa_level: int
        notification_level: int
        premium_tier: int
        member_count: typing.Optional[int]
        max_presences: typing.Optional[int]
        max_members: typing.Optional[int]
        max_video_channel_users: typing.Optional[int]
        approximate_member_count: typing.Optional[int]
        approximate_presence_count: typing.Optional[int]
        vanity_invite_code: typing.Optional[str]
        description: typing.Optional[str]
        joined_at: typing.Optional[datetime]
        icon: typing.Optional[str]
        splash: typing.Optional[str]
        discovery_splash: typing.Optional[str]
        banner: typing.Optional[str]
        owner_id: typing.Optional[int]
        afk_channel_id: typing.Optional[int]
        application_id: typing.Optional[int]
        public_updates_channel_id: typing.Optional[int]
        rules_channel_id: typing.Optional[int]
        widget_channel_id: typing.Optional[int]
        system_channel_id: typing.Optional[int]

    __slots__ = ("_client", "_rest", "_cache", "_client_cache", "id", "name", "afk_timeout", "premium_subscription_count",
                "preferred_locale", "widget_enabled", "large", "unavailable", "system_channel_flags",
                "premium_progress_bar_enabled", "features", "verification_level", "notification_level",
                "mfa_level", "premium_tier", "nsfw_level", "member_count", "max_presences", "max_members",
                "max_video_channel_users", "approximate_member_count", "approximate_presence_count",
                "vanity_invite_code", "description", "joined_at", "icon", "splash", "discovery_splash",
                "banner", "owner_id", "afk_channel_id", "widget_channel_id", "application_id", "system_channel_id",
                "rules_channel_id", "public_updates_channel_id", "explicit_content_filter",)

    def __init__(self, data: typing.Dict[str, typing.Any], client: Client, enable_cache: bool = False) -> None:
        self._client = client
        self._rest = client._rest
        self._cache = client.get_guild_cache(guild=self)
        self._client_cache = client._cache
        if not isinstance(self._cache, GuildCache):
            raise TypeError(
                f"Client.get_guild_cache() returned an unexpected object of type " \
                f"{self._cache.__class__!r}, Expected a GuildCache instance." # type: ignore
            )
        self._cache.clear()
        self._create_guild(data)
        self._update_with_data(data)

    def __del__(self) -> None:
        self._cache.clear()

    def _create_guild(self, data: typing.Dict[str, typing.Any]) -> None:
        # These fields are only sent during initial GUILD_CREATE fields.
        # To avoid overwriting them in _update_with_data() method, These
        # are assigned here instead.

        joined_at = data.get("joined_at")
        self.joined_at = parse_iso_timestamp(joined_at) if joined_at is not None else None
        self.large = data.get("large", False)
        self.unavailable = data.get("unavailable", False)
        self.member_count = data.get("member_count")

        cache = self._cache
        client_cache = self._client_cache

        for raw_member in data.get("members", []):
            member = GuildMember(raw_member, guild=self)
            cache.add_member(member)
            client_cache.add_user(member.user)

        for raw_channel in data.get("channels", []):
            cls = _guild_channel_factory(raw_channel["type"])
            channel = cls(raw_channel, guild=self)
            cache.add_channel(channel)

        for raw_scheduled_event in data.get("guild_scheduled_events", []):
            scheduled_event = ScheduledEvent(raw_scheduled_event, guild=self)
            cache.add_scheduled_event(scheduled_event)

        for raw_stage_instance in data.get("stage_instances", []):
            stage_instance = StageInstance(raw_stage_instance, guild=self)
            cache.add_stage_instance(stage_instance)

    def _update_with_data(self, data: typing.Dict[str, typing.Any]) -> None:
        # I'm documenting these attributes here for future reference when we
        # eventually implement these features.
        #
        # - permissions
        # - voice_states
        # - threads
        # - presences
        # - welcome_screen
        # - stage_instances
        # - stickers
        # - guild_scheduled_events

        # General / non-optional attributes
        self.id = int(data["id"])
        self.name = data["name"]
        self.afk_timeout = data.get("afk_timeout", 0)
        self.premium_subscription_count = data.get("premium_subscription_count", 0)
        self.preferred_locale = data.get("preferred_locale", "en-US")
        self.widget_enabled = data.get("widget_enabled", False)
        self.premium_progress_bar_enabled = data.get("premium_progress_bar_enabled", False)
        self.features = data.get("features", [])
        self.system_channel_flags = SystemChannelFlags(data.get("system_channel_flags", 0))

        # Enums
        self.verification_level = data.get("verification_level", 0)
        self.notification_level = data.get("default_message_notifications", 0)
        self.explicit_content_filter = data.get("explicit_content_filter", 0)
        self.mfa_level = data.get("mfa_level", 0)
        self.premium_tier = data.get("premium_tier", 0)
        self.nsfw_level = data.get("nsfw_level", 0)

        # Nullable attributes
        self.max_presences = data.get("max_presences")
        self.max_members = data.get("max_presences")
        self.max_video_channel_users = data.get("max_video_channel_users")
        self.approximate_member_count = data.get("approximate_member_count")
        self.approximate_presence_count = data.get("approximate_presence_count")
        self.vanity_invite_code = data.get("vanity_url_code")
        self.description = data.get("description")

        # CDN resources
        self.icon = data.get("icon") or data.get("icon_hash")
        self.splash = data.get("splash")
        self.discovery_splash = data.get("discovery_splash")
        self.banner = data.get("banner")

        # Snowflakes
        self.owner_id = get_optional_snowflake(data, "owner_id")
        self.afk_channel_id = get_optional_snowflake(data, "afk_channel_id")
        self.widget_channel_id = get_optional_snowflake(data, "widget_channel_id")
        self.application_id = get_optional_snowflake(data, "application_id")
        self.system_channel_id = get_optional_snowflake(data, "system_channel_id")
        self.rules_channel_id = get_optional_snowflake(data, "rules_channel_id")
        self.public_updates_channel_id = get_optional_snowflake(data, "public_updates_channel_id")

        cache = self._cache

        for raw_role in data.get("roles", []):
            role = Role(raw_role, guild=self)
            cache.add_role(role)

        for raw_emoji in data.get("emojis", []):
            emoji = Emoji(raw_emoji, guild=self)
            cache.add_emoji(emoji)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    @property
    def cache(self) -> GuildCache:
        """Returns the cache handler associated to this guild.

        Returns
        -------
        :class:`GuildCache`
        """
        return self._cache

    @property
    def vanity_invite_url(self) -> typing.Optional[str]:
        """The vanity invite URL for the guild. If guild has no
        vanity invite set, ``None`` is returned.

        Returns
        -------
        :class:`builtins.str`
        """
        if self.vanity_invite_code is None:
            return None

        return f"https://discord.gg/{self.vanity_invite_code}"

    @property
    def shard_id(self) -> int:
        """The *computed* shard ID for this guild.

        Note that the value returned by this property is just computed
        using the guild ID and total shards count of the bound client and
        the actual shard with that ID may not exist in the client's cache.
        This is usually the case for guilds that are not cached by the client.

        Returns
        -------
        :class:`int`
        """
        shards_count = self._client.shards_count
        assert shards_count is not None, "No shards count is available yet."
        return compute_shard_id(guild_id=self.id, shards_count=shards_count)

    @property
    def shard(self) -> typing.Optional[Shard]:
        """The shard associated to this guild.

        This can be ``None`` in some cases, See :attr:`.shard_id` documentation
        for more information. This is equivalent to calling :meth:`Client.get_shard`
        using the :attr:`.shard_id`.

        Returns
        -------
        Optional[:class:`Shard`]
        """
        return self._client.get_shard(self.shard_id)

    @property
    def default_role(self) -> typing.Optional[Role]:
        """The default (@everyone) role of this guild.

        This property returns the result of :meth:`GuildCache.get_role`
        with ``role_id`` set to the guild ID. This returns ``None``
        for the guilds fetched over REST API.

        Returns
        -------
        Optional[:class:`Role`]
        """
        role_id = self.id
        return self._cache.get_role(role_id)

    @property
    def me(self) -> typing.Optional[GuildMember]:
        """Returns the :class:`GuildMember` for the bot's user.

        If the bot is not part of guild or the guild is fetched
        using :meth:`Client.fetch_guild`, this returns ``None``.

        Note that this property does not require :attr:`~Intents.members`
        intents as bot member is sent by Discord regardless.

        Returns
        -------
        Optional[:class:`GuildMember`]
        """
        user_id = self._client.user.id # type: ignore # This is never None here
        return self._cache.get_member(user_id)

    @property
    def owner(self) -> typing.Optional[GuildMember]:
        """Returns the owner of this guild.

        This property utilizes members cache and as such requires
        members intents to be enabled.

        Returns
        -------
        Optional[:class:`GuildMember`]
        """
        owner_id = self.owner_id

        if owner_id is None:
            return

        return self._cache.get_member(owner_id)

    @property
    def afk_channel(self) -> typing.Optional[VoiceChannel]:
        """Returns the AFK channel for this guild, if any.

        Returns
        -------
        Optional[:class:`VoiceChannel`]
        """
        afk_channel_id = self.afk_channel_id

        if afk_channel_id is None:
            return None

        # This shall always return VoiceChannel
        return self._cache.get_channel(afk_channel_id)  # type: ignore

    @property
    def widget_channel(self) -> typing.Optional[GuildChannel]:
        """Returns the widget channel for this guild, if any.

        Returns
        -------
        Optional[:class:`GuildChannel`]
        """
        widget_channel_id = self.widget_channel_id

        if widget_channel_id is None:
            return None

        return self._cache.get_channel(widget_channel_id)  # type: ignore

    @property
    def system_channel(self) -> typing.Optional[TextChannel]:
        """Returns the system channel for this guild, if any.

        Returns
        -------
        Optional[:class:`TextChannel`]
        """
        system_channel_id = self.system_channel_id

        if system_channel_id is None:
            return None

        # This shall always return TextChannel
        return self._cache.get_channel(system_channel_id)  # type: ignore

    @property
    def rules_channel(self) -> typing.Optional[TextChannel]:
        """Returns the rules channel for this guild, if any.

        Returns
        -------
        Optional[:class:`TextChannel`]
        """
        rules_channel_id = self.rules_channel_id

        if rules_channel_id is None:
            return None

        # This shall always return TextChannel
        return self._cache.get_channel(rules_channel_id)  # type: ignore

    @property
    def public_updates_channel(self) -> typing.Optional[TextChannel]:
        """Returns the public updates channel for this guild, if any.

        Returns
        -------
        Optional[:class:`TextChannel`]
        """
        public_updates_channel_id = self.public_updates_channel_id

        if public_updates_channel_id is None:
            return None

        # This shall always return TextChannel
        return self._cache.get_channel(public_updates_channel_id)  # type: ignore

    def icon_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the icon URL for this guild.

        If guild has no custom icon set, ``None`` is returned.

        The ``extension`` parameter only supports following extensions
        in the case of guild icons:

        - :attr:`ImageExtension.GIF`
        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. If not supplied, An ideal
            extension will be picked depending on whether guild has static
            or animated icon.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        if self.icon is None:
            return None
        if extension is UNDEFINED:
            extension = "gif" if self.is_icon_animated() else "png"

        return create_cdn_url(
            f"/icons/{self.id}/{self.icon}",
            extension=extension,
            size=size,
            valid_exts=BASIC_EXTS,
        )

    def banner_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the banner URL for this guild.

        If guild has no custom banner set, ``None`` is returned.

        The ``extension`` parameter only supports following extensions
        in the case of guild banners:

        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. Defaults to :attr:`~ImageExtension.PNG`.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        if self.banner is None:
            return
        if extension is UNDEFINED:
            extension = "png"

        return create_cdn_url(
            f"/banners/{self.id}/{self.banner}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )

    def splash_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the splash URL for this guild.

        If guild has no custom splash set, ``None`` is returned.

        The ``extension`` parameter only supports following extensions
        in the case of guild splashes:

        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. Defaults to :attr:`~ImageExtension.PNG`.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        if self.splash is None:
            return
        if extension is UNDEFINED:
            extension = "png"

        return create_cdn_url(
            f"/splashes/{self.id}/{self.splash}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )

    def discovery_splash_url(self, extension: str = UNDEFINED, size: int = UNDEFINED) -> typing.Optional[str]:
        """Returns the discovery splash URL for this guild.

        If guild has no custom discovery splash set, ``None`` is returned.

        The ``extension`` parameter only supports following extensions
        in the case of guild discovery splashes:

        - :attr:`ImageExtension.PNG`
        - :attr:`ImageExtension.JPG`
        - :attr:`ImageExtension.JPEG`
        - :attr:`ImageExtension.WEBP`

        Parameters
        ----------
        extension: :class:`builtins.str`
            The extension to use in the URL. Defaults to :attr:`~ImageExtension.PNG`.
        size: :class:`builtins.int`
            The size to append to URL. Can be any power of 2 between
            64 and 4096.

        Raises
        ------
        ValueError
            Invalid extension or size was passed.
        """
        if self.discovery_splash is None:
            return
        if extension is UNDEFINED:
            extension = "png"

        return create_cdn_url(
            f"/splashes/{self.id}/{self.discovery_splash}",
            extension=extension,
            size=size,
            valid_exts=BASIC_STATIC_EXTS,
        )

    def is_icon_animated(self) -> bool:
        """Indicates whether the guild has animated icon.

        Having no custom icon set will also return ``False``.

        Returns
        -------
        :class:`builtins.bool`
        """
        if self.icon is None:
            return False

        return self.icon.startswith("a_")

    # API calls

    async def leave(self) -> None:
        """Leaves the guild.

        Raises
        ------
        HTTPNotFound
            The bot is already not part of this guild.
        HTTPException
            HTTP request failed.
        """
        await self._rest.leave_guild(guild_id=self.id)

    # Roles

    async def fetch_roles(self) -> typing.List[Role]:
        """Fetches the list of roles associated to this guild.

        Returns
        -------
        List[:class:`Role`]
            The list of fetched roles.

        Raises
        ------
        HTTPException
            HTTPs request failed.
        """
        roles = await self._rest.get_roles(guild_id=self.id)
        return [Role(role, guild=self) for role in roles]

    async def create_role(self, *,
        name: str = UNDEFINED,
        permissions: Permissions = UNDEFINED,
        color: int = UNDEFINED,
        hoist: bool = UNDEFINED,
        icon: bytes = UNDEFINED,
        unicode_emoji: str = UNDEFINED,
        mentionable: bool = UNDEFINED,
        reason: typing.Optional[str] = None,
    ) -> Role:
        """Creates a role in this guild.

        This operation requires the :attr:`~Permissions.manage_roles` permission
        for the client user in the guild.

        Parameters
        ----------
        name: :class:`builtins.str`
            The name of this role. Defaults to ``"new role"``.
        permissions: :class:`Permissions`
            The permissions for this role. Defaults to @everyone role's permissions
            in the guild.
        color: :class:`builtins.int`
            The color value of this role.
        hoist: :class:`builtins.bool`
            Whether this role should appear hoisted from other roles.
        icon: :class:`builtins.bytes`
            The bytes representing the icon of this role. The guild
            must have ``ROLES_ICON`` feature to set this. This parameter
            cannot be mixed with ``unicode_emoji``.
        unicode_emoji: :class:`builtins.str`
            The unicode emoji used as icon for this role. The guild
            must have ``ROLES_ICON`` feature to set this. This
            parameter cannot be mixed with ``icon``.
        mentionable: :class:`builtins.bool`
            Whether this role is mentionable.
        reason: :class:`builtins.str`
            The reason for performing this action that shows up on
            the audit log entry.

        Returns
        -------
        :class:`Role`
            The created role.

        Raises
        ------
        HTTPForbidden
            You are missing the :attr:`~Permissions.manage_roles` permissions.
        HTTPException
            The creation failed.
        """
        json = {}

        if name is not UNDEFINED:
            json["name"] = name

        if permissions is not UNDEFINED:
            json["permissions"] = str(permissions.value)

        if color is not UNDEFINED:
            json["color"] = color

        if hoist is not UNDEFINED:
            json["hoist"] = hoist

        if icon is not UNDEFINED:
            json["icon"] = get_image_data(icon)

        if unicode_emoji is not UNDEFINED:
            json["unicode_emoji"] = unicode_emoji

        if mentionable is not UNDEFINED:
            json["mentionable"] = mentionable

        data = await self._rest.create_role(guild_id=self.id, json=json, reason=reason)
        return Role(data, guild=self)

    async def fetch_member(self, user_id: int) -> GuildMember:
        """Fetches a member from this guild for the provided user ID.

        Parameters
        ----------
        user_id: :class:`builtins.int`
            The ID of user to get member for.

        Raises
        ------
        HTTPNotFound
            Member not found.
        HTTPException
            Failed to fetch the member.

        Returns
        -------
        :class:`GuildMember`
            The requested member.
        """
        data = await self._rest.get_guild_member(guild_id=self.id, user_id=user_id)
        return GuildMember(data, guild=self)

    async def members(
        self,
        limit: typing.Optional[int] = None,
        after: typing.Union[int, datetime] = UNDEFINED,
    ) -> typing.AsyncIterator[GuildMember]:
        """Fetches and iterates through the members of this guild.

        This operation requires :attr:`~Intents.members` privileged intent
        to be enabled for the bot otherwise a :exc:`RuntimeError` is raised.

        Parameters
        ----------
        limit: Optional[:class:`builtins.int`]
            The number of members to fetch, ``None`` (default) indicates
            that all members should be fetched.
        after: Union[:class:`builtins.int`, :class:`datetime.datetime`]
            For paginating, To fetch members after the given user ID or
            members created after the given time. By default, the oldest
            created member is yielded first.

        Yields
        ------
        :class:`GuildMember`
            The fetched member.

        Raises
        ------
        RuntimeError
            Missing the members intents.
        """
        if not self._client.intents.members:
            raise RuntimeError("Intents.members flag is required to perform this operation.")

        if isinstance(after, datetime):
            after = compute_snowflake(after)

        while limit is None or limit > 0:
            if limit is None:
                current_limit = 1000
            else:
                current_limit = min(limit, 1000)

            data = await self._rest.get_guild_members(self.id, after=after, limit=current_limit)

            if limit is not None:
                limit -= current_limit

            if not data:
                break

            after = int(data[-1]["user"]["id"])

            for m in data:
                yield GuildMember(m, guild=self)

    async def search_members(self, query: str, *, limit: int = 1) -> typing.List[GuildMember]:
        """Fetches the members whose username or nickname start with the provided query.

        Parameters
        ----------
        query: :class:`builtins.str`
            The query to search with.
        limit: :class:`builtins.int`
            The maximum number of members to return. Defaults to ``1``. Provided
            integer cannot be larger then ``1000``.

        Raises
        ------
        HTTPException
            The fetching failed.

        Returns
        -------
        List[:class:`GuildMember`]
        """
        if limit < 1 or limit > 1000:
            raise ValueError("Parameter 'limit' cannot be lesser then 0 or greater then 1000.")

        params = {"query": query, "limit": limit}
        data = await self._rest.search_guild_members(guild_id=self.id, params=params)
        return [GuildMember(member, guild=self) for member in data]

    async def fetch_channels(self) -> typing.List[GuildChannel]:
        """Fetches the list of all channels of this guild.

        Returns
        -------
        List[:class:`GuildChannel`]

        Raises
        ------
        HTTPException
            Failed to fetch the channels.
        """
        data = await self._rest.get_guild_channels(guild_id=self.id)
        ret = []

        for channel in data:
            cls = _guild_channel_factory(channel["type"])
            ret.append(cls(channel, guild=self)) # should always be a subclass of GuildChannel

        return ret

    async def create_channel(
        self,
        type: int,
        name: str,
        *,
        bitrate: int = UNDEFINED,
        position: int = UNDEFINED,
        nsfw: bool = UNDEFINED,
        topic: typing.Optional[str] = UNDEFINED,
        user_limit: typing.Optional[int] = UNDEFINED,
        slowmode_delay: typing.Optional[str] = UNDEFINED,
        parent: typing.Optional[CategoryChannel] = UNDEFINED,
        reason: typing.Optional[str] = None,
    ):
        """Creates a channel in the guild.

        The ``name`` and ``type`` parameters are the only parameters that are
        required. Other parameters are optional.

        Requires the :attr:`~Permissions.manage_channels` permissions in the relevant
        guild to perform this action.

        Parameters
        ----------
        name: :class:`builtins.str`
            The name of this channel.
        type: :class:`builtins.int`
            The type of this channel.
        topic: :class:`builtins.str`
            The topic of this channel. Only valid for news and text channels.
        bitrate: :class:`builtins.int`
            The bitrate of this channel. Only valid for voice channels.
        user_limit: :class:`builtins.int`
            The number of users that can connect to the channel at a time.
            Only valid for voice channels.
        slowmode_delay: :class:`builtins.int`
            The slowmode delay of this channel. Only valid for text based
            channels.
        position: :class:`builtins.int`
            The position of this channel in the channels list.
        parent: :class:`CategoryChannel`
            The category that this channel belongs to.
        nsfw: :class:`builtins.bool`
            Whether this channel is marked as NSFW.
        reason: :class:`builtins.str`
            The reason for creating the channel that appears on the audit log.

        Returns
        -------
        :class:`GuildChannel`
            The created channel.

        Raises
        ------
        HTTPForbidden
            Missing permissions.
        HTTPBadRequest
            Invalid data in the provided channel.
        HTTPException
            The creation failed.
        """
        json = {
            "name": name,
            "type": type,
        }

        if topic is not UNDEFINED:
            json["topic"] = topic

        if bitrate is not UNDEFINED:
            json["bitrate"] = bitrate

        if user_limit is not UNDEFINED:
            json["user_limit"] = user_limit

        if slowmode_delay is not UNDEFINED:
            json["slowmode_delay"] = slowmode_delay

        if position is not UNDEFINED:
            json["position"] = position

        if parent is not None:
            json["parent_id"] = parent.id

        if nsfw is not UNDEFINED:
            json["nsfw"] = nsfw

        data = await self._rest.create_guild_channel(
            guild_id=self.id,
            json=json,
            reason=reason,
        )
        cls = _guild_channel_factory(data["type"])
        return cls(data, guild=self)

    async def fetch_emojis(self) -> typing.List[Emoji]:
        """Fetches the emojis of this guild.

        Returns
        -------
        List[:class:`Emoji`]
            The list of emojis from this guild.

        Raises
        ------
        HTTPException
            The fetching failed.
        """
        data = await self._rest.get_guild_emojis(guild_id=self.id)
        return [Emoji(e, guild=self) for e in data]

    async def fetch_emoji(self, emoji_id: int) -> Emoji:
        """Fetches the emoji from the given emoji ID.

        Returns
        -------
        :class:`Emoji`
            The requested emoji.

        Raises
        ------
        HTTPNotFound
            Emoji with that ID does not exist.
        HTTPException
            The fetching failed.
        """
        data = await self._rest.get_guild_emoji(guild_id=self.id, emoji_id=emoji_id)
        return Emoji(data, guild=self)

    async def create_emoji(
        self,
        image: bytes,
        name: str,
        *,
        roles: typing.Optional[typing.List[Role]] = UNDEFINED,
        reason: typing.Optional[str] = None,
    ) -> Emoji:
        """Creates an emoji in the guild.

        This operation requires :attr:`~Permissions.manage_emojis_and_stickers`
        permission in the parent emoji guild. The guild must also have a remaining
        slot available for emojis.

        The size of given image data must be less than or equal to 256 KB or
        the creation would fail.

        Parameters
        ----------
        image: :class:`builtins.bytes`
            The image data for the emoji in form of bytes object.
        name: :class:`builtins.str`
            The name of emoji.
        roles: Optional[List[:class:`Role`]]
            The list of roles that can use this emoji. ``None`` or empty
            list denotes that emoji is unrestricted.

        Returns
        -------
        :class:`Emoji`
            The created emoji.

        Raises
        ------
        HTTPForbidden
            You are not allowed to do this.
        HTTPException
            The creation of emoji failed.
        """
        json: typing.Dict[str, typing.Any] = {
            "image": get_image_data(image),
            "name": name,
        }

        if roles is not UNDEFINED:
            if roles is None:
                roles = []

            json["roles"] = [r.id for r in roles]

        data = await self._rest.create_guild_emoji(
            guild_id=self.id,
            json=json,
            reason=reason,
        )
        return Emoji(data, guild=self)

    async def fetch_scheduled_events(self, with_user_counts: bool = False) -> typing.List[ScheduledEvent]:
        """Fetches the scheduled events currently scheduled or active in the guild.

        Parameters
        ----------
        with_user_count: :class:`builtins.int`
            Whether to include :attr:`ScheduledEvent.user_count` data in the returned
            scheduled events.

        Returns
        -------
        List[:class:`ScheduledEvent`]
            The list of fetched events.

        Raises
        ------
        HTTPException
            Failed to fetch the events.
        """
        data = await self._rest.get_scheduled_events(
            guild_id=self.id,
            with_user_counts=with_user_counts
        )
        return [ScheduledEvent(e, guild=self) for e in data]

    async def fetch_scheduled_event(self, scheduled_event_id: int, with_user_counts: bool = False) -> ScheduledEvent:
        """Fetches the scheduled event by it's ID.

        Parameters
        ----------
        scheduled_event_id: :class:`builtins.int`
            The ID of event to fetch.
        with_user_count: :class:`builtins.int`
            Whether to include :attr:`ScheduledEvent.user_count` data in the returned
            scheduled event.

        Returns
        -------
        :class:`ScheduledEvent`
            The requested event.

        Raises
        ------
        HTTPNotFound
            The event with that ID does not exist.
        HTTPException
            Failed to fetch the event.
        """
        data = await self._rest.get_scheduled_event(
            guild_id=self.id,
            scheduled_event_id=scheduled_event_id,
            with_user_counts=with_user_counts
        )
        return ScheduledEvent(data, guild=self)

    async def create_scheduled_event(
        self,
        *,
        name: str,
        starts_at: datetime,
        ends_at: datetime = UNDEFINED,
        description: str = UNDEFINED,
        privacy_level: int = EventPrivacyLevel.GUILD_ONLY,
        location: str = UNDEFINED,
        entity_type: int = UNDEFINED,
        cover_image: bytes = UNDEFINED,
        channel: typing.Union[VoiceChannel, StageChannel] = UNDEFINED,
        reason: typing.Optional[str] = None,
    ) -> ScheduledEvent:
        """Creates a scheduled event in the guild.

        This operation requires :attr:`~Permissions.manage_events` permission
        in the guild.

        The ``channel`` and ``location`` keyword arguments are mutually exlusive and
        either one of them must be provided.

        The value of ``entity_type`` keyword argument is inferred from what is being
        passed from ``channel`` or ``location`` that is:

        - If a :class:`VoiceChannel` is passed in ``channel``, The inferred value would be :attr:`EventEntityType.VOICE`
        - If a :class:`StageChannel` is passed in ``channel``, The inferred value would be :attr:`EventEntityType.STAGE_INSTANCE`
        - If a ``location`` is passed, The inferred value would be :attr:`EventEntityType.EXTERNAL`.

        If the ``entity_type`` parameter is passed explicitly, the value is not inferred and
        the given value is considered without validation.

        ``ends_at`` keyword argument is required when passing the ``location`` argument.

        Parameters
        ----------
        name: :class:`builtins.str`
            The name of event.
        starts_at: :class:`datetime.datetime`
            The time when the event should start.
        ends_at: :class:`datetime.datetime`
            The time when the event should end. Required when passing ``location``,
            optional otherwise.
        description: :class:`builtins.str`
            The description of event.
        privacy_level: :class:`builtins.int`
            The privacy level of the event. Defaults to :attr:`EventPrivacyLevel.GUILD_ONLY`.
        location: :class:`builtins.str`
            The location where the event is hosted.
        entity_type: :class:`builtins.int`
            The type of entity for this event. This parameter is inferred automatically
            when not given, see above.
        cover_image: :class:`builtins.bytes`
            The bytes representing the cover image of event.
        channel: Union[:class:`VoiceChannel`, :class:`StageChannel`]
            The channel where the event is being hosted.
        reason: :class:`builtins.str`
            The reason for creating the event.

        Returns
        -------
        :class:`ScheduledEvent`
            The created event.

        Raises
        ------
        TypeError
            Invalid arguments passed.
        HTTPForbidden
            You are not allowed to create the event.
        HTTPException
            Failed to create the event.
        """
        if location is UNDEFINED and channel is UNDEFINED:
            raise TypeError("Either one of channel or location arguments must be passed.")
        if location is not UNDEFINED and channel is not UNDEFINED:
            raise TypeError("location and channel keyword arguments cannot be mixed.")
        if location is not UNDEFINED and ends_at is UNDEFINED:
            raise TypeError("ends_at must be provided when providing location.")

        json: typing.Dict[str, typing.Any] = {
            "name": name,
            "privacy_level": privacy_level,
            "scheduled_start_time": starts_at.isoformat(),
        }

        if entity_type is UNDEFINED:
            # No explicit value for entity_type is given, Inferring the value.
            if location is not UNDEFINED:
                entity_type = EventEntityType.EXTERNAL
            else:
                channel_tp = type(channel)
                if channel_tp == StageChannel:
                    entity_type = EventEntityType.STAGE_INSTANCE
                elif channel_tp == VoiceChannel:
                    entity_type = EventEntityType.VOICE
                else:
                    raise TypeError("channel must be an instance of StageChannel or VoiceChannel")

        json["entity_type"] = entity_type

        if ends_at is not UNDEFINED:
            json["scheduled_end_time"] = ends_at.isoformat()

        if description is not UNDEFINED:
            json["description"] = description

        if channel is not UNDEFINED:
            json["channel_id"] = channel.id

        if location is not UNDEFINED:
            json["entity_metadata"] = {"location": location}

        if cover_image is not UNDEFINED:
            json["image"] = get_image_data(cover_image)

        data = await self._rest.create_scheduled_event(guild_id=self.id, json=json, reason=reason)
        return ScheduledEvent(data, guild=self)
