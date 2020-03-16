from time import sleep
from goblin import MetaGoblin
from parsing import *


class GrabberGoblin(MetaGoblin):

    def __init__(self, url, save_loc, format, overwrite, nodl, print=False, export=False):
        super().__init__(url=url, save_loc=save_loc, overwrite=overwrite)
        self.format = format
        self.export = export
        self.nodl = nodl
        if not url:
            raise ValueError('no url supplied')

    def link_grab(self):
        '''
        parse html for media links
        '''
        print(f'[parsing] {self.url}')
        html = self.get_html(self.url)
        if html:
            self.links = link_finder(url=self.url, data=html)
            print(f'[parse complete] {len(self.links)} links found')
            if self.nodl == 1:
                for link in self.links:
                    print(link)
            elif self.nodl == 2:
                self.write_iter(self.links, self.txt_loc)
                print(f'[goblin] links written to file')
        else:
            print('[ERROR] no html recieved')
            return None

    def link_dl(self):
        '''
        download media
        '''
        downloaded = []
        self.create_folders(self.dl_folder)
        for link in self.links:
            print(f'[downloading] link {self.links.index(link) + 1} of {len(self.links)}')
            url, filename = dl_prep(url=link)
            if self.format:
                url, filename = custom_format(url=url, name=filename, format=self.format)
            filepath = f'{self.dl_folder}{filename}'
            if not self.overwrite and self.exists(filepath):
                continue
            if url not in downloaded:
                downloaded.append(url)
                self.retrieve(url=url, path=filepath)
            sleep(1)
        self.cleanup(self.dl_folder)
