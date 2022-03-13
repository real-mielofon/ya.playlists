import datetime
import logging
import sys
import os

from mutagen import File
from mutagen.id3 import TIT2, TPE1, TALB, TDRC

from yandex_music.client import Client

DELIMITER = "/"

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

params = [sys.argv[1], sys.argv[2]]

client = Client.from_credentials(params[0], params[1])

listArtists = sys.argv[3:]

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata2

    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

    tr = {ord(a): ord(b) for a, b in zip(*symbols)}

    value = value.translate(tr)  # looks good

    value = unicodedata2.normalize('NFKD', value).encode('ascii', 'ignore').decode('utf-8').strip()
    return value


uniqueTracks = set()

for artistName in listArtists:

    artistSearch = client.search(artistName, type_='artist')
    if artistSearch.artists.total <= 0:
        exit(-1)

    artist = artistSearch.artists.results[0]
    albums = artist.getAlbums(page_size=20)


    print("Artist: %s - albums: %3d" % (
        artist.name, len(albums)))
    for i, album in enumerate(albums):
        print("  \"%s - %s\" (%s)"%(album.title, artist.name, album.year))