import re
import os
from time import sleep
from handlers.meta_goblin import MetaGoblin


# alternate scaled: '?wid=2239&hei=2857&size=2239,2857&qlt=100'


class ASOSGoblin(MetaGoblin):
    '''
    accepts:
        - image
    '''

    def __init__(self, args):
        super().__init__(args)
        self.path_dl = os.path.join(self.path_main, 'fullsize')
        self.path_scanned = os.path.join(self.path_main, 'scanned')
        self.path_backup = os.path.join(self.path_main, 'backup')
        self.path_external = os.path.join(os.getcwd(), 'asos')
        self.query = '?scl=1&qlt=100'

    def __str__(self):
        return 'asos goblin'

    def remove_file(self, path, file):
        os.remove(os.path.join(path, file))

    def move_file(self, from_path, to_path, file):
        if os.path.exists(os.path.join(to_path, file)):
            self.remove_file(file, from_path)
        else:
            os.rename(os.path.join(from_path, file), os.path.join(to_path, file))

    def extract_color(self, file):
        '''
        extract color from filename
        '''
        # NOTE: returning none is not ideal, or at least not handled properly, writes
        # none to text file.
        color = re.search(r'\d+\-\d\-\w+', file)
        if color:
            return re.sub(r'\d+-\d-', '', color.group())

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

    def grab(self):
        '''
        grab a single url in high res
        '''
        color = self.extract_color(self.args['url'])
        id = self.extract_id(self.args['url'])
        if color:
            self.collect(self.form_url(f'{id}-1-{color}', True))
        for n in range(2, 5):
            self.collect(self.form_url(f'{id}-{n}', True))

    def generate_links(self, id, dir):
        '''
        generate a group of links for scanning
        '''
        id = int(id)
        if dir == '+':
            for n in range(id, id + 100):
                self.collect(self.form_url(n))
        else:
            for n in range(id - 1, id - 100, -1):
                self.collect(self.form_url(n))


    def upgrade(self):
        '''
        download hi-res version of downloaded images
        '''
        print(f'[{self.__str__()}] <upgrading>')
        for file in os.listdir(self.path_scanned):
            id = self.extract_id(file)
            if os.path.exists(os.path.join(self.path_dl, f'{id}-2.jpeg')):
                print(f'[{self.__str__()}] <file exists> {id}')
                self.move_file(self.path_scanned, self.path_backup, file)
                continue
            colors = self.read_file(os.path.join(self.path_main, 'colors.txt'), True)
            for color in colors:
                self.collect(self.form_url(f'{id}-1-{color}', True))
            for n in range(2, 5):
                self.collect(self.form_url(f'{id}-{n}', True))
            self.move_file(self.path_scanned, self.path_backup, file)

    def scan(self):
        '''
        find other images using supplied images or urls
        '''
        self.toggle_collecton_type()
        colors = set()
        if self.args['url']:
            files = [self.args['url']]
        else:
            if os.path.exists(self.path_external):
                for file in os.listdir(self.path_external):
                    self.move_file(self.path_external, self.path_main, file)
                os.rmdir(self.path_external)
            files = os.listdir(self.path_main)
        for file in files:
            if not re.search('.jpe?g', file):
                continue
            id = self.extract_id(file)
            colors.add(self.extract_color(file))
            if os.path.exists(os.path.join(self.path_scanned, f'{id}-2.jpeg')):
                print(f'[{self.__str__()}] <file exists> {id}')
                self.move_file(self.path_main, self.path_backup, file)
                continue
            print(f'[{self.__str__()}] <scanning> {id}')
            self.generate_links(id, '+')
            self.loot(save_loc=self.path_scanned, timeout=15)
            self.new_collection()
            self.generate_links(id, '-')
            self.loot(save_loc=self.path_scanned, timeout=15)
            self.move_file(self.path_main, self.path_backup, file)
        print(f'[{self.__str__()}] <exporting colors>')
        self.write_file(colors, os.path.join(self.path_main, 'colors.txt'), iter=True)
        print(f'[{self.__str__()}] <scanning complete>')

    def run(self):
        # TODO: expand
        if self.args['mode'] == 'upgrade':
            self.make_dirs(self.path_dl, self.path_scanned, self.path_backup)
            self.upgrade()
            self.loot(save_loc=self.path_dl)
        elif self.args['mode'] == 'scan':
            self.make_dirs(self.path_dl, self.path_scanned, self.path_backup)
            self.scan()
        else:
            self.grab()
            self.loot()
