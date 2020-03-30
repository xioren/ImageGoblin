import os
import re
from time import sleep
from gzip import decompress
from socket import timeout
from io import DEFAULT_BUFFER_SIZE
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from parsing import Parser


class MetaGoblin(Parser):

    def __init__(self, args):
        self.args = args
        if self.args['nosort']:
            self.path_main = os.getcwd()
        else:
            self.path_main = os.path.join(os.getcwd(), 'goblin_loot', self.__str__().replace(' ', '_'))
        self.headers = {True: {'User-Agent': 'GoblinTeam/1.3',
                               'Accept-Encoding': 'gzip'},
                        False: {'User-Agent': 'GoblinTeam/1.3'}}
        self.loot_tally = 0
        self.collection = set()
        if not self.args['nodl']:
            self.make_dirs(self.path_main)
        if self.args['url'] and self.args['verbose']:
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
        # NOTE:  dangerous, consider recieving file manifest instead?
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
        '''
        toggle collection type between sorted list and set
        '''
        if type(self.collection) == set:
            self.collection = []
        else:
            self.collection = {}

    def grab_vid(self, url):
        '''
        download a video in best quality, primarily for vimeo
        '''
        filename = self.extract_filename(url)
        os.system(f'youtube-dl --output {self.path_main}/{filename} {url}')

    def unzip(self, data):
        try:
            return decompress(data)
        except OSError:
            return data
        except EOFError:
            return None

    def retrieve(self, url, path='', n=0, gzip=True, save=True):
        '''
        retrieve web content
        '''
        request = Request(url, None, self.headers[gzip])
        try:
            with urlopen(request, timeout=10) as response:
                encoding = response.info().get('Content-Encoding')
                if not save:
                    data = response.read()
                    if encoding == 'gzip':
                        data = self.unzip(data)
                        if not data:
                            return self.retrieve(url, gzip=False, save=False)
                    return data.decode('utf-8', 'ignore')
                else:
                    with open(path, 'wb') as file:
                        while True:
                            data = response.read(DEFAULT_BUFFER_SIZE)
                            if not data:
                                break
                            if encoding == 'gzip':
                                data = self.unzip(data)
                                if not data:
                                    return self.retrieve(url, path, gzip=False)
                            file.write(data)
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
        '''
        retry connection after a socket timeout
        '''
        if not self.args['silent']:
            print(f'[{self.__str__()}] <timed out> retry attempt {n}')
        if n > 5:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <timed out> aborting after {n} retries')
        else:
            sleep(self.args['tickrate'])
        return self.retrieve(url, path, n, save)

    def get_html(self, url, n=0, gzip=True):
        '''
        retrieve web page html
        '''
        return self.retrieve(url, save=False)

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
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {path}')

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
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}> {path}')

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
        except TypeError as e:
            if self.args['verbose'] and not self.args['silent']:
                print(f'[{self.__str__()}] <{e}>')
            return ''

    def filter(self, iterable):
        '''
        remove duplicates from a list
        '''
        return set(iterable)

    def new_collection(self):
        '''
        initialize a new collection
        '''
        if type(self.collection) == set:
            self.collection = {}
        else:
            self.collection = []

    def collect(self, url, filename='', clean=False):
        '''
        finalize and add links to collection
        '''
        if clean:
            url = self.sanitize(url)
        if not filename:
            filename = self.extract_filename(url)
        if type(self.collection) == set:
            self.collection.add(f'{self.finalize(url)}-break-{filename}')
        else:
            self.collection.append(f'{self.finalize(url)}-break-{filename}')

    def loot(self, save_loc=None, timeout=False):
        '''
        front end for retrieve
        '''
        track = 0
        for link in self.collection:
            if timeout and track >= timeout:
                return None
            link, filename = link.split('-break-')
            if self.args['nodl']:
                print(link, end='\n\n')
                continue
            if not save_loc:
                save_loc = self.path_main
            filepath = os.path.join(save_loc, f'{filename}.{self.filetype(link)}')
            if os.path.exists(filepath):
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <file exists> {filename}')
                track += 1
                continue
            attempt = self.retrieve(link, filepath)
            if attempt:
                if not self.args['silent']:
                    print(f'[{self.__str__()}] <looted> {filename}')
                self.loot_tally += 1
                track = 0
            else:
                track += 1
            sleep(self.args['tickrate'])
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
        return True
