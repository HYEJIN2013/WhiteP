from datetime import datetime
import shutil
import textwrap

import requests

API_URL = 'https://aur.archlinux.org/rpc/?v=5'


def format_text(text, color=None, bold=False):
    text = str(text)
    result = ''
    if color is not None:
        result += '\x1b[38;5;%dm' % color
    if bold:
        result += '\x1b[1m'
    result += text
    result += '\x1b[0m'
    return result


class Package:
    def __init__(self, values):
        self.name = values.get('Name', None)
        self.version = values.get('Version', None)
        self.description = values.get('Description', None)
        self.url = values.get('URL', None)
        self.aur_url = values.get('URLPath', None)
        self.make_dependencies = values.get('MakeDepends', [])
        self.dependencies = values.get('Depends', [])
        self.maintainer = values.get('Maintainer')
        self.votes = values.get('NumVotes')
        self.opt_dependencies = values.get('OptDepends', [])
        self.last_modified = values.get('LastModified', 0)

        self.licenses = values.get('Licenses', [])
        self.architecture = values.get('Architecture', None)

    def get_info(self):
        res = requests.get(API_URL, params={
            'type': 'info',
            'arg': self.name
        }).json()
        if res['resultcount'] == 0:
            return
        self.__init__(res['results'][0])

    def to_str(self, include_desc=True, colorize=False):
        repo = 'aur/'
        name = self.name
        version = self.version
        votes = '(' + str(self.votes) + ')'
        description = self.description

        if colorize:
            repo = format_text(repo, color=5, bold=True)
            name = format_text(name, bold=True)
            version = format_text(version, color=2, bold=True)
            votes = format_text(votes, color=3, bold=True)

        fmt = None
        if include_desc:
            fmt = '{repo}{name} {version} {votes}\n    {description}'
        else:
            fmt = '{name} {version}'

        return fmt.format(**locals())

    def time_str(self, ts):
        dt = datetime.fromtimestamp(ts)
        return dt.strftime('%a %d %b %Y %T %p')

    def to_info_str(self, colorize=False):
        pairs = (
            ('Name', self.name),
            ('Version', self.version),
            ('Description', self.description),
            ('Architecture', self.architecture),
            ('URL', self.url),
            ('Licenses', '  '.join(self.licenses)),
            ('Depends On', '  '.join(sorted(self.make_dependencies +
                                            self.dependencies))),
            ('Optional Deps', '  '.join(self.opt_dependencies)),
            ('Maintainer', self.maintainer),
            ('Last Modified', self.time_str(self.last_modified)),
        )
        mkey_len = max(len(e[0]) for e in pairs)
        tw_indent = ' ' * (mkey_len + 4)
        result = []
        for e in pairs:
            left = e[0] + ' ' * (mkey_len - len(e[0]) + 2) + ':'
            left = format_text(left, bold=True)
            right = textwrap.wrap(str(e[1]), subsequent_indent=tw_indent,
                                  width=shutil.get_terminal_size((70, 0))
                                  .columns - len(tw_indent))
            result.append(left + ' ' + '\n'.join(right))
        return '\n'.join(result)


def search(keywords):
    keywords = tuple(filter(None, [e.lower() for e in keywords.split()]))
    keywords = tuple(e for e in keywords if len(e) > 1)

    res = requests.get(API_URL, params={
        'type': 'search',
        'arg': keywords
    }).json()

    matches = res['results']

    if len(keywords) > 1:
        upd_matches = []
        for e in matches:
            match_str = ''
            for key in ('Description', 'Name'):
                val = e.get(key, '')
                if not isinstance(val, str):
                    continue
                match_str += val
            match_str = match_str.lower()
            if all(term in match_str for term in keywords):
                upd_matches.append(e)
        matches = upd_matches
    return list(map(Package, matches))

if __name__ == '__main__':
    import sys

    pkgs = search(sys.argv[1])
    pkgs = sorted(pkgs, key=lambda e: e.votes, reverse=True)

    for e in pkgs:
        print(e.to_str(colorize=True))
