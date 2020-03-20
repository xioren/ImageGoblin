import re
import os
from time import sleep
from strings import *
from handlers.meta_goblin import MetaGoblin


class OmegaGoblin(MetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.format = format
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'omega goblin'

    def custom_format(self, url):
        '''
        add, substitute, or remove elements from a filename/url pair
        '''
        self.format = self.format.split(' ')
        if self.format[0] == 'add':
            return url + self.format[1]
        elif self.format[0] == 'sub':
            return re.sub(self.format[1], self.format[2], url)
        elif self.format[0] == 'rem':
            return re.sub(self.format[1], '', url)
        elif format == 'auto':
            url = self.sanitize(url)
            if 'squarespace' in url:
                url += '?format=original'
        else:
            pass
        return url

    def find_links(self):
        '''
        extract media urls from html
        '''
        links = {l.group() for l in re.finditer(regex_patterns['link_pattern'], self.get_html(self.url), re.IGNORECASE)}
        return [re.sub(r'<img.+src="', '', l) for l in links]

    def download_media(self, links):
        '''
        retrieve media
        '''
        for link in links:
            print(f'[{self.__str__()}] <downloading> link {links.index(link) + 1} of {len(links)}')
            if self.format:
                link = self.custom_format(link)
            self.loot(link)
            sleep(self.tickrate)
        if not self.nodl:
            self.cleanup(self.path_main)

    def run(self):
        links = self.find_links()
        self.download_media(links)
