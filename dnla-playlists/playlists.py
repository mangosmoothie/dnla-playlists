import mutagen
import os
import re
import sys
from optparse import OptionParser

music_file_exts = ['.mp3', '.wav', '.ogg']
seconds_re = re.compile('(\d+)(\.\d+)? seconds')


def main(argv):
    (options, args) = build_parser().parse_args(argv)
    validate_options(options)
    print('playlist(s) will be written to ', options.outdir)
    if not options.contains and not options.regex:
        playlists = build_top_10_playlists(options.start_at, [], options.extended,
                                           options.absolute, options.depth)
    else:
        predicates = build_match_predicates(options.contains, options.regex)
        playlists = [build_playlist(options.start_at, predicates, options.extended,
                                    options.absolute, options.depth, options.name)]
    outdir = options.outdir.rstrip(os.path.sep)
    write_playlists(playlists, outdir)


def build_match_predicates(contains, regex):
    predicates = []
    if contains:
        c = contains.lower()
        predicates.append(
            lambda x: c in os.path.basename(x['path']).lower() or c in x['title'].lower() or c in x['artist'].lower()
        )
    if regex:
        r = re.compile(regex)
        predicates.append(
            lambda x: re.search(r, os.path.basename(x['path'])) or re.search(r, x['title']) or re.search(r, x['artist'])
        )
    return predicates


def build_parser():
    parser = OptionParser()
    parser.add_option('-n', '--name', dest='name', default=os.path.basename(os.getcwd()),
                      help='NAME of playlist', metavar='NAME')
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
    parser.add_option('-c', '--contains', dest='contains', default=None,
                      help='case insensitive match on given string, i.e. "string contains SUBSTR". ' +
                           'Checks file names and metadata.', metavar='SUBSTR')
    parser.add_option('-r', '--regex', dest='regex', default=None,
                      help='regex match. checks file name and metadata',
                      metavar='EXP')
    parser.add_option('-f', '--force', dest='force', default=False,
                      action='store_true', help='force execution through warnings')
    return parser


def validate_options(options):
    if not os.path.isdir(options.outdir):
        print('output directory does not exist!')
        sys.exit(1)
    if not os.path.isdir(options.start_at):
        print('starting directory does not exist!')
        sys.exit(1)
    if options.depth != -1:
        print('invalid depth: ' + str(options.depth))
        sys.exit(1)
    if os.path.exists(
            os.path.join(options.outdir,
                         options.name if options.name.endswith('.m3u') else options.name + '.m3u')):
        if options.force:
            print('overwriting playlist: ' + options.name)
        else:
            print('playlist already exists with name: ' + options.name)
            print('run with option -f to overwrite existing playlist')
            sys.exit(1)


class Playlist:
    def __init__(self, path, extended, absolute, name):
        self.items = []
        self.predicates = []
        self.path = path
        self.isExtended = extended
        self.isAbsolute = absolute
        self.name = name + '.m3u'

    def __str__(self):
        return self.name + ' items: ' + str(len(self.items))

    def get_out_str(self, item, outdir):
        x = 0
        if not self.isAbsolute:
            while x < len(outdir) and x < len(item['path']) \
                    and outdir[x] == item['path'][x]:
                x += 1
        if x == 0:
            x = -1
        if self.isExtended:
            return '\n' + '#EXTINF:' + item['seconds'] + ', ' + item['artist'] + ' - ' + item['title'] \
                   + '\n' + item['path'][x + 1:]
        else:
            return '\n' + item['path'][x + 1:]


def write_playlists(playlists, outdir):
    for p in playlists:
        print('writing playlist: ' + str(p))
        with open(os.path.join(outdir, p.name), mode='w') as p_out:
            if p.isExtended:
                p_out.write('#EXTM3U')
            else:
                p_out.write('#STDM3U')
            for i in p.items:
                p_out.write(p.get_out_str(i, outdir))


def all_pass(x, predicates):
    for p in predicates:
        if not p(x):
            return False
    return True


def extract_metadata(path, extended=False):
    meta = {'path': path, 'title': '', 'artist': '', 'seconds': '0'}
    if extended:
        f = mutagen.File(path)
        if f:
            match = re.search(seconds_re, f.info.pprint())
            meta['seconds'] = match.group(1) if match else '0'
        else:
            f = {}
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
                and 2100 > int(d) > 1900:
            playlists.append(build_playlist(dpath, predicates,
                                            extended, absolute,
                                            0, os.path.basename(dpath)))
    return playlists


def build_playlist(root_path, predicates, extended, absolute, depth, name):
    playlist = Playlist(root_path, extended, absolute, name)

    for root, dirs, files in os.walk(root_path):
        for f in files:
            path = os.path.join(root, f)
            if os.path.splitext(path)[1].lower() in music_file_exts:
                item = extract_metadata(path, extended)
                if all_pass(item, predicates):
                    playlist.items.append(item)
    return playlist


if __name__ == "__main__":
    main(sys.argv[1:])
