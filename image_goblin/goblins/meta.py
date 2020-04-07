import os
import re

from time import sleep
from socket import timeout
from gzip import decompress
from shutil import copyfileobj
from io import DEFAULT_BUFFER_SIZE
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from parsing import Parser


class MetaGoblin(Parser):
    '''common methods inherited by all other goblins
    '''

    def __init__(self, args):
        super().__init__()
        self.args = args
        if self.args['nosort']:
            self.path_main = os.getcwd()
        else:
            self.path_main = os.path.join(os.getcwd(), 'goblin_loot', self.__str__().replace(' ', '_'))
        self.headers = {True: {'User-Agent': 'ImageGoblin/1.0.7',
                               'Accept-Encoding': 'gzip'},
                        False: {'User-Agent': 'ImageGoblin/1.0.7'}}
        self.collection = set()
        if not self.args['nodl']:
            self.make_dirs(self.path_main)
        print(f'[{self.__str__()}] <deployed>')

    def make_dirs(self, *paths):
        '''creates directories'''
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

    def cleanup(self, path):
        '''cleanup small unwanted files (icons, thumbnails, etc...)
        default 50kb threshold
        '''
        # NOTE:  dangerous, consider recieving file manifest instead?
        # TEMP: restrict usage to only the directories created by this app
        if not self.args['nosort']:
            for file in os.listdir(path):
                filepath = os.path.join(path, file)
                if os.path.isdir(filepath):
                    continue
                if os.path.getsize(filepath) < 50000:
                    try:
                        os.remove(filepath)
                    except PermissionError as e:
                        if self.args['verbose'] and not self.args['silent']:
                            print(f'[{self.__str__()}] <{e}> {filepath}')
                        continue

    def toggle_collecton_type(self, reverse=False):
        '''toggle collection type between list and set'''
        if type(self.collection) == set:
            self.collection = []
        else:
            self.collection = set()

    def new_collection(self):
        '''initialize a new collection'''
        if type(self.collection) == set:
            self.collection = set()
        else:
            self.collection = []

    def unzip(self, data):
        '''gzip decompression'''
        try:
            return decompress(data)
        except OSError:
            return data
        except EOFError:
            # TODO: improve this
            return b''

    def retrieve(self, url, path='', n=0, gzip=True, save=True):
        '''retrieve web content'''
        request = Request(url, None, self.headers[gzip])
        try:
            with urlopen(request, timeout=20) as response:
                    if save:
                        with open(path, 'wb') as file:
                            copyfileobj(response, file, DEFAULT_BUFFER_SIZE)
                    else:
                        return self.unzip(response.read()).decode('utf-8', 'ignore')
        except HTTPError as e:
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        except URLError as e:
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        except timeout:
            return self.retry(url, n+1, path, save)
        return True

    def retry(self, url, n, path, save):
        '''retry connection after a socket timeout'''
        # TODO: add verbose outputs
        if not self.args['silent']:
                print(f'[{self.__str__()}] <timeout> retry attempt {n}')
        if n > 5:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <timeout> aborting after {n} retries')
            return None
        else:
            sleep(self.args['tickrate'])
        return self.retrieve(url, path, n, save)

    def get_html(self, url):
        '''retrieve web page html'''
        return self.retrieve(url, save=False)

    def write_file(self, data, path, mode='w', iter=False):
        '''write to disk'''
        # QUESTION: is this used?
        try:
            with open(path, mode) as file:
                if iter:
                    file.writelines(data)
                else:
                    file.write(data)
        except OSError as e:
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {path}')

    def read_file(self, path, iter=False):
        '''read txt file'''
        try:
            with open(path, 'r') as file:
                if iter:
                    return file.read().splitlines()
                else:
                    return file.read()
        except OSError as e:
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {path}')

    def extract_urls(self, pattern, url):
        '''extact urls from html based on regex pattern'''
        try:
            return {url.group() for url in re.finditer(pattern, self.get_html(url))}
        except TypeError as e:
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}>')
            return ''

    def collect(self, url, filename='', clean=False):
        '''finalize and add urls tof.path_main) collection'''
        if clean:
            url = self.sanitize(url)
        if not filename:
            filename = self.extract_filename(url)
        if type(self.collection) == set:
            self.collection.add(f'{self.finalize(url)}-break-{filename}')
        else:
            self.collection.append(f'{self.finalize(url)}-break-{filename}')

    def loot(self, save_loc=None, timeout=False):
        '''retrieve collected urls'''
        track = 0
        loot_tally = 0
        timed_out = False
        for url in self.collection:
            if timeout and track >= timeout:
                timed_out = True
                break
            url, filename = url.split('-break-')
            if self.args['nodl']:
                print(url, end='\n\n')
                continue
            if not save_loc:
                save_loc = self.path_main
            filepath = os.path.join(save_loc, f'{filename}.{self.filetype(url)}')
            if os.path.exists(filepath):
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <file exists> {filename}')
                track += 1
                continue
            attempt = self.retrieve(url, filepath)
            if attempt:
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <looted> {filename}')
                loot_tally += 1
                track = 0
            else:
                track += 1
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <complete> {loot_tally} file(s) looted')
        return True, timed_out
