from conn import db_connection

from discord.commands import slash_command
from discord.commands import Option, OptionChoice
from discord.ext import commands
from discord.utils import get
import discord

color = discord.Color.gold()

class AddBot(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    language_list = [OptionChoice(name='Python', value='Python'), 
                     OptionChoice(name='Java', value='Java'), 
                     OptionChoice(name='JavaScript', value='Python'), 
                     OptionChoice(name='Kotlin', value='Kotlin'), 
                     OptionChoice(name='Lua', value='Lua'), 
                     OptionChoice(name='Elixir', value='Elixir'),
                     OptionChoice(name='PHP', value='PHP')]
    @slash_command(description="Adicionar aplicação à lista de análise.")
    async def adicionar(self, ctx, 
                        aplicação: Option(discord.Member, "Digite o ID ou marque a sua aplicação."), 
                        linguagem: Option(str, "Escolha a linguagem da sua aplicação.", choices=language_list),
                        descrição: Option(str, "Descreva como é a sua aplicação."), 
                        prefixo: Option(str, "Digite o prefixo da sua aplicação.")):
      guild_id = ctx.guild.id
      developer_id = ctx.author.id
      tipo = type(aplicação) is int
      app_id = aplicação if tipo == True else aplicação.id
      try:
        conn = await db_connection()
        conn.execute(
                        'INSERT INTO bots (guild_id, developer_id, app, lang, desc, prefix) VALUES (?, ?, ?, ?, ?, ?)',
                        (guild_id, developer_id, app_id, linguagem, descrição, prefixo))
        conn.commit()
      except Exception as e:
        print(e)
      else:
        embed = discord.Embed(title="🤖 BOT LIST", description=f"A aplicação adicionado com sucesso.", color=color)
        await ctx.respond(embed=embed, ephemeral=True)

      config = conn.execute('SELECT * FROM config WHERE guild_id = ?', (guild_id, )).fetchone()
      conn.close()
      channel = self.bot.get_channel(config['correio_id'])
      invite = f"https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions=534723950656&scope=bot%20applications.commands"

      bot = await self.bot.fetch_user(app_id)
                        
      embed = discord.Embed(title=f"📬 CORREIO", description=f"A aplicação **{bot.name}** de **{ctx.author.mention}** foi adicionado na lista de análise.\n\nDescrição: {descrição}.\nLinguagem: {linguagem}\nPrefixo: {prefixo}\n\n**Clique [aqui]({invite}) para adicionar o bot.**", color=color)
      await channel.send(embed=embed)

      channel = self.bot.get_channel(config['logs_id'])
      embed = discord.Embed(title=f"📥 BOT LOGS", description=f"A aplicação **{bot.name}** de **{ctx.author.mention}** foi adicionado na lista de análise.", color=color)
      await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(AddBot(bot))