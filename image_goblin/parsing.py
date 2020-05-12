import re
import mimetypes
import urllib.parse

from os.path import join, exists


class Parser:
    '''generic url/html parsing and manipulation methods'''

    FILENAME_PAT = re.compile(r'(?<=/|\\)[^\\/]+$')
    QUERY_PAT = re.compile(r'[\?&][^"\s]+$')
    QUALITY_PAT = re.compile(r'q((ua)?li?ty)?=\d+')
    CROPPING_PATS = (
        re.compile(r'[\-_]?(?<![a-z])((x+)?-?l(arge)?|profile)(?![a-z])[\-_]?', flags=re.IGNORECASE),
        re.compile(r'[@\-_/]\d+x(\d+)?(?![a-z\d])'), # 000x000
        re.compile(r'expanded_[a-z]+/'),
        re.compile(r'(?<=/)c_.+?/v1/'), # cloudfront
        re.compile(r'/v/\d/.+\.webp$'),
        re.compile(r'-e\d+(?=\.)'),
        re.compile(r'(\.|-)\d+w'), # -000w
        re.compile(r'@\d+x')
    )

    def __init__(self, origin_url, user_formatting):
        self.origin_url = self.add_scheme(self.dequery(origin_url))
        self.user_formatting = user_formatting
        mimetypes.add_type('image/webp', '.webp')

####################################################################
# sub classes
####################################################################

    class GoblinHTMLParser:

        ELEMENT_PAT = re.compile(r'<[a-z]+\s[^>]+>')
        TAG_PAT = re.compile(r'(?<=<)[a-z\-]+')
        ATTRIBUTE_PAT = re.compile(r'[a-z\d\-]+="[^"]+')

        def __init__(self, content):
            self.html = content
            self.attributes = {}
            self.elements = {}

        def parse_elements(self):
            '''extract all elements from an html source'''
            for element in [e.group() for e in re.finditer(self.ELEMENT_PAT, self.html)]:
                tag = re.search(self.TAG_PAT, element).group()
                if tag not in self.elements:
                    self.elements[tag] = {}
                for attribute in re.finditer(self.ATTRIBUTE_PAT, element):
                    attr, value = attribute.group().split('="')
                    if attr not in self.elements[tag]:
                        self.elements[tag][attr] = [value]
                    else:
                        self.elements[tag][attr].append(value)

####################################################################
# methods
####################################################################

    def extract_filename(self, url):
        '''extract filename from url'''
        filename = re.search(self.FILENAME_PAT, self.dequery(url))
        return re.sub(r'\..+$', '', filename.group()) if filename else 'image'

    def decrop(self, url):
        '''remove common cropping from url'''
        for pat in self.CROPPING_PATS:
            url = re.sub(pat, '', url)
        return url

    def dequery(self, url):
        '''remove query string from url'''
        return re.sub(self.QUERY_PAT, '', url)

    def sanitize(self, url):
        '''combine dequery and decrop'''
        return self.decrop(self.dequery(url))

    def strip_attribute(self, url):
        '''strip attribute from url'''
        # QUESTION: is this used?
        return re.sub('[^"]+"', '', url)

    def extension(self, url):
        '''extract file extension from url'''
        ext = mimetypes.guess_type(self.dequery(url))[0]
        if ext:
            return ext.split('/')[1]
        return 'jpeg'

    def add_scheme(self, url):
        '''checks for and adds scheme'''
        if not urllib.parse.urlparse(url)[0]:
            if url.startswith('.') or url.startswith('/'):
                pass
            else:
                return f'https://{url}'
        return url

    def finalize(self, url):
        '''prepare a url for an http request
        - add missing scheme
        - expand relative urls
        - unquote quoted urls
        '''
        if '/' not in url: # just a filename
            url = f'{self.origin_url.rstrip('/')}/{url}'
        elif re.search(r'(?:/?[^/\.]+\.[^/]*(?=/))', url): # absolute path
            url = self.add_scheme(url.lstrip('/'))
        else:
            url = urllib.parse.urljoin(self.origin_url, url)
        return urllib.parse.unquote(url)

    def make_unique(self, path):
        '''make filepath unique'''
        n = 1
        while True:
            new_path = join(path, f'({n}).'.join(path.split('.')))
            if exists(new_path):
                n += 1
            else:
                return new_path

    def user_format(self, url):
        '''add, substitute, or remove elements from a url'''
        if self.user_formatting[0] == 'add':
            # QUESTION: add auto query formatting? use urlencode?
            return self.dequery(url) + self.user_formatting[1]
        elif self.user_formatting[0] == 'sub':
            return re.sub(fr'{self.user_formatting[1]}', self.user_formatting[2], url)
        elif self.user_formatting[0] == 'rem':
            return re.sub(fr'{self.user_formatting[1]}', '', url)
        else:
            return url

    def auto_format(self, url):
        '''attempt to upscale common url formats'''
        quality = re.search(self.QUALITY_PAT, url)
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
        elif 'imx.to' in url:
            url = url.replace('/t/', '/i/')
        elif 'i.mdel.net' in url:
            url = url.replace('.jpg', '-orig.jpg')
        elif 'pimpandhost' in url:
            url = url.replace('_s', '').replace('_m', '')
        elif 'pinimg' in url:
               url = re.sub(r'\.com/', '.com/originals/', url)
        elif 'pixhost' in url:
            url = re.sub(r't(?![a-z])', 'img', url.replace('thumb', 'image'))
        elif 'pixroute' in url:
            url = url.replace('_t', '')
        elif 'redd.it' in url:
            url = self.dequery(url).replace('preview', 'i')
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
