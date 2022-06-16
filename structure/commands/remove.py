from conn import db_connection

from discord.commands import slash_command
from discord.commands import Option
from discord import option
from discord.ext import commands
import discord

color = discord.Color.gold()

class Remove(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @slash_command(description="Remover uma aplicação da lista de análises. (expulsar membros)")
    @discord.default_permissions(kick_members=True)
    async def remover(self, ctx, aplicação: discord.Member):
        guild_id = ctx.guild.id
        guild = ctx.guild
        conn = await db_connection()
        try:
          tipo = type(aplicação) is int
          app_id = aplicação if tipo == True else aplicação.id
          bot = await guild.fetch_member(app_id)
          verification_bot = conn.execute('SELECT * FROM bots WHERE app = ?', (app_id, )).fetchone()
          if verification_bot:
            pass
          else:
            raise AttributeError

          config = conn.execute('SELECT * FROM config WHERE guild_id = ?', (guild_id, )).fetchone()
          channel = self.bot.get_channel(config['logs_id'])
          embedc = discord.Embed(title=f"🤖 BOT LIST", description=f"A aplicação **{bot.name}** foi removida da lista de análise com sucesso.", color=color)
          embedr = discord.Embed(title=f"📥 BOT LOGS", description=f"A aplicação **{bot.name}** foi removida da lista de análise.", color=color)
          await channel.send(embed=embedr)
          await ctx.respond(embed=embedc)
              
          conn.execute('DELETE FROM bots WHERE app = ?', (app_id, ))   
          conn.commit()
          conn.close()
        except AttributeError as e:
          print(e)
          await ctx.respond(f'<:error:987048438413815839> | {ctx.author.mention} Esta aplicação não está registrado em nossa base de dados.')
        except discord.errors.NotFound as e:
          await ctx.respond(f'<:error:987048438413815839> | {ctx.author.mention} Esta aplicação não está no servidor.')

    @slash_command(description="Remover uma aplicação aprovada/em análise do servidor. (expulsar membros)")
    @discord.default_permissions(kick_members=True)
    async def expulsar(self, ctx, aplicação: discord.Member):
        guild_id = ctx.guild.id
        guild = ctx.guild
        conn = await db_connection()
        try:
          tipo = type(aplicação) is int
          app_id = aplicação if tipo == True else aplicação.id
          bot = await guild.fetch_member(app_id)
          config = conn.execute('SELECT * FROM config WHERE guild_id = ?', (guild_id, )).fetchone()
          conn.close()
          await guild.kick(bot)
          channel = self.bot.get_channel(config['logs_id'])
          embedc = discord.Embed(title=f"🤖 BOT LIST", description=f"A aplicação **{bot.name}** foi expulsa do servidor com sucesso.", color=color)
          embedr = discord.Embed(title=f"📥 BOT LOGS", description=f"A aplicação **{bot.name}** foi expulsa do servidor.", color=color)
          await channel.send(embed=embedr)
          await ctx.respond(embed=embedc)
        except discord.errors.NotFound as e:
          await ctx.respond(f'<:error:987048438413815839> | {ctx.author.mention} Esta aplicação não está no servidor.')
          

def setup(bot):
    bot.add_cog(Remove(bot))
