import asyncio

import discord
from discord.ext import commands

from configs.role_categories import (
    COURSE_TRACKER_ROLE_CATEGORY,
    PERSONAL_ROLE_CATEGORY, 
    TA_ROLE_CATEGORY
)
from utils import MemberMgr, RoleMgr


class PurgeCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    purge = discord.SlashCommandGroup(
        name="purge",
        default_member_permissions=discord.Permissions(administrator=True),
    )

    @purge.command(
        name="course-trackers",
        description="Purge Course Trackers",
    )
    async def purge_course_trackers(self, ctx: discord.ApplicationContext):
        guild: discord.Guild = ctx.guild

        course_tracker_role_category = discord.utils.get(
            guild.roles, name=COURSE_TRACKER_ROLE_CATEGORY.name
        )
        course_tracker_role = discord.utils.get(
            guild.roles, name="Course Trackers"
        )

        await RoleMgr.purge(
            [
                course_tracker_role_category,
                course_tracker_role,
                *RoleMgr.get_between(
                    guild.roles,
                    course_tracker_role_category,
                    discord.utils.get(guild.roles, name=TA_ROLE_CATEGORY.name),
                ),
            ]
        )

        await ctx.respond("Purged Course Trackers", ephemeral=True)

    @purge.command(
        name="tas",
        description="Purge TAs",
    )
    async def purge_tas(self, ctx: discord.ApplicationContext):
        guild: discord.Guild = ctx.guild

        ta_role_category = discord.utils.get(
            guild.roles, name=TA_ROLE_CATEGORY.name
        )
        graduate_ta_role = discord.utils.get(guild.roles, name="Graduate TAs")
        undergraduate_ta_role = discord.utils.get(
            guild.roles, name="Undergraduate TAs"
        )

        await RoleMgr.purge(
            [
                ta_role_category,
                graduate_ta_role,
                undergraduate_ta_role,
                *RoleMgr.get_between(
                    guild.roles,
                    ta_role_category,
                    discord.utils.get(
                        guild.roles, name=PERSONAL_ROLE_CATEGORY.name
                    ),
                ),
            ]
        )

        await ctx.respond("Purged TAs", ephemeral=True)

    @purge.command(
        name="trackers",
        description="Purge Trackers",
    )
    async def purge_trackers(self, ctx: discord.ApplicationContext):
        await ctx.respond("Not implemented", ephemeral=True)

    @purge.command(
        name="member",
        description="Purge the given member",
    )
    @discord.option("member", type=discord.SlashCommandOptionType.mentionable)
    async def purge_user(
        self, ctx: discord.ApplicationContext, member: discord.Member
    ):
        guild: discord.Guild = ctx.guild

        await ctx.defer(ephemeral=True)

        messageables: list[discord.abc.Messageable] = [
            *guild.text_channels,
            *getattr(await guild.active_threads(), "threads", []),
            * [
                forum.threads
                for forum in [
                    channel
                    for channel in guild.channels
                    if isinstance(channel, discord.ForumChannel)
                ]
            ],
        ]

        for messagable in messageables:
            total_messages_deleted = await MemberMgr.purge_in(
                member, messagable
            )
            await asyncio.sleep(0.3)

            await ctx.followup.send(
                f"Purged {total_messages_deleted} messages from {member.mention} in {messagable.mention}",
                ephemeral=True,
            )

        await ctx.followup.send(f"Purged {member.name}", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(PurgeCommands(bot))
