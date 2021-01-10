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

#listType = ['PlayListDaily','PlayListMissed', 'PlayListPremiere', 'PlayListDejavu', 'PlayListFamily']
listName = [
'PlayListFamily#20210109',
'PlayListDaily#20210109',
'PlayListPremiere#20210108',
'PlayListDaily#20210108',
'PlayListDejavu#20210107',
'PlayListDaily#20210107',
'PlayListDaily#20210106',
'PlayListMissed#20210105',
'PlayListDaily#20210105',
'PlayListDaily#20210104',
'PlayListDaily#20210103',
'PlayListFamily#20210102',
'PlayListDaily#20210102',
'PlayListPremiere#20210101',
'PlayListDaily#20210101',
'PlayListDejavu#20201231',
'PlayListDaily#20201231',
'PlayListDaily#20201230',
]
allPlaylists = client.usersPlaylistsList()

fullPlayLists = [pl for pl in allPlaylists if pl.title in listName]



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

uniqueTracks = set()
for pl in fullPlayLists:
    tracks = pl.fetch_tracks()
    print("pl: %10s (%10s) - tracks: %3d"%(pl.title, datetime.datetime.fromisoformat(pl.modified).strftime('%d/%m/#%Y'), pl.track_count))  # .encode().decode('cp1251')
    for i, shorttrack in enumerate(tracks):
        track = shorttrack.track
        if not track.available:
            continue

        arTitle = ','.join([ar.name for ar in track.artists])
        dirName = '.\\'+pl.title
        trackName =  arTitle+' - '+track.title
        trackName = slugify(trackName).replace("/","_").replace("\\","_").replace("\'","_")
        trackName = trackName.replace("\"","_").replace("?", "_")
        trackName = trackName.replace("|", "_")
        trackName = trackName.replace(":", "_")
        trackName = trackName[:120]

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
