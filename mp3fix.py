import sys
import mutagen.id3

trackFileName = sys.argv[1]
file = mutagen.id3.ID3(f'{trackFileName}')
print(file.version)
for key, value in file.items():
    if key in ['TIT2', 'TPE1']:
        print(value.encoding, ', '.join(value.text).encode('utf8'))
file.save(v1=2, v2_version=3)
