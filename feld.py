import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
intents.guilds = True
intents.messages = True
intents.guild_messages = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")

@bot.command(name="delete_category")
async def delete_category(ctx, *, category_name: str):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=category_name)

    if category is None:
        await ctx.send(f"❌ Kategorie `{category_name}` wurde nicht gefunden.")
        return

    confirm_message = await ctx.send(
        f"⚠️ Bist du sicher, dass du die Kategorie **{category.name}** und alle enthaltenen Channels löschen willst? Antworte mit `ja` oder `nein`."
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["ja", "nein"]

    try:
        reply = await bot.wait_for("message", check=check, timeout=30.0)
    except:
        await ctx.send("⏰ Zeitüberschreitung. Löschung abgebrochen.")
        return

    if reply.content.lower() == "ja":
        for channel in category.channels:
            await channel.delete()
        await category.delete()
        await ctx.send(f"🗑️ Kategorie **{category.name}** und alle Channels wurden gelöscht.")
    else:
        await ctx.send("❎ Löschung abgebrochen.")

bot.run(os.getenv("TOKEN"))
