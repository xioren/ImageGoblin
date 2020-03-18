import re
import os
from time import sleep
from handlers.meta_goblin import MetaGoblin


class LemanagementGoblin(MetaGoblin):

    '''
    mode options:
        - name
        - update
    format option:
        - country (find)
        - month year (update)
    link types:
        - image

    # NOTE: https://lemanagement.dk/wp-content/uploads/import/
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        self.format = format
        print(f'[{self.__str__()}] <running>')

    def __str__(self):
        return 'lemanagement goblin'

    def find(self, name, ref_year=2000, ref_month=1):
        complete = []
        path = '/media/veracrypt1/M/misc/brands/lemanagement/indexes/'
        for file in os.listdir(path):
            if file == 'import.html':
                continue
            found = set()
            dir_year, dir = file.rstrip('.html').split('_')
            with open(f'{path}{file}', 'r') as html:
                matches = re.finditer(r'href="{}.+align.+/td'.format(name.replace('_', '-')), html.read())
            for match in matches:
                match = match.group()
                image = re.search(r'[\w\-]+(\d+x\d+)*\.(jpe*g|png|tiff*|gif|mp4|mov)', match, IGNORECASE)
                year, month, _ = re.search(r'\d{4}\-\d{2}\-\d{2}', match).group().split('-')
                if int(year) >= ref_year and int(month.lstrip('0')) >= ref_month:
                    try:
                        found.add(re.sub(r'\-\d+x\d+', '', image.group()))
                    except Exception:
                        pass
            for f in found:
                if re.search(r'scaled|e\d+', f):
                    pass
                else:
                    complete.append(f'https://lemanagement.dk/wp-content/uploads/{dir_year}/{dir}/{f}')
        return complete


    def update(self, month, year):
        html = self.loot(f'https://lemanagement.dk/wp-content/uploads/{year}/{month}/',
                         wait=20, mode='w', save_loc='/media/veracrypt1/M/misc/brands/leman/indexes/',
                         filename=f'{year}_{month}.html')

    def run(self, country='Denmark'):
        # TODO: what trigger this module? name, url? fix this. consider kwargs also.
        if self.mode == 'update':
            month, year = self.format
            sef.update(month, year)
        else:
            found = self.find(name)
            if self.format:
                country = self.format
            # TODO: add name alt here
            for link in found:
                if self.nodl:
                    print(link)
                else:
                    self.loot(link, '/media/veracrypt1/M/{}/{}/'.format(country, filename=name.replace('-', '_')))
                    sleep(self.tickrate)
