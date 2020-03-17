import os
from time import sleep
from goblin import MetaGoblin
from parsing import *


class GrabberGoblin(MetaGoblin):

    def __init__(self, url, format, nodl, tickrate, verbose):
        super().__init__(url, tickrate, verbose, nodl)
        self.format = format

    def link_grab(self):
        '''
        parse html for media links
        '''
        print(f'[parsing] {self.url}')
        html = self.get_html(self.url)
        if html:
            links = link_finder(self.url, html)
            print(f'[parse complete] {len(links)} links found')
            if self.nodl == 1:
                for link in links:
                    print(link)
            elif self.nodl == 2:
                self.write_file(links, os.path.join(self.main_path.replace('web_goblin', ''), 'goblin_links.txt'), iter=True)
                print(f'[goblin] links written to file')
        else:
            print('[ERROR] no html recieved')
            return None
        return links

    def link_dl(self, links):
        '''
        retrieve media
        '''
        assert links
        downloaded = []
        for link in links:
            print(f'[downloading] link {links.index(link) + 1} of {len(links)}')
            if self.format:
                link = custom_format(link, self.format)
            filename = extract_filename(link)
            filepath = os.path.join(self.main_path, f'{filename}.{filetype(link)}')
            if os.path.exists(filepath):
                print(f'[file exists] {filename}')
                continue
            if link not in downloaded:
                downloaded.append(link)
                self.retrieve(link, filepath)
            sleep(self.tickrate)
        self.cleanup(self.main_path)
