import os
import re

from sys import exit
from time import sleep
from socket import timeout
from gzip import decompress
from shutil import copyfileobj
from ssl import CertificateError
from io import DEFAULT_BUFFER_SIZE
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from version import __version__
from parsing import Parser


class MetaGoblin(Parser):
    '''common methods inherited by all other goblins'''

    def __init__(self, args):
        super().__init__()
        self.args = args
        if self.args['nosort']:
            self.path_main = os.getcwd()
        else:
            self.path_main = os.path.join(os.getcwd(), 'goblin_loot', self.__str__().replace(' ', '_'))
        self.headers = {'User-Agent': f'ImageGoblin/{__version__}',
                        'Accept-Encoding': 'gzip'}
        self.collection = set()
        self.looted = set()
        if not self.args['nodl']:
            self.make_dirs(self.path_main)
        print(f'[{self.__str__()}] <deployed>')

    def make_dirs(self, *paths):
        '''creates directories'''
        # BUG: sometimes dirs do not make correctly leaving empty binary file
        for path in paths:
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except OSError as e:
                    # NOTE: no sense in continuing if the download dirs fail to make
                    # may change approach in future, exit for now
                    exit(f'[{self.__str__()}] <{e}> {path}')

    def cleanup(self, path):
        '''cleanup small unwanted files (icons, thumbnails, etc...)
        default 50kb threshold
        '''
        for path in self.looted:
            if os.path.getsize(path) < 50000:
                try:
                    os.remove(path)
                except OSError as e:
                    if self.args['verbose'] and not self.args['silent']:
                        print(f'[{self.__str__()}] <{e}> {path}')

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
            # OPTIMIZE: return something other than empty bytes?
            return b''

    def get(self, url, path='', n=0, save=True):
        '''get web content'''
        request = Request(url, None, self.headers)
        try:
            with urlopen(request, timeout=20) as response:
                    if save:
                        with open(path, 'wb') as file:
                            copyfileobj(response, file, DEFAULT_BUFFER_SIZE)
                    else:
                        return self.unzip(response.read()).decode('utf-8', 'ignore')
        except (HTTPError, URLError, CertificateError) as e:
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {url}')
            return None
        except timeout:
            return self.retry(url, n+1, path, save)
        return True

    def retry(self, url, n, path, save):
        '''retry connection after a socket timeout'''
        # TODO: add verbose outputs
        if n > 5:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <timeout> aborting after {n} retries')
            return None
        if not self.args['silent']:
                print(f'[{self.__str__()}] <timeout> retry attempt {n}')
        sleep(self.args['dealay'])
        return self.get(url, path, n, save)

    def get_html(self, url):
        '''return html'''
        return self.get(url, save=False)

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
            return {url.group().replace('\\', '') for url in re.finditer(pattern, self.get_html(url))}
        except TypeError as e:
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}>')
            return ''

    def collect(self, url, filename='', clean=False):
        '''finalize and add urls to collection'''
        if clean:
            url = self.sanitize(url)
        if not filename:
            filename = self.extract_filename(url)
        if type(self.collection) == set:
            self.collection.add(f'{self.finalize(url)}-break-{filename}')
        else:
            self.collection.append(f'{self.finalize(url)}-break-{filename}')

    def loot(self, save_loc=None, timeout=0):
        '''get collected urls'''
        failed = loot_tally = 0
        timed_out = False
        for url in self.collection:
            if timeout and failed >= timeout:
                timed_out = True
                break
            url, filename = url.split('-break-')
            ftype = self.filetype(url)
            if self.args['nodl']:
                print(url, end='\n\n')
                continue
            if not save_loc:
                save_loc = self.path_main
            filepath = os.path.join(save_loc, f'{filename}.{ftype}')
            if os.path.exists(filepath):
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <file exists> {filename}')
                continue
            attempt = self.get(url, filepath)
            if attempt:
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <looted> {filename}')
                loot_tally += 1
                failed = 0
                self.looted.add(filepath)
            else:
                failed += 1
            sleep(self.args['delay'])
        print(f'[{self.__str__()}] <complete> {loot_tally} file(s) looted')
        return timed_out
