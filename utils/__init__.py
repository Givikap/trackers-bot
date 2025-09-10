import discord

import asyncio
import sys
from collections.abc import Iterable

class MemberMgr:
    @staticmethod
    async def assign(member: discord.Member, roles: Iterable[discord.Role]):
        for role in roles:
            await member.add_roles(role)

    @staticmethod
    async def purge_in(member: discord.Member, messageable: discord.abc.Messageable) -> int:
        total_messages_deleted = 0

        if isinstance(messageable, (discord.TextChannel, discord.Thread)):
            try:
                deleted_messages = await messageable.purge(
                    limit=None,
                    check=lambda m: m.author.id == member.id,
                    bulk=True
                )

                total_messages_deleted += len(deleted_messages)

            except (discord.Forbidden, discord.HTTPException) as e:
                sys.exit(f"{type(e).__module__}.{type(e).__name__}")

            try:
                async for message in messageable.history(limit=None, oldest_first=False):
                    if message.author.id != member.id:
                        continue
                    
                    if (discord.utils.utcnow() - message.created_at).days >= 14:
                        try:
                            await message.delete()
                            total_messages_deleted += 1
                            
                            await asyncio.sleep(1.05)
                        
                        except (discord.Forbidden, discord.HTTPException):
                            await asyncio.sleep(2.0)

            except (discord.Forbidden, discord.HTTPException) as e:
                sys.exit(f"{type(e).__module__}.{type(e).__name__}")
            
        return total_messages_deleted
    
class RoleMgr:
    @staticmethod
    def get_between(roles: Iterable[discord.Role], role1: discord.Role, role2: discord.Role) -> list[discord.Role]:
        lower, upper = sorted((role1.position, role2.position))
        return [role for role in roles if lower < role.position < upper]

    @staticmethod
    async def purge(roles: Iterable[discord.Role]):
        for role in roles:
            for member in role.members:
                await member.remove_roles(role)
