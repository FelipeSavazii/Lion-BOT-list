from conn import db_connection

from discord.commands import slash_command
from discord.commands import Option
from discord.ext import commands
import discord

color = discord.Color.gold()

class Config(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    @slash_command(description="Configuração do sistema de bot list. (somente administradores)")
    @discord.default_permissions(administrator=True)
    async def configurações(self, ctx, 
                            correio: Option(discord.TextChannel, "Digite o ID do canal de correio."), 
                            logs: Option(discord.TextChannel, "Digite o ID do canal de logs."), 
                            bot_em_analise: Option(discord.Role, "Digite o ID do cargo que as aplicações em análise irão receber."), 
                            bot_aprovado: Option(discord.Role, "Digite o ID do cargo que as aplicações aprovadas irão receber."), 
                            developer: Option(discord.Role, "Digite o ID do cargo que os desenvolvedores das aplicações aprovadas irão receber."),
                            verificador: Option(discord.Role, "Digite o ID do cargo que verificará as aplicações.")):
      guild_id = ctx.guild.id
      try:
        conn = await db_connection()
        try:
          post = conn.execute('SELECT * FROM config WHERE guild_id = ?', (guild_id, )).fetchone()
          if post != None:
            conn.execute(
                        'UPDATE config SET correio_id = ?, logs_id = ?, cargo_analise_id = ?, cargo_aprovado_id = ?, cargo_dev_id = ?, cargo_verificador_id WHERE guild_id = ?',
                        (correio.id, logs.id, bot_em_analise.id, bot_aprovado.id, developer.id, verificador.id, guild_id))
          else:
            conn.execute(
                        'INSERT INTO config (guild_id, correio_id, logs_id, cargo_analise_id, cargo_aprovado_id, cargo_dev_id, cargo_verificador_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (guild_id, correio.id, logs.id, bot_em_analise.id, bot_aprovado.id, developer.id, verificador.id))
          conn.commit()
          conn.close()
        except Exception as e:
          print(e)
      except Exception as e:
        print(e)
      else:
        embed = discord.Embed(title="🤖 BOT LIST", description=f'Configurações alteradas com sucesso.\n\n'
                              f'**CANAIS**:\n\n📬 {correio.mention}\n📥 {logs.mention}\n\n'
                              f'**CARGOS**:\n\n🤔 {bot_em_analise.mention}\n✅ {bot_aprovado.mention}\n🧑‍💻 {developer.mention}', color=color)
        await ctx.respond(embed=embed, ephemeral=True)
      

def setup(bot):
    bot.add_cog(Config(bot))