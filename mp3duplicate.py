import sys
import mutagen.id3
from mutagen.mp3 import EasyMP3 as MP3


import os
import sys

walk_dir = sys.argv[1]

print('walk_dir = ' + walk_dir)

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

dict_mp3 = {}
for root, subdirs, files in os.walk(walk_dir):
  for filename in files:
    file_path = os.path.join(root, filename)
    filename, file_extension = os.path.splitext(file_path)

    if file_extension != '.mp3':
      continue

    trackFileName = file_path
    file = MP3(f'{trackFileName}')
    mp3title = "%s - %s"%(' '.join(file.tags['artist']), ' '.join(file.tags['title']))

    list_files = dict_mp3.get(mp3title, [])
    list_files.append(file_path)
    dict_mp3[mp3title] = list_files

for key in dict_mp3:
  list_files = dict_mp3[key]
  if len(list_files) > 1:
    print("")
    for file_path in dict_mp3[key]:
      print("del \"%s\""%(file_path))