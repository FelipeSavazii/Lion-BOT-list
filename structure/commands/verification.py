from conn import db_connection

from discord.commands import slash_command
from discord.commands import Option
from discord.ext import commands
import discord

color = discord.Color.gold()

class Verification(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @slash_command(description="Verificar informaões de uma certa aplicação em análise. (gerenciar mensagens)")
    @discord.default_permissions(manage_messages=True)
    async def verificar(self, ctx, 
                          aplicação: Option(discord.Member, "Digite o ID ou marque a sua aplicação.")):
      conn = await db_connection()
      tipo = type(aplicação) is int
      app_id = aplicação if tipo == True else aplicação.id
      try:
        bot = conn.execute('SELECT * FROM bots WHERE app = ?', (app_id, )).fetchone()
        bot_2 = await self.bot.fetch_user(app_id)
        embed = discord.Embed(title="🤖 BOT LIST", description=f"Informações da aplicação **{bot_2.name}**:\n\nDescrição: {bot['desc']}.\nLinguagem: {bot['lang']}\nPrefixo: {bot['prefix']}\n\n**Clique [aqui](https://discord.com/api/oauth2/authorize?client_id={bot['app']}&permissions=534723950656&scope=bot%20applications.commands) para adicionar o bot**.\n", color=color)
      except TypeError:
        await ctx.respond(f'<:error:987048438413815839> | {ctx.author.mention} Esse bot não está registrado em nossa base de dados.')
      else:
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Verification(bot))