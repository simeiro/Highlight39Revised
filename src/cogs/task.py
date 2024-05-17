#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@tasks.loopに関する処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/05/17(Created: 2024/05/17)"

import os
import sys
from discord.ext import commands, tasks

from sqlite3_process import Sqlite3Process
from api_process import ApiProcess




class Task(commands.Cog):
    """
    一定周期処理を記述したクラスです
    """

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=24)
    async def send_ranking(self):
        """
        ランキングデータを送信します
        """
        mainpy_path = sys.argv[0].replace('main.py', '')
        users_path = '../data/users'
        users_db = os.listdir(mainpy_path + users_path)
        api_process_instance = ApiProcess()
        sqlite3_process_instance = Sqlite3Process()

        embeds = api_process_instance.get_ranking_embeds()

        for user_db in users_db:
            ids_list = sqlite3_process_instance.get_guild_ids_and_channel_ids(db=user_db)
            for ids in ids_list:
                guild = self.bot.get_guild(ids['guild_id'])
                channel = guild.get_channel(ids['channel_id'])
                for embed in embeds:
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        bot起動時にロードしていることを確認するためにprintします
        """

        self.send_ranking.start()

        print('loaded : task.py')


async def setup(bot: commands.Bot):
    """
    Taskのcogを追加します
    """
    await bot.add_cog(Task(bot))
