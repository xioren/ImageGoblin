import os
import re
from time import sleep
from handlers.meta_goblin import MetaGoblin


class InstagramGoblin(MetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.username = self.extract_username(self.args['url'])
        self.html_local = os.path.join(os.getcwd(), 'html.txt')
        self.sub_dir = os.path.join(self.path_main, self.username)
        self.link_pat = r'https://scontent[^"\n \']+_n\.[^"\n \']+'
        self.make_dirs(self.sub_dir)

    def __str__(self):
        return 'instagram goblin'

    def extract_username(self, url):
        '''
        extract instagram username
        '''
        return re.search(r'(/*[^/]+/*)$', url).group().strip('/')

    def move_vid(self, path):
        '''
        move videos into seperate directory
        '''
        dirpath = os.path.join(path, 'vid')
        if os.path.exists(dirpath) is False:
            os.mkdir(dirpath)
        for file in os.listdir(path):
            if '.mp4' in file:
                os.rename(os.path.join(path, file), os.path.join(dirpath, file))

    def find_posts(self):
        '''
        parse html for instagram posts
        '''
        return {post.group() for post in re.finditer(r'/p/[^"]+', self.read_file(self.html_local))}

    def find_media(self, posts):
        '''
        opens links from iterable and parses for media
        '''
        for post in posts:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <parsing> {post}')
            content = self.extract_links(self.link_pat, f'https://www.instagram.com{post}')
            for link in content:
                if re.search(r'/[a-z]\d{3}x\d{3}/|ig_cache_key', link):
                    continue
                self.collect(link.replace(r'\u0026', '&'), f'{self.username}_{self.extract_filename(link)}')
            sleep(self.args['tickrate'])

    def run(self):
        posts = self.find_posts()
        media = self.find_media(posts)
        self.loot(save_loc=self.sub_dir)
        self.move_vid(self.sub_dir)
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.sub_dir)
