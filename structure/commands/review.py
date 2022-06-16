from conn import db_connection

from discord.commands import slash_command
from discord.commands import Option
from discord.ext import commands
import discord

color = discord.Color.gold()

class Review(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @slash_command(description="Aprovar ou reprovar uma aplicação. (gerenciar mensagens)")
    @discord.default_permissions(manage_messages=True)
    async def análise(self, ctx, 
                      aplicação: discord.Member, 
                      opção: Option(str, "Escolha a opção:", choices=["aprovar", "reprovar"])):
        guild_id = ctx.guild.id
        guild = ctx.guild
        conn = await db_connection()
        try:
          tipo = type(aplicação) is int
          app_id = aplicação if tipo == True else aplicação.id
          bot = await guild.fetch_member(app_id)
          if opção == "aprovar":
            cargos = conn.execute('SELECT cargo_analise_id, cargo_aprovado_id FROM config WHERE guild_id = ?', (guild_id, )).fetchone()
            role1 = guild.get_role(cargos[0])
            role2 = guild.get_role(cargos[1])
            await bot.remove_roles(role1)
            await bot.add_roles(role2)
          elif opção == "reprovar":
            await self.bot.kick(bot)

          config = conn.execute('SELECT * FROM config WHERE guild_id = ?', (guild_id, )).fetchone()
          channel = self.bot.get_channel(config['logs_id'])
          embedc = discord.Embed(title=f"🤖 BOT LIST", description=f"A aplicação **{bot.name}** foi {'aprovado' if opção == 'aprovar' else 'reprovado'} com sucesso.", color=color)
          embedr = discord.Embed(title=f"📥 BOT LOGS", description=f"A aplicação **{bot.name}** foi {'aprovado' if opção == 'aprovar' else 'reprovado'}.", color=color)
          await channel.send(embed=embedc)
          await ctx.respond(embed=embedr)
              
          conn.execute('DELETE FROM bots WHERE app = ?', (app_id, ))   
          conn.commit()
          conn.close()
        except AttributeError as e:
          print(e)
          await ctx.respond(f'<:error:987048438413815839> | {ctx.author.mention} Esta aplicação não está registrado em nossa base de dados.')
        except discord.errors.NotFound as e:
          await ctx.respond(f'<:error:987048438413815839> | {ctx.author.mention} Esta aplicação não está no servidor.')
          

def setup(bot):
    bot.add_cog(Review(bot))