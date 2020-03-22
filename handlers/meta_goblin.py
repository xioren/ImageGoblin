import os
import re
from gzip import decompress
from socket import timeout
from io import DEFAULT_BUFFER_SIZE
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from parsing import Parser
from meta_sources import *


class MetaGoblin(Parser):

    def __init__(self, args):
        self.args = args
        self.path_main = os.path.join(os.getcwd(), 'goblin_loot', self.__str__().replace(' ', '_'))
        self.external_links = os.path.join(os.getcwd(), 'links.txt')
        self.headers = {'User-Agent': 'GoblinTeam/1.3',
                        'Accept-Encoding': 'gzip'}
        self.loot_tally = 0
        if not self.args['nodl']:
            self.make_dirs(self.path_main)
        if self.args['url']:
            print(f'[{self.__str__()}] <deployed> {self.args["url"]}')
        else:
            print(f'[{self.__str__()}] <deployed>')

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
                    if not self.args['silent']:
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
            if not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        except URLError as e:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        except timeout:
            return self.retry(url, n+1, path)
        return True

    def retry(self, url, n, path=None):
        '''
        retry connection after a socket timeout
        '''
        if not self.args['silent']:
            print(f'[{self.__str__()}] <timed out> retry attempt {n}')
        if n > 5:
            if not self.args['silent']:
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
            if not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        except URLError as e:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        except timeout:
            return self.retry(url, n+1)
        return html.decode('utf-8', 'ignore')

    def write_file(self, data, path, mode='w', iter=False):
        '''
        write to disk
        '''
        # QUESTION: is this used?
        try:
            with open(path, mode) as file:
                if iter:
                    for item in data:
                        file.write(f'{item}\n')
                else:
                    file.write(data)
        except OSError as e:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <write error> {e}')

    def read_file(self, path, iter=False):
        '''
        read txt file
        '''
        try:
            with open(path, 'r') as file:
                if iter:
                    return file.read().splitlines()
                else:
                    return file.read()
        except OSError as e:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <read error> {e}')

    def move_vid(self, path):
        '''
        move videos into seperate directory
        '''
        # QUESTION: move to instagram?
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
                local_files.add(self.extract_filename(file))
        if self.extract_filename(url) in local_files:
            return True
        else:
            return False

    def extract_links(self, pattern, url):
        '''
        extact links from html based on regex pattern
        '''
        try:
            return {link.group() for link in re.finditer(pattern, self.get_html(url))}
        except TypeError:
            return ''

    def filter(self, iterable):
        '''
        remove duplicates from a list
        '''
        return set(iterable)

    def loot(self, url, save_loc=None, filename=None, clean=False):
        '''
        front-end for retrieve
        '''
        if self.args['nodl']:
            print(url, end='\n\n')
            return
        if clean:
            url = self.sanitize(url)
        if not filename:
            filename = self.extract_filename(url)
        if not save_loc:
            save_loc = self.path_main
        filepath = os.path.join(save_loc, f'{filename}.{self.filetype(url)}')
        if os.path.exists(filepath):
            if not self.args['silent']:
                print(f'[{self.__str__()}] <file exists> {filename}')
            return False
        attempt = self.retrieve(self.finalize(url), filepath)
        if attempt:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <looted> {filename}')
            self.loot_tally += 1
            return True
        return False
