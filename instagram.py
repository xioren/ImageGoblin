import os
from time import sleep
from goblin import MetaGoblin
from parsing import *


class InstaGoblin(MetaGoblin):

    def __init__(self, url, tickrate, verbose, nodl):
        super().__init__(url, tickrate, verbose, nodl)
        self.username = insta_username(self.url)
        self.html_txt = os.path.join(self.main_path.replace('web_goblin', ''), 'html.txt')
        self.sub_dir = os.path.join(self.main_path, self.username)
        self.create_folders(self.sub_dir)

    def find_posts(self):
        '''
        parse html for instagram posts
        '''
        print(f'[parsing] {self.url}')
        html = self.read_file(self.html_txt)
        assert html
        return parse_posts(html)

    def find_media(self, posts):
        '''
        opens links from iterable and parses for media
        '''
        links = []
        for post in posts:
            print(f'[parsing] post {posts.index(post) + 1} of {len(posts)}')
            html = self.get_html(post)
            content = parse_content(html)
            for link in content:
                links.append(link)
            sleep(self.tickrate)
        print(f'[parse complete] {len(links)} links found')
        return links

    def down_media(self, media):
        '''
        retrieves media from web
        '''
        for link in media:
            print(f'[downloading] link {media.index(link) + 1} of {len(media)}')
            filename = extract_filename(link)
            filepath = os.path.join(self.sub_dir, f'{self.username}_{filename}.{filetype(link)}')
            if os.path.exists(filepath):
                print(f'[file exists] {self.username}_{filename}')
                continue
            self.retrieve(link, filepath)
            sleep(self.tickrate)
        self.cleanup(self.sub_dir)
        self.move_vid(self.sub_dir)
        print(f'[parse complete] {len(media)} links found')
