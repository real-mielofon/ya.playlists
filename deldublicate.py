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
    deleted = 0
    for i, track in enumerate(tracks):
        if track.track.id in uniqueTracks:
            #удалить
            deleted+=1
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
    print("pl: %10s (%10s) - tracks: %3d deleted: %3d"%(pl.title, datetime.datetime.fromisoformat(pl.modified).strftime('%d/%m/#%Y'), pl.track_count, deleted))  # .encode().decode('cp1251')
