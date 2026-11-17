import discord
from discord.ext import commands
import redis


class Cache(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.r = redis.Redis(host="redis", port=6379, db=0)

    @discord.slash_command(
        name="cache_status",
        description="Cache status 2",
        guild_ids=[1545900943659245668],
    )
    async def cache_status(self, ctx):
        await ctx.respond(self.r.lolwut())


def setup(bot):
    bot.add_cog(Cache(bot))
