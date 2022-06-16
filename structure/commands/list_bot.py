from conn import db_connection

from discord.commands import slash_command
from discord.ext import commands
import discord

color = discord.Color.gold()

class ListBot(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @slash_command(description="Lista de aplicações em análise. (gerenciar mensagens)")
    @discord.default_permissions(manage_messages=True)
    async def lista(self, ctx):
      guild_id = ctx.guild.id
      try:
        conn = await db_connection()
        bots = conn.execute(f'SELECT * FROM bots WHERE guild_id = {guild_id}').fetchone()
        embed = discord.Embed(title="🤖 BOT LIST", description=f"Lista de aplicações em análise: \n\n{'Nenhuma aplicação registrada.' if bots == None else None}", color=color)
        if bots:
          for bot in bots:
            try:
              bot_2 = await self.bot.fetch_user(bot['app'])
            except discord.errors.NotFound:
              pass
            else:
              invite = f"https://discord.com/api/oauth2/authorize?client_id={bot['app']}&permissions=534723950656&scope=bot%20applications.commands"
              embed.add_field(name=f'{bot_2.name}', value=f"Descrição: {bot['desc']}.\nLinguagem: {bot['lang']}\nID da Aplicação: {bot['app']}\nPrefixo: {bot['prefix']}\n\n**Clique [aqui]({invite}) para adicionar o bot.**", inline=False)
      except Exception as e:
        print(e)
      else:
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(ListBot(bot))