import re
from urllib.parse import urlparse
from strings import *


class Parser:

    '''
    generic parsing methods
    '''

    def extract_filename(self, url):
        '''
        extracts filename from url
        '''
        try:
            return re.sub(regex_patterns['filetype'], '', re.search(regex_patterns['filename'], self.dequery(url)).group().strip('/'))
        except AttributeError:
            return 'image'

    def decrop(self, url):
        '''
        removes common cropping from url
        '''
        for pat in format_patterns:
            url = re.sub(pat, '', url)
        return url

    def dequery(self, url):
        '''
        remove query string from url
        '''
        return re.sub(regex_patterns['query'], '', url)

    def sanitize(self, url):
        '''
        combines dequery and decrop
        '''
        return self.decrop(self.dequery(url))

    def filetype(self, url):
        '''
        extract file type
        '''
        type = re.search(regex_patterns['filetypes'], url, re.IGNORECASE)
        if not type:
            return ''
        return type.group().lstrip('.')

    def add_scheme(self, url):
        '''
        checks for and adds scheme
        '''
        if not urlparse(url)[0]:
            url = 'https://' + url.lstrip('/')
        return url

    def add_jpeg(self, filename):
        '''
        add .jpeg to filename
        '''
        if not re.search(regex_patterns['filetype'], filename):
            filename += '.jpeg'
        return filename

    def get_netloc(self, url):
        '''
        return netloc of a url
        '''
        return urlparse(url)[1]

    def is_relative(self, url):
        '''
        check if url is relative
        '''
        if not self.get_netloc(url):
            return True
        else:
            return False

    def make_absolute(self, url, relative):
        '''
        convert relative url to absolute
        '''
        return self.get_netloc(url) + f'/{relative}'

    def unescape(self, url):
        '''
        substitute escape characters for ascii counterparts
        '''
        for key in escape_to_ascii:
            if key in url:
                url = url.replace(key, escape_to_ascii[key])
        return url

    def finalize(self, url):
        '''
        prepare a url for downloading
        '''
        return self.add_scheme(self.unescape(url.strip('/')))
