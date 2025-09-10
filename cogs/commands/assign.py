import discord
from discord.ext import commands

from configs.role_categories import (
    COURSE_TRACKER_ROLE_CATEGORY,
    TA_ROLE_CATEGORY
)
from utils import MemberMgr

class AssignCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    assign = discord.SlashCommandGroup(
        name="assign", 
        default_member_permissions=discord.Permissions(administrator=True)
    )

    @assign.command(
        name="course-tracker",
        description="Assign Course Tracker roles to the given member for the given course",
    )
    @discord.option("member", type=discord.SlashCommandOptionType.mentionable)
    @discord.option("course", type=discord.SlashCommandOptionType.role)
    async def assign_course_tracker(
        self, 
        ctx: discord.ApplicationContext,
        member: discord.Member, 
        course: discord.Role,
    ):
        guild: discord.Guild = ctx.guild

        await MemberMgr.assign(member, [
            discord.utils.get(guild.roles, name=COURSE_TRACKER_ROLE_CATEGORY.name),
            discord.utils.get(guild.roles, name="Course Trackers"),
            discord.utils.get(guild.roles, name=f"{course.name} Tracker")
        ])

        await ctx.respond(f"Assigned Course Tracker roles to {member.mention} for {course.mention}", ephemeral=True)

    @assign.command(
        name="grad-ta",
        description="Assign Graduate TA roles to the given member",
    )
    @discord.option("member", type=discord.SlashCommandOptionType.mentionable)
    @discord.option("course", type=discord.SlashCommandOptionType.role, required=False)
    async def assign_graduate_ta(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Member,
        course: discord.Role = None
    ):
        guild: discord.Guild = ctx.guild

        await MemberMgr.assign(member, [
            discord.utils.get(guild.roles, name=TA_ROLE_CATEGORY.name),
            discord.utils.get(guild.roles, name=f"Graduate TAs")
        ])

        if course:
            await MemberMgr.assign(member, [discord.utils.get(guild.roles, name=f"{course.name} TA")])
            
        await ctx.respond(
            f"Assigned Undergraduate TA role to {member.mention}{f' for {course.mention}' if course else ''}", 
            ephemeral=True
        )

    @assign.command(
        name="undergrad-ta",
        description="Assign Undergraduate TA roles to the given member for the given course",
    )
    @discord.option("member", type=discord.SlashCommandOptionType.mentionable)
    @discord.option("course", type=discord.SlashCommandOptionType.role)
    async def assign_undergraduate_ta(
        self, 
        ctx: discord.ApplicationContext, 
        member: discord.Member, 
        course: discord.Role
    ):
        guild: discord.Guild = ctx.guild

        await MemberMgr.assign(member, [
            discord.utils.get(guild.roles, name=TA_ROLE_CATEGORY.name),
            discord.utils.get(guild.roles, name=f"Undergraduate TAs"),
            discord.utils.get(guild.roles, name=f"{course.name} TA")
        ])

        await ctx.respond(f"Assigned Undergraduate TA role to {member.mention} for {course.mention}", ephemeral=True)
    
def setup(bot: commands.Bot):
    bot.add_cog(AssignCommands(bot)) 
