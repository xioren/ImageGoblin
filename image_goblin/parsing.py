import re

from urllib.parse import urlparse, unquote

# IDEA: consider implementing re.compile

class Parser:
    '''generic parsing methods'''

    def __init__(self):
        self.filename_pat = r'(?<=/)[^/]+$'
        self.query_pat = r'[\?&][^" ]+$'
        self.quality_pat = r'q((ua)?li?ty)=\d+'
        self.filetype_pat = r'(?<=\.)[A-Za-z0-9]+'
        self.filetypes = r'\.(jpe?g|png|gif|mp4|web[pm]|tiff?|mov|svg|bmp|exif)'
        self.filter_pat = r'\.(js|css|pdf|php|html)|(fav)?icon|logo|menu'
        self.cropping_pats = (
            r'[@\-_/]?((\d{3,4}x(\d{3,4})?|(\d{3,4})?x\d{3,4}))',
            r'(-|_)?large(-|_)?',
            r'(?<=/)([a-z]{,2}_[\w:]+(,|/)?)+/v\d+/', # cloudfront
            r'expanded_[a-z]+/',
            r'(\.|-)\d+w',
            r'-e\d+(?=\.)',
            r'/v/\d/.+\.webp$'
        )

    def extract_filename(self, url):
        '''extracts filename from url'''
        try:
            return re.sub(r'\..+$', '', re.search(self.filename_pat, self.dequery(url)).group())
        except AttributeError as e:
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
        type = re.search(f'{self.filetype_pat}$', self.dequery(url), re.IGNORECASE)
        if not type:
            return 'jpeg'
        return type.group().replace('jpg', 'jpeg')

    def add_scheme(self, url):
        '''checks for and adds scheme'''
        if not urlparse(url)[0]:
            url = f'https://{re.sub(r"^/{2,}", "", url)}'
        return url

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
        return self.get_netloc(self.args['targets'][self.__repr__()][0]) + relative

    def finalize(self, url):
        '''prepare a url for an http request'''
        if self.is_relative(url):
            url = self.make_absolute(url)
        return self.add_scheme(unquote(url.strip('/')))

    def make_unique(self, filename):
        '''make filename unique'''
        # FIXME: unused and not up to date with current
        # if kept, needs a filepath arg or something along those lines
        n = 1
        while True:
            unique = f'({n}).'.join(filename.split('.'))
            if os.path.exists(unique):
                n += 1
            else:
                return unique

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

    def auto_format(self, url):
        '''attempt to upscale common url formats'''
        quality = re.search(self.quality_pat, url)
        url = self.sanitize(url)
        if 'acidimg' in url:
            url = url.replace('small', 'big')
        elif 'imagetwist' in url:
            url = url.replace('/th/', '/i/').replace('.jpg', '.JPG')
        elif 'imgbox' in url:
            if '-t' in url or '.t' in url:
                url = re.sub(r'\d[\-\.]t', 'i', url)
            else:
                url = url.replace('_t', '_o').replace('thumb', 'image')
        elif 'imgcredit' in url:
            url = url.replace('.th', '').replace('.md', '')
        elif 'imgur' in url:
            filename = re.search(r'[^/]+$', url).group()
            if len(filename) == 11:
                pass
            else:
                url = 'https://i.imgur.com/{}'.format(re.sub(r'\w\.', '.', filename))
        elif 'imx.to' in url:
            url = url.replace('/t/', '/i/')
        elif 'pimpandhost' in url:
            url = url.replace('_s', '').replace('_m', '')
        elif 'pinimg' in url:
               url = re.sub(r'\.com/', '.com/originals/', url)
        elif 'pixhost' in url:
            url = re.sub(r't(?![a-z])', 'img', url.replace('thumb', 'image'))
        elif 'pixroute' in url:
            url = url.replace('_t', '')
        elif 'squarespace' in url:
            url += '?format=original'
        elif 'tumblr' in url:
            if '.gif' in url:
                url = re.sub(r'\d+(?=\.gif)', '500', url)
            else:
                url = re.sub(r'\d+(?=\.jpg)', '1280', url)
        elif 'wix' in url:
            url = re.sub(r'(?<=\.jpg).+$', '', url)
        if quality:
            url += '?{}'.format(re.sub(r'\d+', '100', quality.group()))
        return url
