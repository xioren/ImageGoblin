import os
import re
import http.cookiejar

from sys import exit
from time import sleep
from socket import timeout
from shutil import copyfileobj
from ssl import CertificateError
from http.client import InvalidURL
from urllib.parse import urlencode
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
        super().__init__()
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
                        'Accept-Encoding': 'gzip'}

        self.make_dirs(self.path_main)

        self.logger = Logger(self.args['verbose'], self.args['silent'])
        self.parser = Parser(self.args['targets'][self.ID][0], self.args['format'])
        self.cj = http.cookiejar.CookieJar()

        self.logger.log(0, self.NAME, 'deployed')

####################################################################
# sub classes
####################################################################

    class ParsedRequest:
        '''wrapper for http.client.HTTPResponse'''

        def __init__(self, object):
            if object:
                self.code = object.code
                # QUESTION: keep as string?
                self.info = object.info()
                # TEMP: implement real retry handling
                for _ in range(5):
                    try:
                        if object.info().get('content-encoding') == 'gzip':
                            self.content = MetaGoblin.unzip(object.read()).decode('utf-8', 'ignore')
                        else:
                            self.content = object.read().decode('utf-8', 'ignore')
                        break
                    except timeout:
                        sleep(2)
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
                        self.logger.log(0, self.NAME, e, 'exiting')
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

    def unzip(data):
        '''gzip decompression'''
        try:
            return decompress(data)
        except EOFError:
            return b''

    def make_request(self, url, n=0, data=None, set_cookies=False):
        '''make an http request'''
        try:
            request = Request(self.parser.add_scheme(url), data, self.headers)
        except ValueError as e:
            self.logger.log(2, self.NAME, e, url)
            return None

        try:
            response = urlopen(request, timeout=20)
            if set_cookies:
                self.cj.extract_cookies(response, request)
            return response
        except HTTPError as e:
            self.logger.log(2, self.NAME, e, url)
            # servers sometimes return 502 when requesting large files, retrying usually works.
            if e.code == 502:
                return self.retry(url, n+1, data)
        except (URLError, CertificateError, UnicodeEncodeError, InvalidURL) as e:
            self.logger.log(2, self.NAME, e, url)
        except timeout:
            return self.retry(url, n+1, data)

    def extract_cookie(self, name):
        '''return a cookie from the cookie jar'''
        for cookie in self.cj:
            if cookie.name == name:
                return cookie.value

    def set_cookies(self):
        '''parse reponse headers and set cookies'''
        for cookie in self.cj:
            self.extend_cookie('Cookie', f'{cookie.name}={cookie.value}')

    def extend_cookie(self, cookie, value):
        '''add or extend a cookie'''
        if cookie not in self.headers:
            self.headers[cookie] = value
        else:
            values = set(self.headers[cookie].split('; '))
            values.add(value)
            self.headers[cookie] = '; '.join(values)

    def get(self, url, set_cookies=False):
        '''make a get request'''
        return self.ParsedRequest(self.make_request(url, set_cookies=set_cookies))

    def post(self, url, data, set_cookies=False):
        '''make a post request'''
        if isinstance(data, dict):
            data = urlencode(data)
        return self.ParsedRequest(self.make_request(url, data=data.encode(), set_cookies=set_cookies))

    def download(self, url, path, n=0):
        '''download web content'''
        response = self.make_request(url)
        if response:
            ext = response.info().get('content-type') or 'image/jpeg'
            path = self.check_filepath(f'{path}.{ext.split("/")[1]}')
            if path:
                if response.info().get('content-encoding') == 'gzip':
                    response = GzipFile(fileobj=BufferedReader(response))
                try:
                    with open(path, 'wb') as file:
                        copyfileobj(response, file, DEFAULT_BUFFER_SIZE)
                except timeout:
                    return self.retry(url, n, path=path)
                self.looted.append(path)
                return True

    def retry(self, url, n, data=None, path=None):
        '''retry connection after a socket timeout'''
        if n > 5:
            self.logger.log(2, self.NAME, 'timed out', f'aborting after {n} retries')
            return None
        self.logger.log(2, self.NAME, 'timed out', f'retry attempt {n}')

        sleep(3)

        if path:
            return self.download(url, path, n)
        else:
            return self.make_request(url, n, data)

    def write_file(self, data, path, iter=False):
        '''write to text file'''
        # QUESTION: is this used? keep if so?
        try:
            with open(path, 'w') as file:
                if iter:
                    file.write('\n'.join(data))
                else:
                    file.write(data)
        except OSError as e:
            self.logger.log(2, self.NAME, e, path)

    def read_file(self, path, iter=False):
        '''read from text file'''
        try:
            with open(path, 'r') as file:
                if iter:
                    return file.read().splitlines()
                else:
                    return file.read()
        except OSError as e:
            self.logger.log(2, self.NAME, e, path)

    def check_filepath(self, path):
        '''check if filepath exists and either skip or make unique if necessary'''
        if os.path.exists(path):
            if self.args['noskip'] or self.args['filename']:
                path = self.parser.make_unique(path)
            else:
                self.logger.log(2, self.NAME, 'file exists', self.parser.extract_filename(path))
                return None

        return path

    def collect(self, url, filename='', clean=False):
        '''finalize and add urls to the collection'''
        if self.parser.filter(url):
            return None

        if clean:
            url = self.parser.sanitize(url)
        if not filename:
            filename = self.parser.extract_filename(url)
        elif self.parser.extension(filename): # remove extension
            filename = '.'.join(filename.split('.')[:-1])

        # add to collection as hashable string
        if isinstance(self.collection, list):
            self.collection.append(f'{self.parser.finalize(url)}-break-{filename}')
        else:
            self.collection.add(f'{self.parser.finalize(url)}-break-{filename}')

    def loot(self, save_loc=None, timeout=0):
        '''retrieve resources from collected urls'''
        failed = 0
        file = 1 # tracking for progress bar
        timed_out = False

        for item in self.collection:
            if timeout and failed >= timeout:
                timed_out = True
                break

            url, filename = item.split('-break-')

            if self.args['nodl']:
                print(url, end='\n\n')
                continue

            self.logger.progress(self.NAME, 'looting', file, len(self.collection))

            if not save_loc:
                save_loc = self.path_main
            filepath = os.path.join(save_loc, filename)

            attempt = self.download(url, filepath)
            if attempt:
                self.logger.log(2, self.NAME, 'looted', filename)
                failed = 0
            else:
                failed += 1
            file += 1
            sleep(self.args['delay'])

        self.logger.log(0, self.NAME, 'complete', f'{len(self.looted)} file(s) looted', clear=True)

        return timed_out
