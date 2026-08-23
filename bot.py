import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)

coins = {}

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

def get_coins(user_id):
    return coins.get(user_id, 0)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello! 👋")

@bot.command()
async def bal(ctx):
    balance = get_coins(ctx.author.id)
    await ctx.send(f"💰 {ctx.author.mention}, your balance is **{balance} coins**.")

@bot.command()
async def daily(ctx):
    coins[ctx.author.id] = get_coins(ctx.author.id) + 100
    await ctx.send("🎁 You received **100 coins**!")

@bot.command()
async def work(ctx):
    earned = random.randint(50, 150)
    coins[ctx.author.id] = get_coins(ctx.author.id) + earned
    await ctx.send(f"💼 You earned **{earned} coins**!")

@bot.command()
async def cf(ctx):
    result = random.choice(["Heads 🪙", "Tails 🪙"])
    await ctx.send(f"🪙 Coin Flip: **{result}**")

@bot.command()
async def mine(ctx):
    earned = random.randint(20, 100)
    coins[ctx.author.id] = get_coins(ctx.author.id) + earned
    await ctx.send(f"⛏️ You mined **{earned} coins**!")

bot.run(os.getenv("DISCORD_TOKEN"))
