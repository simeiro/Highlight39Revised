#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
sqlite3に関連する処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/05/17(Created: 2024/05/17)"

import sqlite3

import discord


class Sqlite3Process():
    """
    sqlite3の処理
    """

    def __init__(self) -> None:
        pass

    def create_db(self, user_id: int):
        """
        ユーザーのDBを作成します

        :param int user_id: discordのユーザーID
        """

        dbname = f'./data/users/{user_id}.db'
        connect = sqlite3.connect(dbname)
        cursor = connect.cursor()

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS set_channels (
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                UNIQUE(guild_id, channel_id)
            )
            '''
        )

        connect.commit()
        connect.close()

    def set_channel(self, interaction: discord.Interaction):
        """
        ユーザーDBにアクセスし、チャンネルをセットします

        :param discord.Interaction interaction: /setコマンド使用時のdiscord.Interaction
        :return: 既に存在しているデータであればFalse, 存在していなければTrueを返します
        :rtype: bool
        """

        dbname = f'./data/users/{interaction.user.id}.db'
        connect = sqlite3.connect(dbname)
        cursor = connect.cursor()

        guild_id = interaction.guild.id
        channel_id = interaction.channel.id

        try:
            cursor.execute(
                '''
                INSERT INTO set_channels (guild_id, channel_id)
                VALUES (?, ?)
                ''',
                (guild_id, channel_id)
            )

            connect.commit()
            connect.close()
        except sqlite3.IntegrityError:
            connect.close()
            return False

        return True


    def delete_channel(self, interaction: discord.Interaction):
        """
        ユーザーDBにアクセスし、チャンネルを削除します

        :param discord.Interaction interaction: /deleteコマンド使用時のdiscord.Interaction
        :return: 削除できた場合はTrue、できなかった場合はFalseを返します
        :rtype: bool
        """

        dbname = f'./data/users/{interaction.user.id}.db'
        connect = sqlite3.connect(dbname)
        cursor = connect.cursor()

        guild_id = interaction.guild.id
        channel_id = interaction.channel.id

        try:
            cursor.execute(
                '''
                DELETE FROM set_channels
                WHERE guild_id = ? AND channel_id = ?
                ''',
                (guild_id, channel_id)
            )
            deleted_rows = cursor.rowcount
            connect.commit()
            connect.close()

            if deleted_rows == 0:
                return False

        except sqlite3.Error:
            connect.close()
            return False


        return True

    def get_guild_ids_and_channel_ids(self, db: str):
        """
        あるdbのguild_idとchannel_idの辞書の集まりのリストを返します
        [{guild_id: int, channel_id: int}, {guild_id: int, channel_id: int} ...]

        :param db: データベース名
        :return: guild_idとchannel_idの辞書の集まりのリストを返します
        :rtype: List[Dict[str, int]]
        """

        dbname = f'./data/users/{db}'
        connect = sqlite3.connect(dbname)
        cursor = connect.cursor()

        cursor.execute("SELECT guild_id, channel_id FROM set_channels")
        results = cursor.fetchall()

        return_data = []
        for result in results:
            guild_id, channel_id = result
            return_data.append({"guild_id": guild_id, "channel_id": channel_id})

        return return_data
