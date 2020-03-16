import re
from urllib.parse import urlparse
from strings import *


def instagram(url):
    '''
    return instagram username
    '''
    return re.search(regex_patterns['insta_username'], url).group().strip('/')


def dl_prep(url):
    '''
    prepares url and filename for download
    '''
    filename = re.search(regex_patterns['filename'], url)
    if filename:
        return add_scheme(url), add_jpeg(strip_query(filename.group()))
    else:
        return add_scheme(url), 'image.jpeg'


def remove_format(url, name):
    '''
    removes common formatting
    '''
    for pat in format_patterns:
        url = re.sub(pat, '', url)
        name = re.sub(pat, '', name)
    return url, name


def custom_format(url, name, format):
    '''
    add, substitute, or remove elements from a filename/url pair
    '''
    parts = format.split(' ')
    if parts[0] == 'add':
        assert len(parts) == 2
        url = url.strip('\n') + parts[1]
    elif parts[0] == 'sub':
        assert len(parts) == 3
        url = re.sub(parts[1], parts[2], url)
        name = re.sub(parts[1], parts[2], name)
    elif parts[0] == 'rem': # remove
        assert len(parts) == 2
        url = re.sub(parts[1], '', url)
        name = re.sub(parts[1], '', name)
    elif format == 'auto':
        url, name = remove_format(url, name)
        if 'squarespace' in url:
            url = url + '?format=original'
    else:
        pass
    return url, name


def remove_slashes(string):
    '''
    remove redundent forward slashes
    '''
    return re.sub('//', '/', string)


def add_scheme(url):
    '''
    checks for and adds scheme
    '''
    if not urlparse(url)[0]:
        url = 'https://' + url
    return url


def add_jpeg(name):
    '''
    add .jpeg to filename
    '''
    if not re.search(r'\.\w+$', name):
        name += '.jpeg'
    return name


def make_unique(name, n=0):
    '''
    makes filename unique
    '''
    return f'({n}).'.join(re.split(r'\.', name))


def get_netloc(url):
    '''
    return netloc of a url
    '''
    return urlparse(url)[1]


def link_finder(data, url):
    '''
    method for extracting image urls from html
    '''
    link_table = []
    links = re.finditer(regex_patterns['link_pattern'], data, re.IGNORECASE)
    for link in links:
        link = unescape(link.group().strip('"').lstrip('/'))
        if re.search(regex_patterns['filter'], link):
            continue
        if is_relative(link):
            link = make_absolute(url, link)
        if link not in link_table:
            link_table.append(link)
    return link_table


def iter_finder(url):
    '''
    seperate iterable from a url (mode 3)
    '''
    return re.split('%%%', url)


def parse_html(html):
    '''
    parses page links from html (instagram)
    '''
    link_table = []
    tags = re.finditer(f'<a href.+?>', html)
    for tag in tags:
        link = tag.group()
        if re.search(regex_patterns['insta_link'], link):
            link_table.append(f'https://www.instagram.com{link[9:-2]}')
    return link_table


def parse_content(html):
    '''
    parses media links from html (instagram)
    '''
    link_table = []
    tags = re.finditer(f'<.+>', html)
    for tag in tags:
        matches = re.finditer(regex_patterns['link_pattern'], tag.group())
        for link in matches:
            link = unescape(link.group())
            if re.search(regex_patterns['insta_crop'], link):
                continue
            if link not in link_table:
                link_table.append(link)
    return link_table


def insta_prep(url):
    '''
    parse filename from url
    '''
    return strip_query(re.search(regex_patterns['filename'], url).group().strip('/'))


def insta_check(url):
    '''
    verify instagram link
    '''
    if re.search('instagram', url):
        return True
    else:
        return False


def is_relative(url):
    '''
    check if url is relative
    '''
    if not get_netloc(url):
        return True
    else:
        return False


def strip_query(string):
    '''
    remove query string
    '''
    return re.sub(regex_patterns['query'], '', string)


def make_absolute(url, relative):
    '''
    convert relative url to absolute
    '''
    return get_netloc(url) + relative


def add_slash(path):
    '''
    add forward slash to end of filepath
    '''
    if not path[-1] == '/':
        path += '/'
    return path


def unescape(url):
    for key in escape_to_ascii:
        if key in url:
            url = url.replace(key, escape_to_ascii[key])
    return url
