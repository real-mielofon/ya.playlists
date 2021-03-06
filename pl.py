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
# print(client)

listType = [
    ('yamusic-daily', 'PlayListDaily'),
    ('yamusic-missed', 'PlayListMissed'),
    ('yamusic-premiere', 'PlayListPremiere'),
    ('yamusic-dejavu', 'PlayListDejavu'),
    ('yamusic-family', 'PlayListFamily')
]
allPlaylists = client.usersPlaylistsList()
for plName, plPrefix in listType:
    pls = client.usersPlaylistsList(plName)
    for playListFrom in pls:
        newPlayListName = plPrefix + datetime.datetime.fromisoformat(playListFrom.modified).strftime('#%Y%m%d')
        print(playListFrom.title, ' ', newPlayListName)  # .encode().decode('cp1251')

        fullPLList: List[Playlist] = [tPl for tPl in allPlaylists if plPrefix == tPl.title]
        if len(fullPLList) > 0:
            fullPL = fullPLList[0]
        else:
            fullPL = client.usersPlaylistsCreate(plPrefix)

        tracksShort = playListFrom.fetchTracks()
        trackInFullPL = set([track.track.id for track in fullPL.fetchTracks()])
        json = []
        jsonForFull = []
        for track in tracksShort:
            json = json + [{'id': track.track.id, 'album_id': track.track.albums[0].id}]
            if not track.track.id in trackInFullPL:
                jsonForFull += [{'id': track.track.id, 'album_id': track.track.albums[0].id}]

        newpls: List[Playlist] = [tPl for tPl in allPlaylists if newPlayListName == tPl.title]
        findPL = len(newpls) > 0
        if findPL:
            print('уже есть такой')
        else:
            # Создаём новый плейлист
            playlistNew = client.usersPlaylistsCreate(newPlayListName)

            diff = Difference().add_insert(0, json)
            client.users_playlists_change(playlistNew.kind, diff.to_json())

        # в суммарный
        diff = Difference().add_insert(fullPL.track_count, jsonForFull)
        client.users_playlists_change(fullPL.kind, diff.to_json(), revision=fullPL.revision)
