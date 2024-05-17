#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
/deleteコマンドの処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/05/17(Created: 2024/05/17)"

import discord
from discord.ext import commands
from discord import app_commands

from sqlite3_process import Sqlite3Process




class Delete(commands.Cog):
    """
    /deleteコマンドの処理を記述したクラスです
    """

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete", description="セット情報を削除します")
    async def delete_channel_data(self, interaction: discord.Interaction):
        """
        セット情報を削除します
        """
        sqlite3_process_instance = Sqlite3Process()
        sqlite3_process_instance.create_db(user_id=interaction.user.id)
        if sqlite3_process_instance.delete_channel(interaction=interaction):
            await interaction.response.send_message("セットを解除しました")
        else:
            await interaction.response.send_message("データが存在しません")


    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """

        await self.bot.tree.sync()
        print('loaded : delete.py')


async def setup(bot: commands.Bot):
    """
    Deleteのcogを追加します
    """
    await bot.add_cog(Delete(bot))
