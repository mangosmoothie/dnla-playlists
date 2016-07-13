import mutagen
import os
import re
import sys
import getopt

music_file_exts = ['.mp3', '.wav', '.ogg']
seconds_re = re.compile('(\d+)(\.\d+)? seconds')


def main(argv):
    extended, absolute = False
    outdir = os.getcwd()
    try:
        opts, args = getopt.getopt(argv, "he:a:o:", ["extended=", "absolute=", "outdir="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    if len(opts) == 0:
        print_usage()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-e", "--extended"):
            extended = True
        elif opt in ("-a", "--absolute"):
            absolute = True
        elif opt in ("-o", "--outdir"):
            outdir = arg

    print('playlist(s) will be written to ', outdir)
    predicates = [lambda x: os.path.splitext(x['path'])[1] in music_file_exts]
    playlist = build_playlist(os.getcwd(), predicates, extended)
    #finish


class Playlist:

    def __init__(self, path, extended=False, relative=True):
        self.items = []
        self.predicates = []
        self.path = path
        self.isExtended = extended
        self.isRelative = relative


def all_pass(x, predicates):
    for p in predicates:
        if not p(x):
            return False
    return True


def extract_metadata(path, extended=False):
    meta = {'path': path}
    if extended:
        f = mutagen.File(path) or {}
        meta['title'] = f.get('title',
                              os.path.basename(path))
        meta['artist'] = f.get('artist',
                               path.split(os.path.sep)[-2])
        match = re.search(seconds_re, f.info.pprint())
        meta['seconds'] = match.group(1) if match else '0'
    return meta


def build_playlist(root_path, predicates, extended):
    playlist = Playlist(root_path, extended)

    for root, dirs, files in os.walk(root_path):
        for f in files:
            item = extract_metadata(f, extended)
            if all_pass(item, predicates):
                playlist.items.append(item)
    return playlist


def print_usage():
    print('usage: core.py [-ea] [-o path-to-dir]')
    print('-h for help')


def print_help():
    print('')
    print('builds dlna playlists')
    print('')
    print('params: -e --extended  use m3u extended format (has additional media metadata)')
    print('params: -a --absolute  use absolute file paths [default is relative paths]')
    print('params: -o --outdir    location of output file(s) [default is current dir]')
    print('')
    print_usage()


if __name__ == "__main__":
    main(sys.argv[1:])
