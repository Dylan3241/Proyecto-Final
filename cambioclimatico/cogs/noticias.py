import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
import xml.etree.ElementTree as ET

RSS_URL = "https://www.theguardian.com/environment/rss"

class Noticias(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #==================================================
    # VER NOTICIAS
    #==================================================

    @app_commands.command(
        name="noticias", 
        description="Muestra noticias recientes sobre el medio ambiente")
    async def noticias(self, interaction: discord.Interaction):
        
        await interaction.response.defer()

        async with aiohttp.ClientSession() as session:
                    async with session.get(RSS_URL, headers={"User-Agent": "Mozilla/5.0"}) as resp:
                        if resp.status != 200:
                            return await interaction.followup.send("No pude obtener noticias ahora mismo 😔")
                        
                        contenido = await resp.text()

         
         # Parsear XML del RSS               

        root = ET.fromstring(contenido)
        channel = root.find("channel")
        items = channel.findall("item")

        noticias = items[:5]

        embed = discord.Embed(
            title="🌎 Noticias ambientales recientes",
            description="Últimos titulares del mundo ambiental",
            color=0x00ff80
        )

        for noticia in noticias:
            titulo = noticia.find("title").text
            link = noticia.find("link").text
            embed.add_field(name=f"• {titulo}", value=f"[Leer noticia]({link})", inline=False)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Noticias(bot))

