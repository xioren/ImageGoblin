import re
import os
from strings import *
from handlers.meta_goblin import MetaGoblin


class OmegaGoblin(MetaGoblin):

    '''
    generic goblin for links that did not match a handler
    accepts:
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'generic goblin'

    def find_links(self):
        '''
        extract media urls from html
        '''
        links = self.extract_links(regex_patterns['link_pattern'], self.args['url'])
        cleaned_links = [re.sub(r'<img.+src="', '', link) for link in links]
        for link in cleaned_links:
            if self.args['format']:
                link = self.custom_format(link)
            self.collect(link)

    def run(self):
        if self.args['all']:
            with open(os.path.join(os.getcwd(), self.args['local'])) as file:
                links = set(file.read().splitlines())
            for link in links:
                if self.args['format']:
                    link = self.user_format(link)
                self.collect(link)
        else:
            links = self.find_links()
        self.loot()
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.path_main)
