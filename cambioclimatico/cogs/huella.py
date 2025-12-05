import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import datetime

DB_PATH = "database.db"

# Factores de emisión (kg CO₂ por unidad)
FACTOR_TRANSPORTE_KM = 0.21
FACTOR_ELECTRICIDAD_KWH = 0.433
FACTOR_CARNE_KG = 27.0
FACTOR_RESIDUOS_KG = 1.2

# -----------------------------------------
# Calcular huella anual
# -----------------------------------------
def compute_annual_kg(row):
    """
    row = (transporte_km, electricidad_kwh, carne_kg, residuos_kg)
    Unidades:
      - transporte_km: km por día
      - electricidad_kwh: kWh por mes
      - carne_kg: kg por semana
      - residuos_kg: kg por semana
    """

    transporte_km = row[0] or 0
    electricidad_kwh = row[1] or 0
    carne_kg = row[2] or 0
    residuos_kg = row[3] or 0

    transporte_annual = transporte_km * 365 * FACTOR_TRANSPORTE_KM
    electricidad_annual = electricidad_kwh * 12 * FACTOR_ELECTRICIDAD_KWH
    carne_annual = carne_kg * 52 * FACTOR_CARNE_KG
    residuos_annual = residuos_kg * 52 * FACTOR_RESIDUOS_KG

    total = transporte_annual + electricidad_annual + carne_annual + residuos_annual

    return total, {
        "transporte": transporte_annual,
        "electricidad": electricidad_annual,
        "carne": carne_annual,
        "residuos": residuos_annual
    }

class HuellaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #==================================================
    # ESTABLECER TU HUELLA
    #==================================================   


async def setup(bot):
    await bot.add_cog(HuellaCog(bot))

    