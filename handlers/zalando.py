import re
import os
from time import sleep
from string import ascii_uppercase as upper, digits
from handlers.meta_goblin import MetaGoblin


# NOTE: video format: https://mosaic04.ztat.net.vgs.content/08/12/1C/0I/6Q/11/VIDEO/HIGH_QUALITY/1572009797216.mp4
# TODO: make conform to verbose rules


class ZalandoGoblin(MetaGoblin):

    '''
    accepts:
        - image
        - webpage
    '''

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'zalando goblin'

    def form_url(self, image, size='large'):
        '''
        form url from filename
        '''
        # TODO: does not handle digit.digit formats
        image = re.sub('.jpe*g', '', image).upper()
        if not re.search(r'@\d+', image):
            image += '@8'
        compounded = f'{image[:2]}/{image[2:4]}/{image[4:6]}/{image[6:8]}/'\
                     f'{image[8]}{image[10]}/{image[11:13]}/{image}'
        if size == 'small':
            return f'https://mosaic03.ztat.net/vgs/media/article/{compounded}.jpg?imwidth=300'
        else:
            return f'https://mosaic01.ztat.net/vgs/media/original/{compounded}.jpg'

    def identify(self, url):
        '''
        identify url type
        '''
        if '.html' in url:
            return 'page'
        elif len(url) < 15:
            return 'id'
        else:
            return 'image'

    def extract_id(self, url):
        '''
        extract image id
        '''
        # # WARNING: will throw exception if non zalando images are input
        # QUESTION: can this handle digit.digit formats?
        return re.sub(r'@\d+|\.(jpe*g|html|\d)', '', re.search(r'(\w+\-\w+(@\d+(\.\d)*)*(\.(jpe*g|html))*)$', self.dequery(url)).group())

    def scan(self):
        '''
        scan for images
        '''
        self.toggle_collecton_type()
        id = self.extract_id(self.args['url'])
        for n in range(1, 50):
            self.collect(self.form_url(f'{id}@{n}'))

    def find_more(self):
        '''
        search for other images
        '''
        alpha = digits + upper
        id = self.extract_id(self.args['url'])
        ref = id
        id = id.split('-')
        for k in alpha:
            new_id = f'{id[0][:-1]}{k}-{id[1]}'
            if new_id == ref:
                continue
            for n in range(4, 25, 4):
                self.collect(self.form_url(f'{new_id}@{n}', 'small'))

    def create_links(self):
        '''
        create text file of full links of found ids (from find_more)
        '''
        files = os.listdir(self.path_main)
        self.write_file([self.form_url(file) for file in links], self.external_links, iter=True)

    def run(self):
        if self.args['mode'] == 'find':
            self.find_more()
            self.loot()
        else:
            self.scan()
            self.loot(timeout=8)
        print(f'[{self.__str__()}] <looted> {self.loot_tally} files')
