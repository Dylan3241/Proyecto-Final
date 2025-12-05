import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import datetime

DB_PATH = "database.bd"

class Registro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    #==================================================
    # REGISTRO
    #==================================================

    @app_commands.command(name="registrar", description="Registra a un usuario en el sistema del bot")
    @app_commands.describe(usuario="Selecciona el usuario que deseas registrar")
    async def registrar(self, interaction: discord.Interaction, usuario: discord.Member):

        user_id = usuario.id
        nombre = usuario.name
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (user_id,))
        existe = cursor.fetchone()

        if existe:
            conn.close()
            return await interaction.response.send_message(
                f"{usuario.mention} ya está registrado 👍", ephemeral=True
            )
        
        cursor.execute("""
            INSERT INTO usuarios (user_id, nombre, registrado_en)
            VALUES (?, ?, ?)
        """, (user_id, nombre, fecha))
        
        conn.commit()
        conn.close()

        await interaction.response.send_message(
            f"¡{usuario.mention} ha sido registrado correctamente! 🌱"
        )

    #==================================================
    # VER TU PERFIL
    #==================================================        
    
    @app_commands.command(name="perfil", description="Muestra tu información registrada")
    async def perfil(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT nombre, registrado_en FROM usuarios WHERE user_id = ?",
                       (user_id)
                    )
        
        datos = cursor.fetchone()
        conn.close

        if not datos:
            return await interaction.response.send_message(
                "No estás registrado. Usa `/registrar` primero."
            )
        
        nombre, fecha = datos
        
        embed = discord.Embed (
            title="📘 Tu perfil",
            color=0x00ff80
        )
        
        embed.add_field(name="👤 Nombre", value=nombre, inline=False)
        embed.add_field(name="🆔 ID", value=user_id, inline=False)
        embed.add_field(name="📅 Registrado el", value=fecha, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Registro(bot))

        