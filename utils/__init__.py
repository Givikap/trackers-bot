import discord

class RoleMgr:
    @staticmethod
    def get_between(roles: list[discord.Role], role1: discord.Role, role2: discord.Role) -> list[discord.Role]:
        lower, upper = sorted((role1.position, role2.position))
        return [role for role in roles if lower < role.position < upper]
    
    @staticmethod
    async def assign(member: discord.Member, roles: list[discord.Role]):
        for role in roles:
            await member.add_roles(role)

    @staticmethod
    async def purge(roles: list[discord.Role]):
        roles = [role for role in roles if role.members]

        for role in roles:
            members = role.members

            for member in members:
                await member.remove_roles(role)
