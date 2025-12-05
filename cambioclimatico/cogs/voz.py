import discord
from discord.ext import commands
import speech_recognition as sr
import subprocess
import os

class Voz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #==================================================
    # TRANSCRIBIR AUDIOS
    #==================================================

    @commands.command(name="transcribir")
    async def transcribir(self, ctx):
        await ctx.send("Buscando audio...")

        async for msg in ctx.channel.history(limit=20):
            for att in msg.attachments:
                if att.filename.endswith((".wav", ".mp3", ".ogg", ".m4a")):
                    ruta = f"./temp.{att.filename.split('.')[-1]}"
                    await att.save(ruta)

                    texto = await self.convertir_audio(ruta)
                    os.remove(ruta)

                    if texto:
                        return await ctx.send(f"📄 **Transcripción:**\n```{texto}```")
                    else:
                        return await ctx.send("No pude entender el audio.")

        await ctx.send("No encontré audios recientes.")

    async def convertir_audio(self, path):
        try:
            wav = path.rsplit(".", 1)[0] + ".wav"
            subprocess.run(["ffmpeg", "-i", path, wav, "-y"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            r = sr.Recognizer()
            with sr.AudioFile(wav) as s:
                audio = r.record(s)

            os.remove(wav)

            return r.recognize_google(audio, language="es-ES")
        except:
            return None

    #==================================================
    # FRASES DEL CAMBIO CLIMATICO
    #==================================================
    @commands.command(name="clima")
    async def frases_clima(self, ctx):
        frases = [
            "El cambio climático no es futuro, es presente.",
            "Cada grado que sube la temperatura global importa.",
            "Cuidar el planeta no es una opción, es una obligación.",
            "No existe un planeta B."
        ]

        import random
        frase = random.choice(frases)

        await ctx.send(f"🌍 **Frase sobre el clima:**\n> {frase}")

    #==================================================
    # DATOS DEL CAMBIO CLIMATICO
    #==================================================
    @commands.command(name="climadata")
    async def datos_clima(self, ctx):
        texto = (
            "🌡️ **Datos del cambio climático:**\n"
            "- La temperatura global ya aumentó más de 1.1°C desde la era preindustrial.\n"
            "- El 2023 y 2024 fueron de los años más cálidos registrados.\n"
            "- Se derriten los glaciares a un ritmo récord.\n"
            "- El nivel del mar continúa subiendo cada año.\n"
            "- Las olas de calor extremas son cada vez más frecuentes.\n"
        )
        await ctx.send(texto)

    #==================================================
    # FRASE RANDOM DE “VOZ” GENERAL
    #==================================================
    @commands.command(name="frase")
    async def frase_random(self, ctx):
        frases = [
            "Hablar es gratis, pero escuchar vale oro.",
            "El silencio a veces dice más que mil palabras.",
            "La voz es poderosa si sabes usarla."
        ]

        import random
        await ctx.send(random.choice(frases))


async def setup(bot):
    await bot.add_cog(Voz(bot))