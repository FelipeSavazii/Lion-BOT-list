from conn import db_connection

from discord.commands import slash_command
from discord.commands import Option
from discord import option
from discord.ext import commands
import discord

color = discord.Color.gold()

class Review(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @slash_command(description="Aprovar ou reprovar uma aplicação. (gerenciar mensagens)")
    @discord.default_permissions(manage_messages=True)
    @option(
      "nota",
      description="Escolha a nota da aplicação.",
      min_value=1,
      max_value=10
  )
    async def análise(self, ctx, 
                      aplicação: discord.Member, 
                      opção: Option(str, "Escolha a opção:", choices=["Aprovar", "Reprovar"]),
                      nota: int,
                      descrição: Option(str, "Digite observações") = None):
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
          if opção == "Aprovar":
            cargos = conn.execute('SELECT cargo_analise_id, cargo_aprovado_id FROM config WHERE guild_id = ?', (guild_id, )).fetchone()
            role1 = guild.get_role(cargos[0])
            role2 = guild.get_role(cargos[1])
            await bot.remove_roles(role1)
            await bot.add_roles(role2)
          elif opção == "Reprovar":
            await guild.kick(bot)

          config = conn.execute('SELECT * FROM config WHERE guild_id = ?', (guild_id, )).fetchone()
          channel = self.bot.get_channel(config['logs_id'])
          status = 'aprovada.' if opção == 'Aprovar' else 'reprovada.'
          embedc = discord.Embed(title=f"📥 BOT LOGS", description=f"A aplicação **{bot.name}** foi {status} \n\nNota: {nota}.\n{'Descrição: '+descrição+'.' if descrição != None else None}", color=color)
          embedr = discord.Embed(title=f"🤖 BOT LIST", description=f"A aplicação **{bot.name}** foi {status} com sucesso.", color=color)
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
