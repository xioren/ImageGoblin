import re
from urllib.parse import urlparse
from strings import *


def insta_username(url):
    '''
    extract instagram username
    '''
    return re.search(regex_patterns['insta_username'], url).group().strip('/')


def extract_filename(url):
    '''
    extracts filename from url
    '''
    return re.sub(regex_patterns['filetype'], '', re.search(regex_patterns['filename'], dequerry(url)).group().strip('/'))


def decrop(url):
    '''
    removes common cropping from url
    '''
    for pat in format_patterns:
        url = re.sub(pat, '', url)
    return url


def dequerry(url):
    '''
    remove querry string from url
    '''
    return re.sub(regex_patterns['querry'], '', url)


def filetype(url):
    '''
    extract file type
    '''
    type = re.search(regex_patterns['type_id'], url, re.IGNORECASE)
    if not type:
        return 'jpeg'
    return type.group().lstrip('.')


def custom_format(url, format):
    '''
    add, substitute, or remove elements from a filename/url pair
    '''
    if format[0] == 'add':
        assert len(format) == 2
        url = url.strip('\n') + format[1]
    elif format[0] == 'sub':
        assert len(format) == 3
        url = re.sub(format[1], format[2], url)
    elif format[0] == 'rem':
        assert len(format) == 2
        url = re.sub(format[1], '', url)
    elif format == 'auto':
        url = decrop(dequerry(url))
        if 'squarespace' in url:
            url += '?format=original'
    else:
        pass
    return url


def add_scheme(url):
    '''
    checks for and adds scheme
    '''
    if not urlparse(url)[0]:
        url = 'https://' + url
    return url


def add_jpeg(filename):
    '''
    add .jpeg to filename
    '''
    if not re.search(regex_patterns['filetype'], filename):
        filename += '.jpeg'
    return filename


def get_netloc(url):
    '''
    return netloc of a url
    '''
    return urlparse(url)[1]


def link_finder(url, html):
    '''
    method for extracting image urls from html
    '''
    link_table = []
    links = re.finditer(regex_patterns['link_pattern'], html, re.IGNORECASE)
    for link in links:
        link = unescape(link.group().strip('"').lstrip('/'))
        if not re.search(regex_patterns['link_filter'], link):
            continue
        if re.search(regex_patterns['filter'], link):
            continue
        if is_relative(link):
            link = make_absolute(url, link)
        if link not in link_table:
            link_table.append(link)
    return link_table


def extract_iterable(url):
    '''
    seperate iterable from a url (mode 3)
    '''
    return re.split('%%%', url)


def parse_posts(html):
    '''
    parses posts from html (instagram)
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
        matches = re.finditer(regex_patterns['insta_media'], tag.group())
        for link in matches:
            link = unescape(link.group())
            if re.search(regex_patterns['insta_crop'], link):
                continue
            if link not in link_table:
                link_table.append(link)
    return link_table


def is_relative(url):
    '''
    check if url is relative
    '''
    if not get_netloc(url):
        return True
    else:
        return False


def make_absolute(url, relative):
    '''
    convert relative url to absolute
    '''
    return get_netloc(url) + f'/{relative}'


def unescape(url):
    '''
    substitute escape characters for ascii counterparts
    '''
    for key in escape_to_ascii:
        if key in url:
            url = url.replace(key, escape_to_ascii[key])
    return url
