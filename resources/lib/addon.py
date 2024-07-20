from __future__ import absolute_import, division, unicode_literals
from typing import Union
from routing import Plugin
import sys
from apiProxy import apiRequest
from urllib.parse import urlencode
from config import ENDPOINTS
import json
import xbmc
import xbmcgui
import xbmcplugin

plugin = Plugin()
URL = sys.argv[0]

@plugin.route('/')
def main_menu() -> None:
    xbmcplugin.setPluginCategory(plugin.handle, 'Главное меню')
    xbmcplugin.setContent(plugin.handle, 'movies')
    xbmcplugin.addSortMethod(plugin.handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)

    menuItems: dict = [
        {"label": "Домашняя", "uri": "home"},
        {"label": "Поиск", "uri": "search"},
        {"label": "Закладки", "uri": "bookmarks"},
        {"label": "Избранное", "uri": "favorites"},
        {"label": "История", "uri": "history"}
    ]

    for item in menuItems:
        is_folder = True
        list_item = xbmcgui.ListItem(label=item['label'])
        info_tag: xbmc.InfoTagVideo = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(item['label'])
        info_tag.setGenres([item['label']])
        url = f"{URL}/{item['uri']}"
        xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, is_folder)

    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/home')
def homePage() -> None:
    xbmcplugin.setPluginCategory(plugin.handle, 'Домашняя')
    xbmcplugin.setContent(plugin.handle, 'movies')
    xbmcplugin.addSortMethod(plugin.handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)

    menuItems: dict = [
        {"label": "Последнее", "uri": "0"},
        {"label": "В эфире", "uri": "2"},
        {"label": "Анонсировано", "uri": "3"},
        {"label": "Завершено", "uri": "1"},
    ]

    for index, item in enumerate(menuItems):
        is_folder = True
        list_item = xbmcgui.ListItem(label=item['label'])
        info_tag: xbmc.InfoTagVideo = list_item.getVideoInfoTag()
        info_tag.setMediaType('video')
        info_tag.setTitle(item['label'])
        info_tag.setGenres([item['label']])
        url = f"{URL}/{item['uri']}?page=0"
        xbmcplugin.addDirectoryItem(plugin.handle, url, list_item, is_folder)

    xbmcplugin.endOfDirectory(plugin.handle)


def addReleaseToDirectory(pluginHandle, item):
    is_folder = True
    genres: list = []
    if item['genres']:
        genres = item['genres'].split(', ')

    episodes_released = ""
    episodes_total = "? эп."
    if item['episodes_total']:
        episodes_released = f"{item['episodes_released']}/"
    if item['episodes_total']:
        episodes_total = f"{item['episodes_total']} эп."

    description = f"{episodes_released}{episodes_total}\n{item['description']}"

    list_item = xbmcgui.ListItem(label=f"{item['title_ru']}")
    list_item.setArt({'poster': item['image']})
    info_tag: xbmc.InfoTagVideo = list_item.getVideoInfoTag()
    info_tag.setMediaType('movie')
    info_tag.setTitle(item['title_ru'])
    info_tag.setGenres(genres)
    info_tag.setRating(item['grade'], item['vote_count'])
    info_tag.setPlot(description)
    info_tag.setCountries([item['country'] or "Неизвестно"])
    info_tag.setDirectors([f"Режиссёр: {item['director'] or 'Неизвестно'}", f"Автор: {item['author'] or 'Неизвестно'}"])
    info_tag.setStudios([item['studio'] or "Неизвестно"])
    if item['status']:
        info_tag.setTvShowStatus(item['status']['name'])
    if item['year']:
        info_tag.setYear(int(item['year']))
    url = f"{URL}/release/{item['id']}"
    info_tag.setDuration(item['duration'] * 60)
    xbmcplugin.addDirectoryItem(pluginHandle, url, list_item, is_folder)


@plugin.route('/home/<listId>')
def homeListPage(listId: str):

    page: int = int(plugin.args['page'][0])
    listId: Union[None, int] = int(listId)

    xbmcplugin.setPluginCategory(plugin.handle, 'Последние релизы')
    xbmcplugin.setContent(plugin.handle, 'movies')
    xbmcplugin.addSortMethod(plugin.handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(plugin.handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.addSortMethod(plugin.handle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmcplugin.addSortMethod(plugin.handle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING)

    if listId == 0:
        listId = None

    data = json.dumps(
            {
                "country": None,
                "season": None,
                "sort": 0,
                "studio": None,
                "age_ratings": [],
                "category_id": None,
                "end_year": None,
                "episode_duration_from": None,
                "episode_duration_to": None,
                "episodes_from": None,
                "episodes_to": None,
                "genres": [],
                "profile_list_exclusions": [],
                "start_year": None,
                "status_id": listId,
                "types": [],
                "is_genres_exclude_mode_enabled": False,
            })
    response = apiRequest(f"{ENDPOINTS['filter']}/{page}", "POST", data)

    for item in response['content']:
        addReleaseToDirectory(plugin.handle, item)

    list_item = xbmcgui.ListItem(label=f"Следующая страница ({page + 2})")
    xbmcplugin.addDirectoryItem(plugin.handle, f"{URL}?page={page + 1}", list_item, True)

    xbmcplugin.endOfDirectory(plugin.handle)


def run(argv):
    ''' Addon entry point from wrapper '''
    plugin.run(argv)