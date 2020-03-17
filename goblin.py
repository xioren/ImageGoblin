import os
from time import sleep
from gzip import decompress
from io import DEFAULT_BUFFER_SIZE
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from parsing import *


class MetaGoblin:

    def __init__(self, url, tickrate, verbose, nodl):
        self.url = url
        self.tickrate = tickrate
        self.verbose = verbose
        self.nodl = nodl
        self.main_path = os.path.join(os.getcwd(), 'web_goblin')
        self.headers = {'User-Agent': 'Firefox/72',
                        'Accept-Encoding': 'gzip'}
        if not self.nodl:
            self.create_folders(self.main_path)

    def create_folders(self, path):
        '''
        creates directories
        '''
        if os.path.exists(path) is False:
            os.makedirs(path)

    def cleanup(self, path):
        '''
        cleanup unwanted files (icons, erroneous, etc...)
        default 50kb threshhold
        '''
        # TODO: dangerous, consider recieving file manifest instead?
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            if os.path.getsize(filepath) < 50000:
                try:
                    os.remove(filepath)
                except PermissionError as e:
                    print(f'[cleanup error] {e}')
                    continue

    def retrieve(self, url, path, mode='wb'):
        '''
        retrieve web content
        '''
        request = Request(url, None, self.headers)
        try:
            with urlopen(request, timeout=10) as response:
                with open(path, mode) as file:
                    while True:
                        data = response.read(DEFAULT_BUFFER_SIZE)
                        if not data:
                            break
                        if response.info().get('Content-Encoding') == 'gzip':
                            try:
                                data = decompress(data)
                            except OSError:
                                pass
                        file.write(data)
        except HTTPError as e:
            if self.verbose:
                print(f'[{e}] {url}')
            return None
        print(f'[success] {url}')
        return True

    def get_html(self, url):
        request = Request(url, None, self.headers)
        try:
            with urlopen(request, timeout=10) as response:
                html = response.read()
                if response.info().get('Content-Encoding') == 'gzip':
                    try:
                        html = decompress(html)
                    except OSError:
                        pass
        except HTTPError as e:
            if self.verbose:
                print(f'[{e}] {url}')
            return None
        return html.decode()

    def make_unique(self, filename):
        '''
        make filename unique
        '''
        n = 1
        while True:
            unique = f'({n}).'.join(filename.split('.'))
            if os.path.exists(unique):
                n += 1
            else:
                return unique

    def write_file(self, data, path, mode='w', iter=False):
        '''
        write to disk
        '''
        try:
            with open(path, mode) as file:
                if iter:
                    for item in data:
                        file.write(f'{item}\n')
                else:
                    file.write(data)
        except OSError as e:
            print(f'[write error] {e}')

    def read_file(self, path, mode=None):
        '''
        read txt file
        '''
        try:
            with open(path, 'r') as file:
                if mode == 'iter':
                    return file.readlines()
                else:
                    return file.read()
        except OSError as e:
            print(f'[read error] {e}')

    def move_vid(self, path):
        '''
        move videos into seperate directory
        '''
        dirpath = os.path.join(path, 'vid')
        if os.path.exists(dirpath) is False:
            os.mkdir(dirpath)
        for file in os.listdir(path):
            if '.mp4' in file:
                os.rename(os.path.join(path, file), os.path.join(dirpath, file))
