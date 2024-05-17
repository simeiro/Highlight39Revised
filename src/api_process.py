#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
apiに関連する処理
"""

__author__ = "simeiro"
__version__ = "0.0.0"
__date__ = "2024/05/17(Created: 2024/05/17)"

from datetime import datetime, timedelta

import discord
import requests



class ApiProcess():
    """
    apiの処理に関連するclassです
    """

    def __init__(self) -> None:
        pass

    def _get_vocaloid_file_name(self):
        """
        niconicoのVOCALOIDランキングのjsonファイル名を取得します
        例: https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/daily/2024-05-17/file_name_list.json

        :return: jsonファイル名
        :rtype: str
        """

        before_one_day = datetime.now() -timedelta(days=1)
        before_one_day = before_one_day.strftime("%Y-%m-%d")
        url = (
            f'https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/daily/'
            f'{before_one_day}/file_name_list.json'
        )
        responce = requests.get(url, timeout=10)
        json = responce.json()

        file = ''
        for genre in json:
            if genre['tag'] == 'VOCALOID':
                file = genre['file']
                break

        return file

    def _get_youtube_url_by_niconico_url(self, nico_url: str):
        """
        niconicoのurlを元にしてyoutubeのurlを取得します

        :param nico_url: niconicoのurl
        :return: youtubeのurl
        :rtype: str
        """
        api_url = 'https://vocadb.net/api/songs?query=' + nico_url + '&fields=PVs'
        responce = requests.get(api_url, timeout=10)
        json = responce.json()

        youtube_url = 'YouTubeURLなし'
        for pv in json["items"][0]["pvs"]:
            if pv['service'] == 'Youtube':
                youtube_url = pv['url']
                break

        return youtube_url

    def _get_ranking_json(self, file_name: str):
        """
        niconicoのランキングのjsonファイルを取得します
        例: https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/daily/2024-05-17/music_sound_02.json

        :param file_name: 使用するランキングのjsonファイル名
        :return: niconicoのランキングのjsonファイルを返します
        :rtype: json
        """
        before_one_day = datetime.now() -timedelta(days=1)
        before_one_day = before_one_day.strftime("%Y-%m-%d")
        url = f'https://dcdn.cdn.nimg.jp/nicovideo/old-ranking/daily/{before_one_day}/{file_name}'
        responce = requests.get(url, timeout=10)
        json = responce.json()

        return json

    def get_ranking_embeds(self):
        """
        1~5位までのランキングデータをembed形式でまとめて返します

        :return: embedデータをlistで返します
        :rtype: List[discord.Embed]
        """
        file_name = self._get_vocaloid_file_name()
        json = self._get_ranking_json(
            file_name=file_name
        )

        embeds = []
        for i, song in enumerate(json):
            if i >= 5:
                break
            niconico_url = 'https://www.nicovideo.jp/watch/'+ song['id']
            youtube_url = self._get_youtube_url_by_niconico_url(
                nico_url=niconico_url
            )

            embed = discord.Embed(
                title=f'{i+1}位  {song["title"]}',
                description = (
                    f'再生数: {song["count"]["view"]}\n'
                    f'[youtube](<{youtube_url}>)\n'
                    f'[niconico](<{niconico_url})'
                )
            )
            embed.set_thumbnail(url=song['thumbnail']['url'])

            embeds.append(embed)

        return embeds
