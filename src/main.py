#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
niconicoのVOCALOIDランキングを通知するbotです
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/05/17(Created: 2024/05/17)"

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv



INITIAL_EXTENTIONS = [
    "cogs.set",
    "cogs.delete",
    "cogs.task"
]

Intents = discord.Intents.all()
Intents.message_content = True
Intents.members = True
bot = commands.Bot(command_prefix="!", intents=Intents)


async def main():
    """
    botを起動します。
    """
    load_dotenv()
    async with bot:
        await load_extension()
        await bot.start(os.getenv("TOKEN"))


async def load_extension():
    """
    cogをロードする
    """
    for cog in INITIAL_EXTENTIONS:
        await bot.load_extension(cog)


@bot.event
async def on_message(message):
    """
    messageを受け取ったときの処理
    ここでは、botのメッセージには反応しないことと、コマンドと一致するかの処理を記述
    """

    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_ready():
    """
    起動時の処理
    """

    print("Bot is ready.")


if __name__ == "__main__":
    asyncio.run(main())
