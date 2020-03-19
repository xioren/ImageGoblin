import os
from time import sleep
from handlers.meta_goblin import MetaGoblin
from parsing import *


class OmegaGoblin(MetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.format = format
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'omega goblin'

    def link_grab(self):
        '''
        parse html for media links
        '''
        print(f'[{self.__str__()}] <parsing> {self.url}')
        html = self.get_html(self.url)
        if html:
            links = link_finder(self.url, html)
            print(f'[{self.__str__()}] <parse complete> {len(links)} links found')
            if self.nodl == 1:
                for link in links:
                    print(link)
        else:
            print('[{self.__str__()}] <ERROR> no html recieved')
            return None
        return links

    def link_dl(self, links):
        '''
        retrieve media
        '''
        assert links
        downloaded = []
        for link in links:
            print(f'[{self.__str__()}] <downloading> link {links.index(link) + 1} of {len(links)}')
            if self.format:
                link = custom_format(link, self.format)
            if link not in downloaded:
                downloaded.append(link)
                self.loot(link)
            sleep(self.tickrate)
        self.cleanup(self.path_main)

    def run(self):
        links = self.link_grab()
        if not self.nodl:
            self.link_dl(links)
