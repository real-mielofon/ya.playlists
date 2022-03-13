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

allAlbumsLikeByMe = client.usersLikesAlbums(user_id=client.me.account.uid)


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


for i, album in enumerate([like.album for like in allAlbumsLikeByMe if like.type == 'album']):
    print("  \"%s - %s\" (%s)" % (album.title, album.artists[0].name if len(album.artists)>0 else 'NONE', album.year))
