import os
from time import sleep
from gzip import decompress
from io import DEFAULT_BUFFER_SIZE
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from parsing import *
from meta_sources import *


class MetaGoblin:

    def __init__(self, url, tickrate, verbose, nodl):
        self.url = url
        self.tickrate = tickrate
        self.verbose = verbose
        self.nodl = nodl
        self.path_main = os.path.join(os.getcwd(), 'goblin_loot')
        self.external_links = os.path.join(os.getcwd(), 'links.txt')
        self.headers = {'User-Agent': 'GoblinTeam/1.2',
                        'Accept-Encoding': 'gzip'}
        if not self.nodl:
            self.make_dirs(self.path_main)

    def make_dirs(self, *paths):
        '''
        creates directories
        '''
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

    def cleanup(self, path):
        '''
        cleanup small unwanted files (icons, erroneous, etc...)
        default 50kb threshold
        '''
        # TODO: dangerous, consider recieving file manifest instead?
        for file in os.listdir(path):
            filepath = os.path.join(path, file)
            if os.path.isdir(filepath):
                continue
            if os.path.getsize(filepath) < 50000:
                try:
                    os.remove(filepath)
                except PermissionError as e:
                    print(f'[{self.__str__()}] <cleanup error> {e}')
                    continue

    def retrieve(self, url, path, wait):
        '''
        retrieve web content
        '''
        request = Request(url, None, self.headers)
        try:
            with urlopen(request, timeout=wait) as response:
                with open(path, 'wb') as file:
                    while True:
                        data = response.read(DEFAULT_BUFFER_SIZE)
                        if not data:
                            break
                        if response.info().get('Content-Encoding') == 'gzip':
                            try:
                                data = decompress(data)
                            except OSError:
                                pass
                            except EOFError:
                                return None
                        file.write(data)
        except HTTPError as e:
            if self.verbose:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        except URLError as e:
            if self.verbose:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        return True

    def get_html(self, url, wait=10):
        '''
        retrieve web page html
        '''
        request = Request(url, None, self.headers)
        try:
            with urlopen(request, timeout=wait) as response:
                html = response.read()
                if response.info().get('Content-Encoding') == 'gzip':
                    try:
                        html = decompress(html)
                    except OSError:
                        pass
                    except EOFError:
                        return None
        except HTTPError as e:
            if self.verbose:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        except URLError as e:
            if self.verbose:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        return html.decode('utf-8', 'ignore')

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
            print(f'[{self.__str__()}] <write error> {e}')

    def read_file(self, path, iter=False):
        '''
        read txt file
        '''
        # NOTE: unused
        try:
            with open(path, 'r') as file:
                if iter:
                    return file.read().splitlines()
                else:
                    return file.read()
        except OSError as e:
            print(f'[{self.__str__()}] <read error> {e}')

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

    def is_duplicate(self, path, url):
        '''
        check for filename duplicates
        '''
        local_files = set()
        for root, dirs, files in os.walk(path):
            for file in files:
                local_files.add(extract_filename(file))
        if extract_filename(url) in local_files:
            return True
        else:
            return False

    def loot(self, url, save_loc=None, filename=None, clean=False, wait=10):
        '''
        front-end for retrieve
        '''
        if clean:
            url = sanitize(url)
        if not filename:
            filename = extract_filename(url)
        if not save_loc:
            save_loc = self.path_main
        filepath = os.path.join(save_loc, f'{filename}.{filetype(url)}')
        if os.path.exists(filepath):
            if self.verbose:
                print(f'[{self.__str__()}] <file exists> {filename}')
            return False
        attempt = self.retrieve(add_scheme(url), filepath, wait)
        if attempt:
            print(f'[{self.__str__()}] <looted> {filename}')
            return True
        return False
