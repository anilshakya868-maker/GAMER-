import os
import random
import time
import discord
from discord.ext import commands

# =========================
# BOT SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="?",
    intents=intents,
    help_command=None
)

# =========================
# DATA
# =========================

coins = {}
daily_cooldown = {}
rob_cooldown = {}


def get_coins(user_id):
    return coins.get(user_id, 0)


def add_coins(user_id, amount):
    coins[user_id] = get_coins(user_id) + amount


# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")


# =========================
# BALANCE
# =========================

@bot.command()
async def bal(ctx):
    balance = get_coins(ctx.author.id)

    await ctx.send(
        f"💰 **{ctx.author.display_name}**\n"
        f"Balance: **{balance:,} coins**"
    )


# =========================
# DAILY - 24 HOURS
# =========================

@bot.command()
async def daily(ctx):
    user_id = ctx.author.id
    now = time.time()

    if user_id in daily_cooldown:
        remaining = 86400 - (
            now - daily_cooldown[user_id]
        )

        if remaining > 0:
            hours = int(remaining // 3600)
            minutes = int(
                (remaining % 3600) // 60
            )

            await ctx.send(
                f"⏰ Daily already claimed!\n"
                f"Come back in **{hours}h {minutes}m**."
            )
            return

    amount = random.randint(50000, 100000)

    add_coins(user_id, amount)
    daily_cooldown[user_id] = now

    await ctx.send(
        f"🎁 **DAILY REWARD**\n"
        f"💰 You received **{amount:,} coins**!"
    )


# =========================
# WORK
# =========================

@bot.command()
async def work(ctx):
    amount = random.randint(500, 5000)

    add_coins(ctx.author.id, amount)

    await ctx.send(
        f"💼 You worked!\n"
        f"💰 Earned **{amount:,} coins**."
    )


# =========================
# MINE - DIAMOND / BOMB
# =========================

@bot.command()
async def mine(ctx):

    result = random.choice([
        "diamond",
        "diamond",
        "diamond",
        "bomb"
    ])

    if result == "bomb":

        await ctx.send(
            "⛏️ **MINE GAME**\n\n"
            "💣 **BOOM!**\n"
            "You found a bomb!\n"
            "❌ No reward this round."
        )

    else:

        amount = random.randint(
            1000,
            10000
        )

        add_coins(
            ctx.author.id,
            amount
        )

        await ctx.send(
            "⛏️ **MINE GAME**\n\n"
            "💎 **DIAMOND FOUND!**\n"
            f"🎉 You won **{amount:,} coins**!"
        )


# =========================
# ROB - 1 HOUR COOLDOWN
# =========================

@bot.command()
async def rob(ctx, member: discord.Member):

    user_id = ctx.author.id
    now = time.time()

    if member.id == user_id:
        await ctx.send(
            "❌ You can't rob yourself!"
        )
        return

    if member.bot:
        await ctx.send(
            "❌ You can't rob a bot!"
        )
        return

    if user_id in rob_cooldown:

        remaining = 3600 - (
            now - rob_cooldown[user_id]
        )

        if remaining > 0:

            minutes = int(
                remaining // 60
            )

            await ctx.send(
                f"⏰ Rob cooldown!\n"
                f"Try again in **{minutes} minutes**."
            )
            return

    target_balance = get_coins(member.id)

    if target_balance <= 0:

        await ctx.send(
            "❌ This user has no coins!"
        )
        return

    rob_cooldown[user_id] = now

    amount = random.randint(
        100,
        min(10000, target_balance)
    )

    coins[member.id] -= amount
    add_coins(user_id, amount)

    await ctx.send(
        f"🕵️ **ROBBED!**\n"
        f"{ctx.author.mention} stole "
        f"**{amount:,} coins** from "
        f"{member.mention}!"
    )


# =========================
# COIN FLIP
# =========================

@bot.command()
async def cf(ctx):

    result = random.choice([
        "win",
        "loss"
    ])

    if result == "win":

        reward = random.randint(
            1000,
            10000
        )

        add_coins(
            ctx.author.id,
            reward
        )

        await ctx.send(
            "🪙 **COIN FLIP**\n\n"
            "🟢 **WIN!** 🎉\n"
            f"💰 Reward: **{reward:,} coins**"
        )

    else:

        await ctx.send(
            "🪙 **COIN FLIP**\n\n"
            "🔴 **LOSS!** 😢\n"
            "No coins won this round."
        )


# =========================
# SLOTS
# =========================

@bot.command()
async def slots(ctx):

    symbols = [
        "🍒",
        "🍋",
        "🍉",
        "⭐",
        "💎"
    ]

    result = [
        random.choice(symbols),
        random.choice(symbols),
        random.choice(symbols)
    ]

    await ctx.send(
        "🎰 **SLOTS**\n\n"
        f"┃ {' | '.join(result)} ┃"
    )

    if (
        result[0] == result[1]
        and result[1] == result[2]
    ):

        reward = random.randint(
            10000,
            25000
        )

        add_coins(
            ctx.author.id,
            reward
        )

        await ctx.send(
            f"🎉 **JACKPOT WIN!**\n"
            f"💰 You received **{reward:,} coins**!"
        )

    elif (
        result[0] == result[1]
        or result[1] == result[2]
    ):

        reward = random.randint(
            1000,
            5000
        )

        add_coins(
            ctx.author.id,
            reward
        )

        await ctx.send(
            f"🟢 **WIN!**\n"
            f"💰 You received **{reward:,} coins**!"
        )

    else:

        await ctx.send(
            "🔴 **LOSS!** 😢\n"
            "No reward this round."
        )


# =========================
# DICE
# =========================

@bot.command()
async def dice(ctx):

    number = random.randint(
        1,
        6
    )

    if number >= 4:

        reward = random.randint(
            2000,
            10000
        )

        add_coins(
            ctx.author.id,
            reward
        )

        await ctx.send(
            f"🎲 You rolled **{number}**\n\n"
            f"🟢 **WIN!**\n"
            f"💰 Reward: **{reward:,} coins**"
        )

    else:

        await ctx.send(
            f"🎲 You rolled **{number}**\n\n"
            "🔴 **LOSS!** 😢"
        )


# =========================
# GUESS
# =========================

@bot.command()
async def guess(ctx, number: int = None):

    if number is None:

        await ctx.send(
            "🎯 Guess a number from **1 to 5**!\n"
            "Example: `?guess 3`"
        )
        return

    if number < 1 or number > 5:

        await ctx.send(
            "❌ Number **1 to 5** ke beech hona chahiye."
        )
        return

    correct = random.randint(
        1,
        5
    )

    if number == correct:

        reward = random.randint(
            5000,
            15000
        )

        add_coins(
            ctx.author.id,
            reward
        )

        await ctx.send(
            f"🎯 Number was **{correct}**!\n"
            f"🟢 **WIN!** 🎉\n"
            f"💰 Reward: **{reward:,} coins**"
        )

    else:

        await ctx.send(
            f"🎯 Number was **{correct}**.\n"
            "🔴 **LOSS!** 😢"
        )


# =========================
# LEADERBOARD
# =========================

@bot.command(
    aliases=["lb", "top"]
)
async def leaderboard(ctx):

    if not coins:

        await ctx.send(
            "🏆 Leaderboard is empty!"
        )
        return

    ranking = sorted(
        coins.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    message = (
        "🏆 **COINS LEADERBOARD** 🏆\n\n"
    )

    for position, (
        user_id,
        balance
    ) in enumerate(
        ranking,
        start=1
    ):

        user = bot.get_user(user_id)

        if user:
            name = user.display_name
        else:
            name = f"User {user_id}"

        message += (
            f"**#{position}** "
            f"{name} — 💰 "
            f"**{balance:,}**\n"
        )

    await ctx.send(message)


# =========================
# HELP
# =========================

@bot.command(name="help")
async def custom_help(ctx):

    message = """
📖 **VIRTUAL COINS BOT**

💰 `?bal`
Check balance.

🎁 `?daily`
50K–100K coins.
Cooldown: 24 hours.

💼 `?work`
Earn coins.

⛏️ `?mine`
💎 Diamond / 💣 Bomb game.

🕵️ `?rob @user`
Rob virtual coins.
Cooldown: 1 hour.

🪙 `?cf`
Coin Flip — Win/Loss.

🎰 `?slots`
Slots — Win/Loss.

🎲 `?dice`
Dice — Win/Loss.

🎯 `?guess 1-5`
Guess the number.

🏆 `?leaderboard`
Top 10 players.

👋 `?hello`
Test bot.

📖 `?help`
Show commands.
"""

    await ctx.send(message)


# =========================
# HELLO
# =========================

@bot.command()
async def hello(ctx):
    await ctx.send(
        "👋 Hello! Bot is working!"
    )


# =========================
# ERROR HANDLER
# =========================

@bot.event
async def on_command_error(
    ctx,
    error
):

    if isinstance(
        error,
        commands.CommandNotFound
    ):
        return

    if isinstance(
        error,
        commands.MissingRequiredArgument
    ):

        await ctx.send(
            "❌ Missing argument.\n"
            "Use `?help` for help."
        )
        return

    if isinstance(
        error,
        commands.BadArgument
    ):

        await ctx.send(
            "❌ Invalid input.\n"
            "Use `?help` for help."
        )
        return

    print(
        f"Command error: {error}"
    )


# =========================
# START BOT
# =========================

bot.run(
    os.getenv("DISCORD_TOKEN")
        )
