import os
from time import sleep
from gzip import decompress
from socket import timeout
from io import DEFAULT_BUFFER_SIZE
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from parsing import *
from meta_sources import *


class MetaGoblin:

    def __init__(self,url, mode, timeout, format, increment, nodl, verbose, tickrate):
        self.url = url
        self.tickrate = tickrate
        self.verbose = verbose
        self.nodl = nodl
        self.path_main = os.path.join(os.getcwd(), 'goblin_loot', self.__str__().replace(' ', '_'))
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
                os.makedirs(path)

    def cleanup(self, path):
        '''
        cleanup small unwanted files (icons, thumbnails, etc...)
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

    def retrieve(self, url, path, n=0):
        '''
        retrieve web content
        '''
        request = Request(url, None, self.headers)
        try:
            with urlopen(request, timeout=10) as response:
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
        except timeout:
            return self.retry(url, wait, n+1, path)
        return True

    def retry(self, url, n, path=None):
        '''
        retry connection after a socket timeout
        '''
        print(f'[{self.__str__()}] <timed out> retry attempt {n}')
        if n > 5:
            print(f'[{self.__str__()}] <timed out> aborting after {n} retries')
        else:
            if path:
                return self.retrieve(url, path, n)
            else:
                return self.get_html(url, n)

    def get_html(self, url, n=0):
        '''
        retrieve web page html
        '''
        request = Request(url, None, self.headers)
        try:
            with urlopen(request, timeout=10) as response:
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
        except timeout:
            return self.retry(url, n+1)
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

    def loot(self, url, save_loc=None, filename=None, clean=False):
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
        if self.nodl:
            print(url)
        else:
            attempt = self.retrieve(unescape(add_scheme(url)), filepath)
            if attempt:
                print(f'[{self.__str__()}] <looted> {filename}')
                return True
        return False
