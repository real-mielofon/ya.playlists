import datetime
import logging
import sys
import os
import unicodedata2
import string
import string

from mutagen import File
from mutagen.id3 import TIT2, TPE1, TALB, APIC, TDRC, USLT

from typing import List

from yandex_music import Playlist
from yandex_music.client import Client
from yandex_music.utils.difference import Difference

DELIMITER = "/"

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

params = [sys.argv[1], sys.argv[2]]

client = Client.from_credentials(params[0], params[1])

albumName = sys.argv[3].split(' - ')
#allPlaylists = client.usersPlaylistsList()
allAlbumsLikeByMe = client.usersLikesAlbums(user_id=client.me.account.uid)


albums = [like.album for like in allAlbumsLikeByMe
          if (like.album.title == albumName[0]) and
          (albumName[1] in [artist.name for artist in like.album.artists])]

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata2
    import re

    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

    tr = {ord(a): ord(b) for a, b in zip(*symbols)}

    # for Python 2.*:
    # tr = dict( [ (ord(a), ord(b)) for (a, b) in zip(*symbols) ] )

    value = value.translate(tr)  # looks good

    value = unicodedata2.normalize('NFKD', value).encode('ascii', 'ignore').decode('utf-8').strip()
#    value = re.sub('[^\w\s-]', '', value).strip().lower()
#    value = re.sub('[-\s]+', '-', value)
    # ...
    return value

def normalizeName(fileName):
    result = slugify(fileName).replace("/","_").replace("\\","_").replace("\'","_")
    result = result.replace("\"","_").replace("?", "_")
    result = result.replace("|", "_")
    result = result.replace(":", "_")
    result = result[:120]
    return result

uniqueTracks = set()
for album in albums:
    if not album.available:
        continue
    for tracks in album.withTracks().volumes:
        print("pl: %10s - tracks: %3d" % (album.title, album.track_count))  # .encode().decode('cp1251')
        for i, track in enumerate(tracks):
            if not track.available:
                continue

            arTitle = ','.join([ar.name for ar in track.artists])

            dirName = '.\\'+normalizeName(f'{arTitle} - {album.title} ({album.year})')
            trackName =  normalizeName(track.title)\

            if trackName in uniqueTracks:
                continue
            else:
                uniqueTracks.add(trackName)
            os.makedirs(dirName, exist_ok=True)

            trackFileName = f'{dirName}\\{i+1:02d}-{trackName}.mp3'

            if not os.path.isfile(trackFileName) :
                print("%3d  %s" % (i+1, trackFileName))
                try:
                    track.download(filename=trackFileName)
                except:
                    print("Error!!")

            file = File(f'{trackFileName}')
            file.update({
                # Title
                'TIT2': TIT2(encoding=3, text=track.title),
                # Artist
                'TPE1': TPE1(encoding=3, text=DELIMITER.join(i['name'] for i in track.artists)),
                # Album
                'TALB': TALB(encoding=3, text=DELIMITER.join(i['title'] for i in track.albums)),
                # Year
                'TDRC': TDRC(encoding=3, text=str(track.albums[0]['year'])),
                # Picture
                #'APIC': APIC(encoding=3, text=cover_filename, data=open(cover_filename, 'rb').read())
            })

            file.save()

#        else:
#            # print("%3d  %s file exist!" % (i+1, trackFileName))
#    client.users_playlists_change(pl.kind, diff.to_json(), pl.revision)
