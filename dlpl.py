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

#listType = ['PlayListDaily','PlayListMissed', 'PlayListPremiere', 'PlayListDejavu', 'PlayListFamily']
listType = ['PlayListPremiere']
allPlaylists = client.usersPlaylistsList()
fullPlayLists = [pl for pl in allPlaylists if pl.title in listType]

for pl in fullPlayLists:
    tracks = pl.fetch_tracks()
    uniqueTracks = set()
    for i, track in enumerate(tracks):
        dirName = '.\\'+pl.title+'.\\'+track.track. track.track.title
        track.track.download()
    client.users_playlists_change(pl.kind, diff.to_json(), pl.revision)
    print("pl: %10s (%10s) - tracks: %3d deleted: %3d"%(pl.title, datetime.datetime.fromisoformat(pl.modified).strftime('%d/%m/#%Y'), pl.track_count, deleted))  # .encode().decode('cp1251')
