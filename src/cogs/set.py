#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
/setコマンドの処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/05/17(Created: 2024/05/17)"

import discord
from discord.ext import commands
from discord import app_commands

from sqlite3_process import Sqlite3Process

class Set(commands.Cog):
    """
    /setコマンドの処理を記述したクラスです
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set", description="通知するチャンネルをセットします")
    async def set_channel(self, interaction: discord.Interaction):
        """
        通知するチャンネルをセットします
        """
        sqlite3_process_instance = Sqlite3Process()
        sqlite3_process_instance.create_db(user_id=interaction.user.id)
        if sqlite3_process_instance.set_channel(interaction=interaction):
            await interaction.response.send_message("チャンネルをセットしました")
        else:
            await interaction.response.send_message("既にセットされています")

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """

        await self.bot.tree.sync()
        print('loaded : set.py')


async def setup(bot: commands.Bot):
    """
    Setのcogを追加します
    """
    await bot.add_cog(Set(bot))
