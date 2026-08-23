import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents)

# Virtual coins
coins = {}


def get_coins(user_id):
    return coins.get(user_id, 0)


@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")


# ?bal
@bot.command()
async def bal(ctx):
    balance = get_coins(ctx.author.id)
    await ctx.send(
        f"💰 {ctx.author.mention}\n"
        f"Balance: **{balance:,} coins**"
    )


# ?daily
@bot.command()
async def daily(ctx):
    amount = random.randint(50000, 100000)
    coins[ctx.author.id] = get_coins(ctx.author.id) + amount

    await ctx.send(
        f"🎁 {ctx.author.mention} received **{amount:,} coins**!"
    )


# ?work
@bot.command()
async def work(ctx):
    amount = random.randint(500, 5000)
    coins[ctx.author.id] = get_coins(ctx.author.id) + amount

    await ctx.send(
        f"💼 You worked and earned **{amount:,} coins**!"
    )


# ?mine
@bot.command()
async def mine(ctx):
    amount = random.randint(100, 3000)
    coins[ctx.author.id] = get_coins(ctx.author.id) + amount

    await ctx.send(
        f"⛏️ You mined **{amount:,} coins**!"
    )


# ?rob @user
@bot.command()
async def rob(ctx, member: discord.Member):

    if member.id == ctx.author.id:
        await ctx.send("❌ You can't rob yourself!")
        return

    target_balance = get_coins(member.id)

    if target_balance <= 0:
        await ctx.send("❌ This user has no coins!")
        return

    amount = random.randint(
        100,
        min(10000, target_balance)
    )

    coins[member.id] = target_balance - amount
    coins[ctx.author.id] = get_coins(ctx.author.id) + amount

    await ctx.send(
        f"🕵️ {ctx.author.mention} stole "
        f"**{amount:,} coins** from {member.mention}!"
    )


# ?leaderboard
@bot.command(aliases=["lb", "top"])
async def leaderboard(ctx):

    if not coins:
        await ctx.send("🏆 Leaderboard is empty!")
        return

    ranking = sorted(
        coins.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    message = "🏆 **COINS LEADERBOARD** 🏆\n\n"

    for position, (user_id, balance) in enumerate(
        ranking, start=1
    ):
        user = bot.get_user(user_id)

        if user:
            name = user.display_name
        else:
            name = f"User {user_id}"

        message += (
            f"**#{position}** "
            f"{name} — 💰 **{balance:,}**\n"
        )

    await ctx.send(message)


# ?slots
# No betting — just a random virtual reward
@bot.command()
async def slots(ctx):

    symbols = ["🍒", "🍋", "🍉", "⭐", "💎"]

    result = [
        random.choice(symbols),
        random.choice(symbols),
        random.choice(symbols)
    ]

    await ctx.send(
        f"🎰 **SLOTS**\n\n"
        f"┃ {' | '.join(result)} ┃"
    )

    if result[0] == result[1] == result[2]:

        reward = random.randint(5000, 20000)

        coins[ctx.author.id] = (
            get_coins(ctx.author.id) + reward
        )

        await ctx.send(
            f"🎉 JACKPOT!\n"
            f"💰 You received **{reward:,} coins**!"
        )

    else:
        reward = random.randint(100, 1000)

        coins[ctx.author.id] = (
            get_coins(ctx.author.id) + reward
        )

        await ctx.send(
            f"🍀 You received **{reward:,} coins**!"
        )


# ?help
@bot.command(name="help")
async def help_command(ctx):

    message = """
📖 **BOT COMMANDS**

💰 `?bal` — Check your coins
🎁 `?daily` — Get 50K–100K coins
💼 `?work` — Work and earn coins
⛏️ `?mine` — Mine and earn coins
🕵️ `?rob @user` — Steal virtual coins
🏆 `?leaderboard` — Top 10 richest players
🎰 `?slots` — Play slots for random virtual rewards
📖 `?help` — Show this help menu

Example:
`?bal`
`?daily`
`?mine`
`?rob @username`
`?leaderboard`
`?slots`
"""

    await ctx.send(message)


# ?hello
@bot.command()
async def hello(ctx):
    await ctx.send("Hello! 👋")


# Start bot
bot.run(os.getenv("DISCORD_TOKEN"))
