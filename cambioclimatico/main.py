import discord
from discord.ext import commands
from discord import app_commands
import config

class CambioClimatico(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all(),
            application_id=1321991836998438922
        )

    async def setup_hook(self):
        from database import create_tables
        create_tables()
        # Aca se cargan los cogs
        await self.load_extension("cogs.registro")
        await self.load_extension("cogs.noticias")
        await self.load_extension("cogs.huella")
        await self.load_extension("cogs.desafios")

        print("Bot cargado correctamente")

bot = CambioClimatico()

@bot.event
async def on_ready():
    print(f"Bot iniciado como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
        
    except Exception as e:
        print(f"Error al sincronizar: {e}")

bot.run(config.TOKEN)