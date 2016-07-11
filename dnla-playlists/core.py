import os
import Mutagen


def gather_files(root_path):
    playlist = Playlist()
    for root, dirs, files in os.walk(root_path):
        for f in files:
            playlist.addMediaItem(f)


class Playlist:

    def __init__(self):
        self.items = []

    def addMediaItem(self, filepath):
        self.items.append(Media(filepath))


class Media:

    def __init__(self, filepath):
        file = Mutagen.File(filepath)
        if file:
            self.name = file['title']
            self.artist = file['artist']
        else:
            self.name = os.path.basename(filepath)
        self.path = filepath

