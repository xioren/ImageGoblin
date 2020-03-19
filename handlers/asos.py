import re
import os
from time import sleep
from handlers.meta_goblin import MetaGoblin
from parsing import *

# TODO: add single use

class ASOSGoblin(MetaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        self.path_dl = os.path.join(self.path_main, 'fullsize')
        self.path_scanned = os.path.join(self.path_main, 'scanned')
        self.path_backup = os.path.join(self.path_main, 'backup')
        self.query = '?wid=2239&hei=2857&size=2239,2857'
        self.make_dirs(self.path_dl, self.path_scanned, self.path_backup)
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'asos goblin'

    def remove_file(self, path, file):
        os.remove(os.path.join(path, file))

    def move_file(self, from_path, to_path, file):
        if os.path.exists(os.path.join(to_path, file)):
            self.remove_file(file, from_path)
        else:
            os.rename(os.path.join(from_path, file), os.path.join(to_path, file))

    def get_color(self, file):
        '''
        extract color from filename
        '''
        # NOTE: returning none is not ideal, or at least not handled properly, writes
        # none to text file. also matches image number when no color present.
        color = re.search(r'\w+\.', file)
        if color:
            return color.group()[:-1]
        else:
            return None

    def form_url(self, id, large=False):
        '''
        generate a url from an image id
        '''
        id = str(id)
        if not re.search(r'\-[a-z0-9]+$', id):
            id += '-2'
        link = f'https://images.asos-media.com/products/asos/{id}'
        return link + self.query if large else link

    def extract_id(self, url):
        '''
        pull image id from url
        '''
        return re.search(r'\d+', url).group()

    def upgrade(self):
        '''
        download hi-res version of downloaded images
        '''
        for file in os.listdir(self.path_scanned):
            if '.jpeg' not in file:
                continue
            id = self.extract_id(file)
            if os.path.exists(os.path.join(self.path_dl, f'{id}-2.jpeg')):
                print(f'[{self.__str__()}] <file exists> {id}')
                self.move_file(self.path_scanned, self.path_backup, file)
                continue
            print(f'[{self.__str__()}] <upgrading> {id}')
            colors = self.read_file(os.path.join(self.path_main, 'colors.txt'), True)
            for color in colors:
                attempt = self.loot(self.form_url(f'{id}-1-{color}', True), self.path_dl)
                if attempt:
                    break
                sleep(self.tickrate)
            for n in range(2, 5):
                self.loot(self.form_url(f'{id}-{n}', True), self.path_dl)
                sleep(self.tickrate)
            self.move_file(self.path_scanned, self.path_backup, file)

    def scan(self, location='dir'):
        '''
        find other images using supplied images or urls
        '''
        colors = set()
        def step(id, increment):
            idle = 0
            while idle < 20:
                attempt = self.loot(self.form_url(id), self.path_scanned)
                if attempt:
                    idle = 0
                else:
                    idle += 1
                id += increment
                sleep(self.tickrate)
        if not self.url == 'asos':
            files = [self.url]
        else:
            if location == 'file':
                files = self.read_file(os.path.join(self.path_main, 'ids.txt'), True)
            else:
                files = os.listdir(self.path_main)
        for file in files:
            if '.jpeg' not in file:
                continue
            id = self.extract_id(file)
            colors.add(self.get_color(file))
            if os.path.exists(os.path.join(self.path_scanned, f'{id}-2.jpeg')):
                print(f'[{self.__str__()}] <file exists> {id}')
                self.move_file(self.path_main, self.path_backup, file)
                continue
            print(f'[{self.__str__()}] <scanning> {id}')
            step(int(id), 1)
            step(int(id) - 1, -1)
            self.move_file(self.path_main, self.path_backup, file)
        print(f'[{self.__str__()}] <exporting colors>')
        self.write_file(colors, os.path.join(self.path_main, 'colors.txt'), iter=True)
        print(f'[{self.__str__()}] <scanning complete>')

    def duplicate_check():
        '''
        check for and remove_file duplicates
        '''
        duplicates = 0
        ids = set()
        for path in sources['asos']:
            for file in os.listdir(path):
                if file == 'need_color':
                    continue
                ids.add(self.extract_id(file))
        for file in os.listdir(self.path_main):
            if file == 'backup' or file == 'fullsize' or file == 'scanned':
                continue
            if re.search(self.extract_id(file)) in ids:
                self.move_file(self.path_main, self.path_backup, file)
                duplicates += 1
        print(f'[{self.__str__()}] <{duplicates} duplicates removed>')

    def sort_colors(self):
        '''
        sort color text file
        '''
        path = '/media/veracrypt1/M/misc/brands/asos_colors.txt'
        path_temp = '/media/veracrypt1/M/misc/brands/asos_colors_temp.txt'
        colors = sorted(set(self.read_file(path, True)))
        self.write_file(colors, path_temp, iter=True)
        os.remove(path)
        os.rename(path_temp, path)

    def color_match(self, path):
        '''
        try to identify correct color for missing files
        '''
        files = set()
        print(f'[{self.__str__()}] <attempting to match correct color>')
        # QUESTION: does jpg or jpeg make a difference with the slicing? consider \d+ re.
        for file in os.listdir(path):
            if '-2' in file:
                files.add(file[:-7])
        colors = self.read_file(os.path.join(self.path_main, 'colors.txt'), True)
        for file in files:
            for color in colors:
                attempt = loot(f'{url}{item}-1-{color[:-1]}{query}')
                if attempt:
                    break
                sleep(self.tickrate)

    def run(self):
        # TODO: expand
        if self.mode == 'scan':
            self.scan()
        elif self.mode == 'upgrade':
            self.upgrade()
