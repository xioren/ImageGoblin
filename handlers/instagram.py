import os
import re
from time import sleep
from strings import *
from handlers.meta_goblin import MetaGoblin


class InstagramGoblin(MetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        self.username = self.extract_username(self.url)
        self.html_txt = os.path.join(os.getcwd(), 'html.txt')
        self.sub_dir = os.path.join(self.path_main, self.username)
        self.make_dirs(self.sub_dir)
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'instagram goblin'

    def extract_username(self, url):
        '''
        extract instagram username
        '''
        return re.search(regex_patterns['insta_username'], url).group().strip('/')

    def find_posts(self):
        '''
        parse html for instagram posts
        '''
        print(f'[{self.__str__()}] <parsing> {self.username}')
        html = self.read_file(self.html_txt)
        assert html
        return {l.group() for l in re.finditer(r'/p/[^"]+', html)}

    def find_media(self, posts):
        '''
        opens links from iterable and parses for media
        '''
        links = set()
        assert posts
        for post in posts:
            # print(f'[{self.__str__()}] <parsing> post {posts.index(post) + 1} of {len(posts)}')
            html = self.get_html(f'https://www.instagram.com{post}')
            content = {l.group() for l in re.finditer(r'https://scontent[^"\n \']+1080x1080[^"\n \']+', html)}
            for link in content:
                links.add(link.replace(r'\u0026', '&'))
            sleep(self.tickrate)
        # print(f'[{self.__str__()}] <parse complete> {len(links)} links found')
        return links

    def down_media(self, media):
        '''
        retrieves media from web
        '''
        assert media
        for link in media:
            # print(f'[{self.__str__()}] <downloading> link {media.index(link) + 1} of {len(media)}')
            self.loot(link, self.sub_dir, f'{self.username}_{self.extract_filename(link)}.{self.filetype(link)}')
            sleep(self.tickrate)
        self.cleanup(self.sub_dir)
        self.move_vid(self.sub_dir)
        # print(f'[{self.__str__()}] <parse complete> {len(media)} links downloaded')

    def run(self):
        posts = self.find_posts()
        media = self.find_media(posts)
        self.down_media(media)
