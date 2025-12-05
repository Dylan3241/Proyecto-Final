import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import datetime

DB_PATH = "database.db"

class Desafios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #==================================================
    # DESAFIOS SEMANALES
    #==================================================

    @app_commands.command(name="desafio", description="Muestra el desafio semanal activo")
    async def desafio(self, interaction: discord.Interaction):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        hoy = datetime.datetime.now().strftime("%Y-%m-%d")

        cursor.execute("SELECT id, titulo, descripcion FROM desafios WHERE fecha_inico <= ? and fecha_fin >= ?", (hoy, hoy))
        desafio = cursor.fetchone()
        conn.close

        if desafio:
            await interaction.response.send_message(f"**Desafio de la semana:** {desafio[1]}\n{desafio[2]}")
        else:
            await interaction.response.send_message(f"No hay desafios esta semana 😔", ephemeral= True)

    #==================================================
    # COMPLETAR UN DESAFIO
    #==================================================

    @app_commands.command(name="completar-desafio", description="Marca el desafio semanal como completado!")
    async def completar_desafio(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor

        hoy = datetime.datetime.now().strftime("%Y-%m-%d")

        cursor.execute("SELECT id, titulo, descripcion FROM desafios WHERE fecha_inico <= ? and fecha_fin >= ?", (hoy, hoy))
        desafio = cursor.fetchone()
        

        if not desafio:
            await interaction.response.send_message("No hay desafíos activos esta semana 😔")
            conn.close()
            return

        desafio_id = desafio[0]

        cursor.execute("""
                       INSERT OR REPLACE INTO desafios_usuarios (user_id, desadio_id, completado)
                       VALUES (?, ?, 1)
                       """,
                       (user_id, desafio_id))
        
        conn.commit()
        conn.close()

        await interaction.response.send_message("¡Desafío completado! 🌟 ¡Gracias por contribuir al cuidado del planeta!")

async def setup(bot):
    await bot.add_cog(Desafios(bot))
    
