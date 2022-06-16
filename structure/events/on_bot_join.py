from conn import db_connection

from discord.ext import commands
import discord

color = discord.Color.gold()

class OnBotJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        conn = await db_connection()
        bots = conn.execute('SELECT guild_id FROM bots WHERE app = ?', (member.id, )).fetchone()
        if bots != None:
          for bot in bots:
            cargo = conn.execute('SELECT cargo_analise_id FROM config WHERE guild_id = ?', (bot, )).fetchone()[0]
            guild = self.bot.get_guild(bot)
            role = guild.get_role(cargo)
            await member.add_roles(role)
        else:
          pass

def setup(bot):
    bot.add_cog(OnBotJoin(bot))