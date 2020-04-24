import re
import urllib.parse

from os.path import join, exists


# TEMP:
# - <meta property="og:image" content="
# - og:image(:secure_url)?" content="[^"]+
# - background-image:[^"]+"[^"]+

class Parser:
    '''generic url/html parsing and manipulation methods'''

    def __init__(self, origin_url, user_formatting):
        self.origin_url = origin_url
        self.user_formatting = user_formatting
        self.filename_pat = re.compile(r'(?<=/)[^/]+$')
        self.query_pat = re.compile(r'[\?&][^" ]+$')
        self.quality_pat = re.compile(r'q((ua)?li?ty)=\d+')
        self.filetype_pat = re.compile(r'(?<=\.)[A-Za-z0-9]+$', flags=re.IGNORECASE)
        # IDEA: add mimetype id'ing from headers?
        self.filetypes = r'\.(jpe?g|png|gif|mp4|web[pm]|tiff?|mov|svg|bmp|exif)'
        self.cropping_pats = (
            re.compile(r'[@\-_/]?((\d{3,4}x(\d{3,4})?|(\d{3,4})?x\d{3,4}))'), # 000x000
            re.compile(r'[\-_](large|profile)|(large|profile)[\-_]'),
            re.compile(r'(?<=/)([a-z]{,2}_[\w:]+(,|/)?)+/v\d+/'), # cloudfront
            re.compile(r'expanded_[a-z]+/'),
            re.compile(r'(\.|-)\d+w'), # -000w
            re.compile(r'-e\d+(?=\.)'),
            re.compile(r'/v/\d/.+\.webp$'),
            re.compile(r'@\d+x')
        )

####################################################################
# sub classes
####################################################################

    class GoblinHTMLParser:

        def __init__(self, content):
            self.html = content
            self.attributes = {}
            self.element_pat = re.compile(r'<[a-z]+ [^>]+>')
            self.tag_pat = re.compile(r'(?<=<)[a-z\-]+')
            self.attribute_pat = re.compile(r'[a-z\d\-]+="[^"]+')
            self.elements = {}

        def parse_elements(self):
            '''extract and sort all elements from an html source'''
            elements = re.finditer(self.element_pat, self.html)
            for element in elements:
                element = element.group()
                tag = re.search(self.tag_pat, element).group()
                if tag not in self.elements:
                    self.elements[tag] = {}
                attributes = re.finditer(self.attribute_pat, element)
                for attribute in attributes:
                    attr, value = attribute.group().split('="')
                    if attr not in self.elements[tag]:
                        self.elements[tag][attr] = [value]
                    else:
                        self.elements[tag][attr].append(value)

####################################################################
# methods
####################################################################

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

    def strip_attribute(self, url):
        '''strip attribute from url'''
        return re.sub('[^"]+"', '', url)

    def filetype(self, url):
        '''extract file type'''
        type = re.search(self.filetype_pat, self.dequery(url))
        if not type:
            return 'jpeg'
        return type.group().replace('jpg', 'jpeg')

    def add_scheme(self, url):
        '''checks for and adds scheme'''
        if not urllib.parse.urlparse(url)[0]:
            if url.startswith('.') or url.startswith('/'):
                pass
            else:
                return f'https://{url}'
        return url

    def finalize(self, url):
        '''prepare a url for an http request'''
        if '/' not in url:
            url = self.add_scheme(self.dequery(self.origin_url)) + url
        else:
            url = urllib.parse.urljoin(self.add_scheme(self.origin_url),
                                       self.add_scheme(url))
        return urllib.parse.unquote(url)

    def make_unique(self, path, filename):
        '''make filename unique'''
        n = 1
        while True:
            new_path = join(path, f'({n}).'.join(filename.split('.')))
            if exists(new_path):
                n += 1
            else:
                return new_path

    def user_format(self, url):
        '''add, substitute, or remove elements from a url'''
        if self.args['format'][0] == 'add':
            return url + self.user_formatting[1]
        elif self.args['format'][0] == 'sub':
            return re.sub(fr'{self.user_formatting[1]}', self.user_formatting[2], url)
        elif self.args['format'][0] == 'rem':
            return re.sub(fr'{self.user_formatting[1]}', '', url)
        else:
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
