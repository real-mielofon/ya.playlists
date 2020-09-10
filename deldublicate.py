import datetime
import logging
import sys
from typing import List

from yandex_music import Playlist
from yandex_music.client import Client
from yandex_music.utils.difference import Difference

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

params = [sys.argv[1], sys.argv[2]]

client = Client.from_credentials(params[0], params[1])

listType = ['PlayListDaily','PlayListMissed', 'PlayListPremiere', 'PlayListDejavu', 'PlayListFamily']
allPlaylists = client.usersPlaylistsList()
fullPlayLists = [pl for pl in allPlaylists if pl.title in listType]

for pl in fullPlayLists:
    tracks = pl.fetch_tracks()
    uniqueTracks = set()
    diff = Difference()
    first = -1
    for i, track in enumerate(tracks):
        if track.track.id in uniqueTracks:
            #удалить
            if first < 0:
                first = i
        else:
            if first >= 0:
                diff.add_delete(first, i)
            first = -1
            uniqueTracks.add(track.track.id)
    if first >= 0:
        diff.add_delete(first, len(tracks))

    client.users_playlists_change(pl.kind, diff.to_json(), pl.revision)