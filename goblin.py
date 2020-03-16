import os
from sys import platform
from gzip import decompress
from getpass import getuser
from io import DEFAULT_BUFFER_SIZE
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from parsing import *


class MetaGoblin:

    def __init__(self, url, save_loc, overwrite):
        if save_loc:
            self.save_loc = Parser.add_slash(save_loc)
        else:
            if platform == 'win32':
                self.save_loc = f'C:/Users/{os.getlogin()}/Downloads/'
            else:
                self.save_loc = f'/home/{getuser()}/Downloads/'
        self.url = url
        self.overwrite = overwrite
        self.main_path = f'{self.save_loc}web_goblin/'
        self.dl_folder = f'{self.main_path}golbin_media/'
        self.txt_loc = f'{self.main_path}goblin_links.txt'
        self.headers = {'User-Agent': 'Firefox/72',
                        'Accept-Encoding': 'gzip'}
        self.create_folders(self.main_path)

    def create_folders(self, path):
        '''
        creates directories
        '''
        if self.exists(path) is False:
            os.makedirs(path)

    def cleanup(self, loc):
        '''
        cleanup unwanted files (icons, blank, etc...)
        '''
        for file in os.listdir(loc):
            if os.path.getsize(f'{loc}/{file}') < 50000:
                try:
                    os.remove(f'{loc}/{file}')
                except PermissionError as e:
                    print(f'[cleanup error] {e}')
                    continue

    def retrieve(self, url, path, silent=False):
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
                            file.write(self.unzip(data))
                        else:
                            file.write(data)
        except Exception as e:
            if not silent:
                print(f'[{e}] {url}')
            return None
        return True

    def get_html(self, url):
        '''
        retrieve html
        '''
        request = Request(url, None, self.headers)
        try:
            with urlopen(request, timeout=10) as response:
                html = response.read()
        except Exception as e:
            print(f'[{e}] {url}')
            return None
        if response.info().get('Content-Encoding') == 'gzip':
            return self.unzip(html).decode()
        else:
            return html.decode()

    def duplicate_file(self, filename):
        '''
        make filename unique
        '''
        n = 1
        while True:
            name_unique = Parser.make_unique(name=filename, n=n)
            if self.exists(name_unique):
                n += 1
            else:
                return name_unique

    def write_file(self, cont, path):
        '''
        write to file (binary)
        '''
        if self.exists(path):
            path = self.duplicate_file(path)
        try:
            with open(path, 'wb') as file:
                file.write(cont)
        except Exception as e:
            print(f'[write error] {e}')

    def write_iter(self, iter, path, mode='w'):
        '''
        write to file iteratively (text)
        '''
        with open(path, mode) as link_out:
            for item in iter:
                try:
                    link_out.write(f'{item}\n')
                except Exception as e:
                    print(f'[write error] {e}')
                    continue

    def read_file(self, path, mode=None):
        '''
        read txt file
        '''
        try:
            with open(path, 'r') as file_in:
                if mode == 'iter':
                    return file_in.readlines()
                else:
                    return file_in.read()
        except Exception as e:
            print(f'[read error] {e}')

    def exists(self, path):
        '''
        check if file exists
        '''
        if os.path.exists(path):
            return True
        else:
            return False

    def unzip(self, data):
        '''
        decompress gzip encoded data
        '''
        # TODO: recode such that try except is not necessary
        try:
            return decompress(data)
        except OSError:
            return data

    def move_vid(self, path):
        if not self.exists(f'{path}vid'):
            os.mkdir(f'{path}vid')
        for file in os.listdir(path):
            if '.mp4' in file:
                os.rename(f'{path}{file}', f'{path}vid/{file}')
