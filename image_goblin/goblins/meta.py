import os
import re

from sys import exit
from time import sleep
from socket import timeout
from shutil import copyfileobj
from ssl import CertificateError
from http.client import InvalidURL
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
                        'Accept': '*/*',
                        'Accept-Encoding': 'gzip'}

        self.make_dirs(self.path_main)

        self.cookie_jar = CookieJar()
        self.logger = Logger(self.args['verbose'], self.args['silent'], self.args['nodl'])
        self.parser = Parser(self.args['targets'][self.ID][0], self.args['format'])

        self.logger.log(0, self.NAME, 'deployed')

####################################################################
# sub classes
####################################################################

    class ParsedRequest:
        '''wrapper for http.client.HTTPResponse'''

        def __init__(self, object):
            if object:
                self.code = object.code
                self.info = object.info()
                try:
                    if object.info().get('content-encoding') == 'gzip':
                        self.content = MetaGoblin.unzip(object.read()).decode('utf-8', 'ignore')
                    else:
                        self.content = object.read().decode('utf-8', 'ignore')
                except timeout:
                    return None
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

    def make_request(self, url, data=None, store_cookies=False, attempt=0):
        '''make an http request'''
        try:
            request = Request(self.parser.add_scheme(url), data, self.headers)
        except ValueError as e:
            self.logger.log(2, self.NAME, e, url)
            return None

        try:
            response = urlopen(request, timeout=20)
            if store_cookies:
                self.cookie_jar.extract_cookies(response, request)
            return response
        except HTTPError as e:
            self.logger.log(2, self.NAME, e, url)
            # servers sometimes return 502 when requesting large files, retrying usually works.
            if e.code == 502:
                return self.retry(self.make_request, url, data=data, store_cookies=store_cookies, attempt=attempt+1)
        except (UnicodeEncodeError, InvalidURL, CertificateError) as e:
            self.logger.log(2, self.NAME, e, url)
        except (timeout, URLError):
            return self.retry(self.make_request, url, data=data, attempt=attempt+1)

    def get(self, url, store_cookies=False, attempt=0):
        '''make a get request'''
        response = self.ParsedRequest(self.make_request(url, store_cookies=store_cookies))
        if not response:
            return retry(self.get, url, store_cookies=False, attempt=attempt+1)
        return response

    def post(self, url, data, store_cookies=False, attempt=0):
        '''make a post request'''
        if isinstance(data, dict):
            data = urlencode(data)
        response = self.ParsedRequest(self.make_request(url, data=data.encode(), store_cookies=store_cookies))
        if not response:
            return retry(self.post, url, data, store_cookies=False, attempt=attempt+1)
        return response

    def download(self, url, filepath, attempt=0):
        '''download web content'''
        response = self.make_request(url)

        if response:
            filepath = self.check_ext(filepath, response.info().get('content-type'))
            if os.path.exists(filepath):
                return None

            if response.info().get('content-encoding') == 'gzip':
                response = GzipFile(fileobj=BufferedReader(response))

            try:
                with open(filepath, 'wb') as file:
                    copyfileobj(response, file, DEFAULT_BUFFER_SIZE)
            except timeout:
                return self.retry(self.download, url, filepath, attempt=attempt+1)

            self.looted.append(filepath)
            return True

    def retry(self, method, *args, **kwargs):
        '''retry http operation after a socket timeout or server error'''
        if kwargs['attempt'] > 5:
            self.logger.log(2, self.NAME, 'server error', f'aborting after {kwargs["attempt"]} retries: {args[0]}')
            return None

        self.logger.log(2, self.NAME, 'server error', f'retry attempt {kwargs["attempt"]}: {args[0]}')
        sleep(kwargs['attempt'])

        return method(*args, **kwargs)

    def write_file(self, data, path, iter=False):
        '''write to text file'''
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
        '''read from text file'''
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
        if '/' in mimetype and mimetype not in ('binary/octet-stream'):
            ext = f'.{mimetype.split("/")[1]}'
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
                    path = self.parser.make_unique(filepath)
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
            sleep(self.args['delay'])

        if self.args['nodl']:
            self.logger.log(0, self.NAME, 'info', f'{len(self.collection)} urls(s) collected', clear=True)
        else:
            self.logger.log(0, self.NAME, 'complete', f'{len(self.looted)} file(s) looted', clear=True)

        return timed_out
