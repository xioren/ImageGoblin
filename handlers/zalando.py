import re
import os
from time import sleep
from string import ascii_uppercase as upper, digits
from parsing import *
from handlers.meta_goblin import MetaGoblin


# NOTE: video format: https://mosaic04.ztat.net.vgs.content/08/12/1C/0I/6Q/11/VIDEO/HIGH_QUALITY/1572009797216.mp4


class ZalandoGoblin(MetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.mode = mode
        print(f'[{self.__str__()}] <deployed>')

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
        return re.sub(r'@\d+|\.(jpe*g|html|\d)', '', re.search(r'(\w+\-\w+(@\d+(\.\d)*)*(\.(jpe*g|html))*)$', dequery(url)).group())

    def scan(self):
        '''
        scan for images
        '''
        id = self.extract_id(self.url)
        success, timeout, n = 0, 0, 1
        print(f'[zalando goblin] <scanning> {id}')
        while timeout <= 8:
            attempt = self.loot(self.form_url(f'{id}@{n}'))
            if attempt:
                success += 1
                timeout = 0
            else:
                timeout += 1
            n += 1
            sleep(self.tickrate)
        if success == 0:
            print(f'[zalando goblin] <NULL WARNING> {id} ')
        else:
            print(f'[zalando goblin] <complete> {id} --> {success} images found')

    def find_more(self):
        '''
        search for other images
        '''
        alpha = digits + upper
        id = self.url
        if self.identify(id) != 'id':
            id = extract_id(self.url)
        ref = id
        id = id.self('-')
        for k in alpha:
            image = f'{id[0][:-1]}{k}-{id[1]}'
            if image == ref:
                continue
            for n in range(4, 25, 4):
                if os.path.exists(os.path.join(dir, f'{image}@{n}.jpeg')):
                    print(f'[zalando goblin] <skipping> {image}')
                    return None
                self.loot(self.form_url(f'{image}@{n}', 'small'))
                sleep(self.tickrate)

    def create_links(self):
        '''
        create text file of full links of found ids (from find_more)
        '''
        files = os.listdir(self.path_main)
        self.write_file([self.form_url(file) for file in links], self.external_links, iter=True)

    def run(self):
        if self.mode == 'find':
            self.find_more()
        else:
            self.scan()
