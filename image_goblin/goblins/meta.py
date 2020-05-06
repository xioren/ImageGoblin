import os
import re

from sys import exit
from time import sleep
from socket import timeout
from gzip import decompress
from shutil import copyfileobj
from ssl import CertificateError
from io import DEFAULT_BUFFER_SIZE
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

from parsing import Parser
from logging import Logger
from version import __version__


class MetaGoblin:
    '''base goblin inherited by all other goblins'''

    def __init__(self, args):
        super().__init__()
        self.args = args
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
        self.collection = set()
        self.looted = []
        self.make_dirs(self.path_main)
        self.logger = Logger(self.args['verbose'], self.args['silent'])
        self.parser = Parser(self.args['targets'][self.ID][0], self.args['format'])
        self.logger.log(0, self.NAME, 'deployed')

####################################################################
# sub classes
####################################################################

    class Get:
        '''wrapper for http.client.HTTPResponse'''

        def __init__(self, object):
            self.code = object.code if object else ''
            self.info = object.info().as_string() if object else ''
            self.content = MetaGoblin.unzip(object.read()).decode('utf-8', 'ignore') if object else '{}'

    class Post:
        '''wrapper for http.client.HTTPResponse'''

        def __init__(self, object):
            self.code = object.code if object else ''
            self.info = object.info().as_string() if object else ''
            self.content = MetaGoblin.unzip(object.read()).decode('utf-8', 'ignore') if object else '{}'

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
                        exit(1)

    def cleanup(self, path):
        '''cleanup small unwanted files (icons, thumbnails, etc...)
        default 50kb threshold
        '''
        if not self.args['nodl'] and not self.args['noclean']:
            for path in self.looted:
                if os.path.getsize(path) < 50000:
                    try:
                        os.remove(path)
                    except OSError as e:
                        self.logger.log(2, self.NAME, e, path)

    def toggle_collecton_type(self):
        '''toggle collection type between list and set'''
        if type(self.collection) == list:
            self.collection = set()
        else:
            self.collection = []

    def new_collection(self):
        '''initialize a new collection'''
        self.collection.clear()

    def size_of(self, iterable):
        '''get size of a set'''
        return sum(1 for _ in iterable)

    def unzip(data):
        '''gzip decompression'''
        try:
            return decompress(data)
        except OSError:
            return data
        except EOFError:
            # OPTIMIZE: return something other than empty bytes?
            return b''

    def make_request(self, url, n=0, data=None):
        '''make a web request'''
        try:
            request = Request(self.parser.add_scheme(url), data, self.headers)
        except ValueError as e:
            self.logger.log(2, self.NAME, e, url)
            return None
        try:
            return urlopen(request, timeout=20)
        except HTTPError as e:
            self.logger.log(2, self.NAME, e, url)
            # servers sometimes return 502 when requesting large files, retrying usually works.
            if e.code == 502:
                return self.retry(url, n+1, data)
        except (URLError, CertificateError) as e:
            self.logger.log(2, self.NAME, e, url)
        except timeout:
            return self.retry(url, n+1, data)

    def extend_cookie(self, cookie, value):
        '''add to or update a cookie'''
        if not self.headers.get(cookie):
            self.headers.update({cookie: value})
        else:
            values = set(self.headers[cookie].split('; '))
            values.add(value)
            self.headers[cookie] = '; '.join(values)

    def get(self, url):
        '''make a get request'''
        return self.Get(self.make_request(url))

    def post(self, url, data):
        '''make a post request'''
        return self.Post(self.make_request(url, data=urlencode(data).encode()))

    def download(self, url, path, n=0):
        '''download web content'''
        response = self.make_request(url)
        if response:
            try:
                with open(path, 'wb') as file:
                    copyfileobj(response, file, DEFAULT_BUFFER_SIZE)
            except timeout:
                return self.retry(url, n, path=path)
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
        '''write to disk'''
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
        '''read from disk'''
        try:
            with open(path, 'r') as file:
                if iter:
                    return file.read().splitlines()
                else:
                    return file.read()
        except OSError as e:
            self.logger.log(2, self.NAME, e, path)

    def extract_by_tag(self, url, tag=None, attr=None):
        '''extract from html by tag'''
        response = self.get(url)
        if response:
            html_parser = self.parser.GoblinHTMLParser(response.content)
            html_parser.parse_elements()
            if tag and attr:
                return html_parser.elements[tag][attr]
            else:
                return html_parser.elements
        else:
            return ''

    def extract_by_regex(self, pattern, url):
        '''extract from html by regex'''
        try:
            return {match.group().replace('\\', '') for match in re.finditer(pattern, self.get(url).content)}
        except TypeError:
            return ''

    def collect(self, url, filename='', clean=False):
        '''finalize and add urls to the collection'''
        if clean:
            url = self.parser.sanitize(url)
        if not filename:
            filename = self.parser.extract_filename(url)
        if type(self.collection) == list:
            self.collection.append(f'{self.parser.finalize(url)}-break-{filename}')
        else:
            self.collection.add(f'{self.parser.finalize(url)}-break-{filename}')

    def loot(self, save_loc=None, timeout=0):
        '''retrieve resources from collected urls'''
        failed = 0
        file = 1
        timed_out = False
        for item in self.collection:
            if timeout and failed >= timeout:
                timed_out = True
                break
            url, filename = item.split('-break-')
            if self.args['nodl']:
                print(url, end='\n\n')
                continue
            self.logger.progress(self.NAME, 'looting files', file, self.size_of(self.collection))
            file += 1
            if not save_loc:
                save_loc = self.path_main
            ftype = self.parser.filetype(url)
            filepath = os.path.join(save_loc, f'{filename}.{ftype}')
            if os.path.exists(filepath):
                if self.args['noskip']:
                    filepath = self.parser.make_unique(save_loc, f'{filename}.{ftype}')
                else:
                    self.logger.log(2, self.NAME, 'file exists', filename)
                    continue
            attempt = self.download(url, filepath)
            if attempt:
                self.logger.log(2, self.NAME, 'looted', filename)
                self.looted.append(filepath)
                failed = 0
            else:
                failed += 1
            sleep(self.args['delay'])
        self.logger.log(0, self.NAME, 'complete', f'{len(self.looted)} file(s) looted', clear=True)
        return timed_out
