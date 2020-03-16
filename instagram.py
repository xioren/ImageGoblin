from time import sleep
from goblin import MetaGoblin
from parsing import *


class InstaGoblin(MetaGoblin):

    def __init__(self, url, save_loc, overwrite):
        super().__init__(url=url, save_loc=save_loc, overwrite=overwrite)
        self.url = url
        self.username = instagram(self.url)
        self.html_txt = f'{self.save_loc}/html.txt'
        if self.username:
            self.sub_dir = f'{self.main_path}{self.username}/'
        else:
            self.sub_dir = f'{self.main_path}no_username_found/'
        self.create_folders(self.sub_dir)

    def find_posts(self):
        '''
        parse html for instagram posts
        '''
        print(f'[parsing] {self.url}')
        html = self.read_file(self.html_txt)
        self.posts = parse_html(html)

    def find_media(self):
        '''
        opens links from iterable and parses for media
        '''
        self.links = []
        for post in self.posts:
            print(f'[parsing] post {self.posts.index(post) + 1} of {len(self.posts)}')
            html = self.get_html(post)
            content = parse_content(html)
            for link in content:
                self.links.append(link)
            sleep(1)
        print(f'[parse complete] {len(self.links)} links found')

    def down_media(self):
        '''
        retrieves media from web
        '''
        for link in self.links:
            print(f'[downloading] link {self.links.index(link) + 1} of {len(self.links)}')
            filepath = f'{self.sub_dir}{self.username}_{insta_prep(link)}'
            if self.exists(filepath):
                continue
            self.retrieve(url=link, path=filepath)
            sleep(1)
        self.cleanup(self.sub_dir)
        self.move_vid(self.sub_dir)
        print(f'[parse complete] {len(self.links)} links found')
