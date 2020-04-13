import os
import re
import json

from time import sleep
from hashlib import md5
from urllib.parse import quote
from goblins.meta import MetaGoblin

# TODO:
#   - add support for stories
#   - add support for specifying # of posts to retrieve

class InstagramGoblin(MetaGoblin):

    def __init__(self, args):
        super().__init__(args)
        self.username = self.extract_username(self.args['targets'][self.__repr__()][0])
        self.insta_dir = os.path.join(self.path_main, self.username)
        self.url_pat = r'https?://scontent[^"\n \']+_n\.[^"\n \']+'
        self.headers = {
            'User-Agent': 'Firefox/72',
            'Accept-Encoding': 'gzip',
            'Cookie': 'ig_pr=1'
            }
        self.make_dirs(self.insta_dir)

    def __str__(self):
        return 'instagram goblin'

    def __repr__(self):
        return 'instagram'

    def extract_username(self, url):
        return re.search(r'(/?[^/]+/?)$', url).group().strip('/')

    def move_vid(self, path):
        '''move videos into seperate directory'''
        vid_path = os.path.join(path, 'vid')
        self.make_dirs(vid_path)
        for file in os.listdir(path):
            if '.mp4' in file:
                os.rename(os.path.join(path, file), os.path.join(vid_path, file))

    def hash(self, string):
        return md5(string.encode()).hexdigest()

    def find_posts(self):
        '''parse instagram page for posts
        code inspired by:
            - https://github.com/ytdl-org/youtube-dl
            - https://github.com/rarcega/instagram-scraper
            - various stack overflow posts
        '''
        # NOTE: both 472f257a40c653c64c666ce877d59d2b and 42323d64886122307be10013ad2dcc44 work for query_hash
        posts = []
        initial_response = json.loads(re.search(r'sharedData\s*=\s*({.+?})\s*;\s*[<\n]', self.get_html(f'https://www.instagram.com/{self.username}/')).group().lstrip('sharedData = ').rstrip(';<'))
        user_id = initial_response['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        csrf_token = initial_response['config']['csrf_token']
        rhx_gis = initial_response.get('rhx_gis', '3c7ca9dcefcf966d11dacf1f151335e8')
        cursor = ''
        if not self.args['silent']:
            print(f'[{self.__str__()}] <collecting posts>')
        while True:
            variables = json.dumps(
                {
                    'id': user_id,
                    'first': 100,
                    'after': cursor
                }
            )
            self.headers.update(
                {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-Instagram-GIS': self.hash(f'{rhx_gis}:{csrf_token}:{self.headers["User-Agent"]}:{variables}')
                }
            )
            media_response = self.get_html('https://www.instagram.com/graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables={}'.format(quote(variables, safe='"')))
            for post in {re.sub('"shortcode":', '', n.group()).strip('"') for n in re.finditer(r'"shortcode":"[^"]+"', media_response)}:
                posts.append(post)
            cursor = json.loads(media_response)['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            if not cursor:
                break
            sleep(self.args['delay'])
        return posts

    def find_media(self, posts):
        '''parses each post for media'''
        for post in posts:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <parsing post> /p/{post}/')
            content = self.extract_urls(self.url_pat, f'https://www.instagram.com/p/{post}/')
            for url in content:
                if re.search(r'(?:/[a-z]\d{3}x\d{3}/|ig_cache_key|c\d\.\d+\.\d+)', url):
                    continue
                self.collect(url.replace(r'\u0026', '&'), f'{self.username}_{self.extract_filename(url)}')
            sleep(self.args['delay'])
        print(f'[{self.__str__()}] <parsing complete>')

    def run(self):
        posts = self.find_posts()
        self.find_media(posts)
        self.loot(save_loc=self.insta_dir)
        self.move_vid(self.insta_dir)
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.insta_dir)
