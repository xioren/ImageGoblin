import os
import re

from sys import exit
from time import sleep
from random import randint
from socket import timeout
from shutil import copyfileobj
from contextlib import closing
from urllib.parse import urlencode
from http.cookiejar import CookieJar
from gzip import decompress, GzipFile
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from io import DEFAULT_BUFFER_SIZE, BufferedReader

from parsing import Parser
from logging import Logger
from version import __version__


class MetaGoblin:
    '''generic utility goblin inherited by all other goblins'''

    def __init__(self, args):
        self.args = args
        self.collection = set()
        self.looted = []
        if self.args['nosort']:
            self.path_main = os.getcwd()
        else:
            self.path_main = os.path.join(os.getcwd(), 'goblin_loot', self.NAME.replace(' ', '_'))
        if self.args['mask']:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0'
        else:
            user_agent = f'ImageGoblin/{__version__}'
        self.headers = {'User-Agent': user_agent,
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip'}

        self.make_dirs(self.path_main)

        self.cookie_jar = CookieJar()
        self.logger = Logger(self.args['verbose'], self.args['silent'], self.args['nodl'])
        self.parser = Parser(self.args['targets'][self.ID][0], self.args['format'])

        self.logger.log(1, self.NAME, 'deployed')

    ####################################################################
    # properties
    ####################################################################

    @property
    def delay(self):
        if self.args['delay'] == 'rand':
            return randint(0, 10)
        return int(self.args['delay'])

    ####################################################################
    # sub classes
    ####################################################################

    class ParsedResponse:
        '''wrapper for http.client.HTTPResponse'''

        def __init__(self, response, *args, **kwargs):
            if object:
                self.code = response.code
                self.info = response.info()
                if response.info().get('Content-Encoding') == 'gzip':
                    self.content = MetaGoblin.unzip(response.read()).decode('utf-8', 'ignore')
                else:
                    self.content = response.read().decode('utf-8', 'ignore')
            else:
                self.code = ''
                self.info = ''
                self.content = '{}'

    ####################################################################
    # methods
    ####################################################################

    def make_dirs(self, *paths):
        '''creates directories'''
        if not self.args['nodl']:
            for path in paths:
                if not os.path.exists(path):
                    try:
                        os.makedirs(path)
                    except OSError as e:
                        # NOTE: no sense in continuing if the download dirs fail to make
                        # may change approach in future, exit for now
                        self.logger.log(1, self.NAME, e, 'exiting')
                        exit(5) # input/output error

    def cleanup(self, path, threshold=50000):
        '''cleanup small unwanted files (icons, thumbnails, etc...)
        # default 50kb threshold
        '''
        if not self.args['nodl'] and not self.args['noclean']:
            for path in self.looted:
                if os.path.exists(path):
                    if os.path.getsize(path) < threshold:
                        try:
                            os.remove(path)
                        except OSError as e:
                            self.logger.log(2, self.NAME, e, path)

    def toggle_collecton_type(self):
        '''toggle collection type between list and set'''
        if isinstance(self.collection, list):
            self.collection = set()
        else:
            self.collection = []

    def new_collection(self):
        '''initialize a new collection'''
        self.collection.clear()
        self.looted.clear()

    def unzip(data):
        '''gzip decompression'''
        try:
            return decompress(data)
        except EOFError:
            return b''

    def cookie_value(self, name):
        '''return the value of a cookie from the cookie jar'''
        for cookie in self.cookie_jar:
            if cookie.name == name:
                return cookie.value

    def set_cookies(self):
        '''parse reponse headers and set cookies'''
        for cookie in self.cookie_jar:
            self.extend_cookie('Cookie', f'{cookie.name}={cookie.value}')

    def extend_cookie(self, cookie, value):
        '''add or extend a cookie'''
        if cookie not in self.headers:
            self.headers[cookie] = value
        else:
            current_values = {}
            new_key, new_val = value.split('=')

            for item in self.headers[cookie].split('; '):
                key, val = item.split('=')
                current_values[key] = val

            current_values[new_key] = new_val
            cookie_string = '; '.join(f'{key}={value}' for key, value in current_values.items())
            self.headers[cookie] = cookie_string

    def request_handler(self, method, *args, **kwargs):
        '''make an http request'''
        try:
            request = Request(self.parser.add_scheme(args[0]), kwargs['data'], self.headers)
        except ValueError as e:
            self.logger.log(2, self.NAME, e, args[0])
            return None

        try:
            with closing(urlopen(request, timeout=20)) as response:
                if kwargs['store_cookies']:
                    self.cookie_jar.extract_cookies(response, request)
                return method(response, *args, **kwargs)
        except HTTPError as e:
            self.logger.log(2, self.NAME, e, args[0])
            # servers sometimes return 502 when requesting large files, retrying usually works.
            if e.code == 502:
                return self.retry(self.request_handler, *args, **kwargs)
        except (timeout, URLError):
            return self.retry(self.request_handler, *args, **kwargs)
        except Exception as e:
            # NOTE: too many possible exceptions to catch individually -> use catchall
            self.logger.log(2, self.NAME, e, args[0])

    def get(self, url, store_cookies=False, attempt=0):
        '''make a get request'''
        return self.request_handler(self.ParsedResponse, url, data=None, store_cookies=store_cookies)

    def post(self, url, data, store_cookies=False, attempt=0):
        '''make a post request'''
        if isinstance(data, dict):
            data = urlencode(data)
        return self.request_handler(self.ParsedResponse, url, data=data.encode(), store_cookies=store_cookies)

    def download(self, url, filepath, attempt=0):
        '''downloader front end'''
        return self.request_handler(self.downloader, url, filepath, data=None, attempt=attempt, store_cookies=False)

    def downloader(self, response, *args, **kwargs):
        '''download web content'''
        if response.info().get('Content-Length') == '0':
            pass
        else:
            filepath = self.check_ext(args[1], response.info().get('Content-Type'))
            if os.path.exists(filepath):
                self.logger.log(2, self.NAME, 'file exists', self.parser.extract_filename(filepath))
                return None

            if response.info().get('Content-Encoding') == 'gzip':
                response = GzipFile(fileobj=BufferedReader(response))
            with open(filepath, 'wb') as file:
                copyfileobj(response, file, DEFAULT_BUFFER_SIZE)

            self.looted.append(filepath)
            return True

    def retry(self, method, *args, **kwargs):
        '''retry http operation after a socket timeout or server error'''
        if kwargs['attempt'] > 5:
            self.logger.log(2, self.NAME, 'server error', f'aborting after {kwargs["attempt"]} retries: {args[1]}')
            return None

        self.logger.log(2, self.NAME, 'server error', f'retry attempt {kwargs["attempt"]}: {args[1]}')
        sleep(kwargs['attempt'])

        return method(*args, **kwargs)

    def write_file(self, data, path, iter=False):
        '''write to a text file'''
        # QUESTION: is this used? keep?
        try:
            with open(path, 'w') as file:
                if iter:
                    file.write('\n'.join(data))
                else:
                    file.write(data)
        except OSError as e:
            self.logger.log(2, self.NAME, e, path)

    def read_file(self, path, iter=False):
        '''read from a text file'''
        try:
            with open(path, 'r') as file:
                if iter:
                    return file.read().splitlines()
                else:
                    return file.read()
        except OSError as e:
            self.logger.log(2, self.NAME, e, path)

    def check_ext(self, filepath, mimetype):
        '''compare guessed extension to header content type and change if necessary'''
        if mimetype and '/' in mimetype and mimetype not in ('binary/octet-stream'):
            ext = f'.{mimetype.split(";")[0].split("/")[1]}'
            guessed_ext = self.parser.extension(filepath)

            if guessed_ext and guessed_ext != ext:
                filepath = filepath.replace(guessed_ext, ext)
            elif not guessed_ext:
                filepath = f'{filepath}{ext}'

        return filepath

    def collect(self, url, filename='', clean=False):
        '''finalize and add urls to the collection'''
        if self.parser.filter(url):
            return None

        if clean:
            url = self.parser.sanitize(url)
        if not filename:
            filename = self.parser.extract_filename(url)
        ext = self.parser.extension(url)

        # add to collection as hashable string
        if isinstance(self.collection, list):
            self.collection.append(f'{self.parser.finalize(url)}-break-{filename}{ext}')
        else:
            self.collection.add(f'{self.parser.finalize(url)}-break-{filename}{ext}')

    def loot(self, save_loc=None, timeout=0):
        '''retrieve resources from collected urls'''
        failed = 0
        file = 1 # tracking for progress bar
        timed_out = False

        for item in self.collection:
            self.logger.progress(self.NAME, 'looting', file, len(self.collection))

            if timeout and failed >= timeout:
                timed_out = True
                break

            url, filename = item.split('-break-')

            if self.args['nodl']:
                print(url, end='\n\n')
                continue

            if not save_loc:
                save_loc = self.path_main
            filepath = os.path.join(save_loc, filename)

            if os.path.exists(filepath):
                if self.args['noskip'] or self.args['filename']:
                    filepath = self.parser.make_unique(filepath)
                else:
                    self.logger.log(2, self.NAME, 'file exists', self.parser.extract_filename(filepath))
                    continue

            attempt = self.download(url, filepath)
            if attempt:
                self.logger.log(2, self.NAME, 'looted', filename)
                failed = 0
            else:
                failed += 1

            file += 1
            sleep(self.delay)

        if self.args['nodl']:
            self.logger.log(1, self.NAME, 'info', f'{len(self.collection)} urls(s) collected', clear=True)
        else:
            self.logger.log(1, self.NAME, 'complete', f'{len(self.looted)} file(s) looted', clear=True)

        return timed_out
