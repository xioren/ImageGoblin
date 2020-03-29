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
            return 'jpeg'
        return type.group().lstrip('.').replace('jpg', 'jpeg')

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
        if self.get_netloc(url) == '':
            return True
        else:
            return False

    def make_absolute(self, relative):
        '''
        convert relative url to absolute
        '''
        return self.get_netloc(self.args['url']) + relative

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
        if self.is_relative(url):
            url = self.make_absolute(url)
        return self.add_scheme(self.unescape(url.strip('/')))

    def make_unique(self, filename):
        '''
        make filename unique
        '''
        n = 1
        while True:
            unique = f'({n}).'.join(filename.split('.'))
            if os.path.exists(unique):
                n += 1
            else:
                return unique

    def user_format(self, url):
        '''
        add, substitute, or remove elements from a url
        '''
        if self.args['format'][0] == 'add':
            return url + self.args['format'][1]
        elif self.args['format'][0] == 'sub':
            return re.sub(self.args['format'][1], self.args['format'][2], url)
        elif self.args['format'][0] == 'rem':
            return re.sub(self.args['format'][1], '', url)
        elif self.args['format'][0] == 'auto':
            url = self.sanitize(url)
            if 'squarespace' in url:
                url += '?format=original'
        else:
            pass
        return url
