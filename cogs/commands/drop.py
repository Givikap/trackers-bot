import discord
from discord.ext import commands

import logging

from configs.role_categories import (
    COURSE_TRACKER_ROLE_CATEGORY,
    TA_ROLE_CATEGORY,
    PERSONAL_ROLE_CATEGORY,
)
from utils import RoleMgr

logger = logging.getLogger(__name__)

class DropCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="drop-course-trackers")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def drop_course_trackers(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild

        course_tracker_role_category = discord.utils.get(guild.roles, name=COURSE_TRACKER_ROLE_CATEGORY.name)
        course_tracker_role = discord.utils.get(guild.roles, name="Course Trackers")

        logger.info("Dropping all Course Trackers roles.")

        await RoleMgr.purge([
            course_tracker_role_category,
            course_tracker_role,
            *RoleMgr.get_between(
                guild.roles, 
                course_tracker_role_category, 
                discord.utils.get(guild.roles, name=TA_ROLE_CATEGORY.name)
            )
        ])

        logger.info("Dropped all Course Trackers roles.")

    @commands.command(name="drop-TAs")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def drop_tas(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild

        ta_role_category = discord.utils.get(guild.roles, name=TA_ROLE_CATEGORY.name)
        graduate_ta_role = discord.utils.get(guild.roles, name="Graduate TAs")
        undergraduate_ta_role = discord.utils.get(guild.roles, name="Undergraduate TAs")

        logger.info("Dropping all TA roles.")

        await RoleMgr.purge([
            ta_role_category,
            graduate_ta_role,
            undergraduate_ta_role,
            *RoleMgr.get_between(
                guild.roles, 
                ta_role_category,
                discord.utils.get(guild.roles, name=PERSONAL_ROLE_CATEGORY.name),
            )
        ])

        logger.info("Dropped all TA roles.")

    @commands.command(name="drop-trackers")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def drop_trackers(self, ctx: commands.Context):
        pass

    @commands.command(name="drop-all")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def drop_all(self, ctx: commands.Context):
        pass
 
def setup(bot: commands.Bot):
    bot.add_cog(DropCommands(bot)) 
