import re
import os
from time import sleep
from strings import *
from handlers.meta_goblin import MetaGoblin


class OmegaGoblin(MetaGoblin):

    '''
    generic goblin for links that did not trigger a handler match
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'generic goblin'

    def custom_format(self, url):
        '''
        add, substitute, or remove elements from a filename/url pair
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

    def find_links(self):
        '''
        extract media urls from html
        '''
        links = self.extract_links(regex_patterns['link_pattern'], self.args['url'])
        return [re.sub(r'<img.+src="', '', link) for link in links]

    def download_media(self, links):
        '''
        retrieve media
        '''
        for link in links:
            # print(f'[{self.__str__()}] <looting> link {links.index(link) + 1} of {len(links)}')
            if self.args['format']:
                link = self.custom_format(link)
            self.loot(link)
            sleep(self.args['tickrate'])
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)

    def run(self):
        links = self.find_links()
        self.download_media(links)
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
