import re
from urllib.parse import urlparse, unquote


class Parser:

    '''generic parsing methods'''

    def __init__(self):
        self.filename_pat = r'(/?[^/]+(\.\w+)?)$'
        self.query_pat = r'\?[^" ]+$'
        self.filetype_pat = r'\.[A-Za-z0-9]+'
        self.filetypes = r'\.(jpe?g|png|gif|mp4|web(p|m)|tiff?)'
        self.tag_pat = r'<[^>]+>'
        self.filter_pat = r'\.(js|css|pdf)|(fav)?icon|logo|menu'
        self.cropping_pats = [
            r'(@|-|_)?(\d{3,4}x(\d{3,4})?|(\d{3,4})?x\d{3,4})',
            r'(-|_)?(large|big|thumb)(-|_)?',
            r'c_fill,f_auto,g_north,h_\d+,q_auto:best,w_\d+/v1/',
            r'expanded_[a-z]+/',
            r'(\.|-)\d+w',
            # BUG: \-e\d+ catches some dashed filenames by mistake, consider changing
            # r'\-e\d+'
            r'/v/\d/.+\.webp$'
            # BUG: removing legitimate url portions
            # r'w/\d+/'
        ]

    def extract_filename(self, url):
        '''extracts filename from url'''
        try:
            return re.sub(self.filetype_pat, '', re.search(self.filename_pat, self.dequery(url)).group().strip('/'))
        except AttributeError:
            return 'image'

    def decrop(self, url):
        '''removes common cropping from url'''
        for pat in self.cropping_pats:
            url = re.sub(pat, '', url)
        return url

    def dequery(self, url):
        '''remove query string from url'''
        return re.sub(self.query_pat, '', url)

    def sanitize(self, url):
        '''combines dequery and decrop'''
        return self.decrop(self.dequery(url))

    def filetype(self, url):
        '''extract file type'''
        type = re.search(self.filetypes, url, re.IGNORECASE)
        if not type:
            return 'jpeg'
        return type.group().lstrip('.').replace('jpg', 'jpeg')

    def add_scheme(self, url):
        '''checks for and adds scheme'''
        if not urlparse(url)[0]:
            url = 'https://' + url.lstrip('/')
        return url

    def add_jpeg(self, filename):
        '''add .jpeg to filename'''
        if not re.search(regex_patterns['filetype'], filename):
            filename += '.jpeg'
        return filename

    def get_netloc(self, url):
        '''return netloc of a url'''
        return urlparse(url)[1]

    def is_relative(self, url):
        '''check if url is relative'''
        if self.get_netloc(self.add_scheme(url)) == '':
            return True
        else:
            return False

    def make_absolute(self, relative):
        '''convert relative url to absolute'''
        return self.get_netloc(self.args['url']) + relative


    def finalize(self, url):
        '''
        prepare a url for downloading
        '''
        if self.is_relative(url):
            url = self.make_absolute(url)
        return self.add_scheme(unquote(url.strip('/')))

    def make_unique(self, filename):
        '''make filename unique'''
        n = 1
        while True:
            unique = f'({n}).'.join(filename.split('.'))
            if os.path.exists(unique):
                n += 1
            else:
                return unique

    def auto_format(self, url):
        '''attempt to upgrade common image types'''
        url = self.sanitize(url)
        if 'squarespace' in url:
            url += '?format=original'
        if 'wix' in url:
            url = re.sub(r'\.jpg.+$', '', url) + '.jpg'
        return url

    def user_format(self, url):
        '''add, substitute, or remove elements from a url'''
        if self.args['format'][0] == 'add':
            return url + self.args['format'][1]
        elif self.args['format'][0] == 'sub':
            return re.sub(self.args['format'][1], self.args['format'][2], url)
        elif self.args['format'][0] == 'rem':
            return re.sub(self.args['format'][1], '', url)
        else:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <WARNING> unknown format')
            return url
