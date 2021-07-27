from urllib.request import urlopen, Request
from os.path import isfile


class Stream:
    def __init__(self, info, title, progress):
        self._title = title
        self._progress = progress
        self._mime_type, self._codecs = info['mimeType'].split('; ')
        self._file_type = self._mime_type.split('/')[1]
        self._codecs = self._codecs.replace('"', '').split('=')[1]
        self._url = info['url']
        self._filesize = int(urlopen(Request(self.url)).info()['Content-Length'])
        if 'video' in self.mime_type:
            self._type = 'video'
            self._fps = info['fps']
            self._res = info['qualityLabel'].replace(str(info['fps']), '')
            self._abr = None
        elif 'audio' in self.mime_type:
            self._type = 'audio'
            self._abr = f"{round(info['bitrate'] / 1000)}kbps"
            self._fps = None
            self._res = None

    def download(self, path='.', name=None):
        if name is None:
            name = self.title

        if isfile(f'{path}/{name}.{self._file_type}'):
            file = open(f'{path}/{name}.{self._file_type}', 'rb')
            length = 0
            for chunk in iter(lambda: file.read(1024), ''):
                if len(chunk) == 0:
                    break
                else:
                    length += len(chunk)
            file = open(f'{path}/{name}.{self._file_type}', 'ab')
        else:
            length = 0
            file = open(f'{path}/{name}.{self._file_type}', 'ab')

        while length != self._filesize:
            try:
                stop_pos = min(length + 1024 * 1024 - 1, self._filesize)
                chunk = urlopen(Request(self.url, headers={'Range': f'bytes={length}-{stop_pos}'})).read()
                file.write(chunk)
                length += len(chunk)
                self._progress.download(self, length)
            except:
                pass
        self._progress.complete(self)

    def __repr__(self):
        parts = [f'type="{self.type}"', f'mime_type="{self.mime_type}"']
        if self.type == 'audio':
            parts.append(f'abr="{self.abr}"')
        if self.type == 'video':
            parts.append(f'res="{self.res}"')
            parts.append(f'fps="{self.fps}"')
        parts.append(f'codecs="{self.codecs}"')
        return f"<Stream: {' '.join(parts)}>"

    @property
    def title(self):
        return self._title

    @property
    def codecs(self):
        return self._codecs

    @property
    def url(self):
        return self._url

    @property
    def type(self):
        return self._type

    @property
    def mime_type(self):
        return self._mime_type

    @property
    def abr(self):
        return self._abr

    @property
    def res(self):
        return self._res

    @property
    def fps(self):
        return self._fps

    @property
    def filesize(self):
        return self._filesize


class Streams:
    def __init__(self, streams):
        self._streams = streams

    def filter(self, **kwargs):
        streams = self._streams
        for name in kwargs:
            streams = filter(lambda x: x.__dict__[f'_{name}'] == kwargs[name], streams)
        return Streams(list(streams))

    def get_highest(self, type):
        if type == 'video':
            key = lambda stream: (int(stream.res[:-1]), stream.fps)
            return sorted(self.filter(type=type), key=key, reverse=True)[0]
        elif type == 'audio':
            key = lambda stream: int(stream.abr[:-4])
            return sorted(self.filter(type=type), key=key, reverse=True)[0]

    def __getitem__(self, key):
        return self._streams[key]

    def __iter__(self):
        for stream in self._streams:
            yield stream

    def __repr__(self):
        return str(self._streams).replace(',', ',\n')


class Streams:
    def __init__(self, streams):
        self._streams = streams

    def filter(self, **kwargs):
        streams = self._streams
        for name in kwargs:
            streams = filter(lambda x: x.__dict__[f'_{name}'] == kwargs[name], streams)
        return Streams(list(streams))

    def get_highest(self, type):
        if type == 'video':
            key = lambda stream: (int(stream.res[:-1]), stream.fps)
            return sorted(self.filter(type=type), key=key, reverse=True)[0]
        elif type == 'audio':
            key = lambda stream: int(stream.abr[:-4])
            return sorted(self.filter(type=type), key=key, reverse=True)[0]

    def __getitem__(self, key):
        return self._streams[key]

    def __iter__(self):
        for stream in self._streams:
            yield stream

    def __repr__(self):
        return str(self._streams).replace(',', ',\n')

