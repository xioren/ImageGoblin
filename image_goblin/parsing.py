import re
import json
import mimetypes
import urllib.parse

from os.path import join, exists


class Parser:
    '''generic url/html parsing and manipulation utilities'''

    QUALITY_PAT = re.compile(r'q((ua)?li?ty)?=\d+')
    FILTER_PAT = re.compile(r'(?:\.(js|css|pdf|php|html|svg(\+xml)?)|favicon|[{}]|\+[\w\.]+\+)', flags=re.IGNORECASE)
    MISC_REPLACEMENTS = {'amp;': '', 'background-image:url(': ''}
    ABSOLUTE_PAT = r'(?:/?[^/\.]+\.[^/]+(?=/))'
    CROPPING_PATS = (
        re.compile(r'[\-_]?((x+)?-?(?<!\w)l(arge)?(?!\w)|profile|square)(?![\w])[\-_/]?', flags=re.IGNORECASE),
        re.compile(r'[@\-_/]\d+x(\d+)?(?![a-z\d])'), # 000x000
        re.compile(r'expanded_[a-z]+/'),
        re.compile(r'(?<=/)[a-z]_.+?/v\d/'), # cloudfront
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
        '''html tag parser'''

        ELEMENT_PAT = re.compile(r'<[a-z]+\s[^>]+>')
        TAG_PAT = re.compile(r'(?<=<)[a-z\-]+')
        ATTRIBUTE_PAT = re.compile(r'[a-z\d\-]+="[^"]+')

        def __init__(self, content):
            self.html = content
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

    def extract_by_tag(self, html, tags:'[(tag,attr)]'=None):
        '''extract from html by tag'''
        if html:
            html_parser = self.GoblinHTMLParser(html)
            html_parser.parse_elements()

            if tags:
                urls = []
                for item in tags:
                    tag, attr = item
                    if tag in html_parser.elements:
                        urls.extend(html_parser.elements[tag].get(attr))
                return urls
            else:
                return html_parser.elements

        return ''

    def extract_by_regex(self, html, pattern):
        '''extract from html by regex'''
        try:
            return {match.group().replace('\\', '') for match in re.finditer(pattern, html)}
        except TypeError:
            return ''

    def extract_filename(self, url):
        '''extract filename from url'''
        filename = self.dequery(url).rstrip('/').split('/')[-1]
        return re.sub(r'\.\w{,4}$', '', filename)

    def decrop(self, url):
        '''remove common cropping from url'''
        for pat in self.CROPPING_PATS:
            url = re.sub(pat, '', url)
        return url

    def dequery(self, url):
        '''remove query string from url'''
        return url.split('?')[0]

    def sanitize(self, url):
        '''combine dequery and decrop'''
        return self.decrop(self.dequery(url))

    def make_url_safe(self, url):
        '''quote control characters in url (filename portion only)'''
        # NOTE: some morons have both quoted and unquoted control characters in the same url,
        # easiest approach --> just unquote then requote all filenames.
        filename = self.extract_filename(url)

        return url.replace(filename, urllib.parse.quote(urllib.parse.unquote(filename)))

    def extension(self, url):
        '''extract file extension from url'''
        ext = mimetypes.guess_type(self.dequery(url))[0]
        if ext:
            return f'.{ext.split("/")[1]}'.replace('svg+xml', 'svg')
        return ''

    def add_scheme(self, url):
        '''checks for and adds https scheme'''
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
        - handle control characters
        '''
        if re.search(self.ABSOLUTE_PAT, url): # absolute path
            url = self.add_scheme(url.lstrip('/'))
        else: # relative path
            url = urllib.parse.urljoin(self.origin_url, url)

        for item in self.MISC_REPLACEMENTS:
            url = url.replace(item, self.MISC_REPLACEMENTS[item])

        return self.make_url_safe(url).rstrip(')')

    def make_unique(self, path):
        '''make filepath unique'''
        n = 1
        while True:
            new_path = join(path, f'({n}).'.join(path.split('.')))
            if exists(new_path):
                n += 1
            else:
                return new_path

    def safe_search(self, pat, string):
        '''safely make one line regex searches'''
        # QUESTION: keep?
        match = re.search(pat, string)
        if match:
            return match.group()
        return ''

    def filter(self, url):
        '''filter unwanted urls'''
        if re.search(self.FILTER_PAT, url):
            return True
        return False

    def safe_load_json(self, json_string):
        '''load JSON safely and if necessary fix improper use of double quote delimiters (*cough* imgur)'''
        if not json_string:
            return {}
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            json_string = json_string.replace('\n', '').replace('\.', '.')
            values = re.finditer(r'(?<=:").+?(?="(,"|}))', json_string)
            for val in values:
                val = val.group()
                json_string = json_string.replace(val, val.replace('"', "'"))
            try:
                return json.loads(json_string)
            except json.JSONDecodeError:
                return {}

    def user_format(self, url):
        '''add, substitute, or remove arbitrary elements from a url'''
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
                url = re.sub(r'\d+(?=\.gif)', '540', url)
            else:
                url = re.sub(r'\d+(?=\.jpg)', '1280', url)
        elif 'wix' in url:
            url = re.sub(r'(?<=\.jpg).+$', '', url)

        if quality:
            url += '?{}'.format(re.sub(r'\d+', '100', quality.group()))

        return url
