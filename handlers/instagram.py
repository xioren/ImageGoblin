import os
from time import sleep
from handlers.meta_goblin import MetaGoblin
from parsing import *


class InstagramGoblin(MetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.username = insta_username(self.url)
        self.html_txt = os.path.join(os.getcwd(), 'html.txt')
        self.sub_dir = os.path.join(self.path_main, self.username)
        self.make_dirs(self.sub_dir)
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'instagram goblin'

    def find_posts(self):
        '''
        parse html for instagram posts
        '''
        print(f'[{self.__str__()}] <parsing> {self.username}')
        html = self.read_file(self.html_txt)
        assert html
        return parse_posts(html)

    def find_media(self, posts):
        '''
        opens links from iterable and parses for media
        '''
        links = []
        for post in posts:
            print(f'[{self.__str__()}] <parsing> post {posts.index(post) + 1} of {len(posts)}')
            html = self.get_html(post)
            content = parse_content(html)
            for link in content:
                links.append(link)
            sleep(self.tickrate)
        print(f'[{self.__str__()}] <parse complete> {len(links)} links found')
        return links

    def down_media(self, media):
        '''
        retrieves media from web
        '''
        assert media
        for link in media:
            print(f'[{self.__str__()}] <downloading> link {media.index(link) + 1} of {len(media)}')
            filename = extract_filename(link)
            filepath = os.path.join(self.sub_dir, f'{self.username}_{filename}.{filetype(link)}')
            self.loot(link, filepath)
            sleep(self.tickrate)
        self.cleanup(self.sub_dir)
        self.move_vid(self.sub_dir)
        print(f'[{self.__str__()}] <parse complete> {len(media)} links downloaded')

    def run(self):
        posts = self.find_posts()
        media = self.find_media(posts)
        self.down_media(media)
