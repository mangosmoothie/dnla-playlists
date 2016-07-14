import mutagen
import os
import re
import sys
from optparse import OptionParser

music_file_exts = ['.mp3', '.wav', '.ogg']
seconds_re = re.compile('(\d+)(\.\d+)? seconds')


def main(argv):
    (options, args) = build_parser().parse_args(argv)
    print('playlist(s) will be written to ', options.outdir)
    predicates = []
    playlists = build_top_10_playlists(options.start_at, predicates, options.extended,
                                       options.absolute, options.depth)
    if not os.path.isdir(options.outdir):
        raise Exception('output directory does not exist!')
    outdir = options.outdir.rstrip(os.path.sep)
    write_playlists(playlists, outdir)


def build_parser():
    parser = OptionParser()
    parser.add_option('-s', '--start-at', dest='start_at', default=os.getcwd(),
                      help='DIR location to start media file search from (default is current DIR)',
                      metavar='DIR')
    parser.add_option('-e', '--extended', dest='extended',
                      action='store_true', default=False,
                      help='use m3u extended format (has additional media metadata)')
    parser.add_option('-a', '--absolute', dest='absolute',
                      action='store_true', default=False,
                      help='use absolute file paths (default is relative paths)')
    parser.add_option('-d', '--depth', dest='depth', type="int", default=-1,
                      help='depth to search, 0 for target dir only (default is fully recursive)')
    parser.add_option('-o', '--outdir', dest='outdir', default=os.getcwd(),
                      help='DIR location of output file(s) (default is current DIR)',
                      metavar='DIR')
    return parser


class Playlist:
    def __init__(self, path, extended, absolute, name):
        self.items = []
        self.predicates = []
        self.path = path
        self.isExtended = extended
        self.isAbsolute = absolute
        self.name = name + '.m3u'

    def __str__(self):
        return 'items: ' + str(self.items)

    def get_out_str(self, item, outdir):
        if self.isExtended:
            raise NotImplementedError('not ready to write extended m3u')
        else:
            return item['path'] if self.isAbsolute else item['path'][len(outdir) + 1:]


def write_playlists(playlists, outdir):
    for p in playlists:
        with open(os.path.join(outdir, p.name), mode='w') as p_out:
            for i in p.items:
                p_out.write(p.jget_out_str(i, outdir))


def all_pass(x, predicates):
    for p in predicates:
        if not p(x):
            return False
    return True


def extract_metadata(path, extended=False):
    meta = {'path': path}
    if extended:
        f = mutagen.File(path)
        if f:
            match = re.search(seconds_re, f.info.pprint())
            meta['seconds'] = match.group(1) if match else '0'
        else:
            f = {}
            meta['seconds'] = '0'
        meta['title'] = f.get('title',
                              [os.path.basename(path)])[0]
        meta['artist'] = f.get('artist',
                               [path.split(os.path.sep)[-2]])[0]
    return meta


def build_top_10_playlists(root_path, predicates, extended, absolute, depth):
    playlists = []
    predicates.append(
        lambda x: re.search('^\d{2}_\d{2} ', os.path.basename(x['path']))
    )
    predicates.append(
        lambda x: int(os.path.basename(x['path'])[3:5]) < 11
    )
    for d in os.listdir(root_path):
        dpath = os.path.join(root_path, d)
        if os.path.isdir(dpath) \
            and re.search('^\d{4}$', d) \
                and 2100 > int(dir) > 1900:

            playlists.append(build_playlist(dpath, predicates,
                                            extended, absolute, 0))
    return playlists


def build_playlist(root_path, predicates, extended, absolute, depth):
    playlist = Playlist(root_path, extended, absolute, os.path.basename(root_path))

    for root, dirs, files in os.walk(root_path):
        for f in files:
            path = os.path.join(root, f)
            if os.path.splitext(path)[1] in music_file_exts:
                item = extract_metadata(path, extended)
                if all_pass(item, predicates):
                    playlist.items.append(item)
    return playlist


if __name__ == "__main__":
    main(sys.argv[1:])
