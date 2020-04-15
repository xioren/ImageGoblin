import os
import re
import json

from time import sleep
from hashlib import md5
from urllib.parse import quote
from goblins.meta import MetaGoblin

# TODO:
#   - finish stories implementation
#   - add support for specifying # of posts to retrieve

class InstagramGoblin(MetaGoblin):
    '''code inspired by:
        - https://github.com/ytdl-org/youtube-dl
        - https://github.com/rarcega/instagram-scraper
        - various stack overflow posts
    '''

    def __init__(self, args):
        super().__init__(args)
        self.username = self.extract_username(self.args['targets'][self.__repr__()][0])
        self.insta_dir = os.path.join(self.path_main, self.username)
        self.url_pat = r'https?://scontent[^"\n \']+_n\.[^"\n \']+'
        self.headers = {
            'User-Agent': 'Firefox/75',
            'Accept-Encoding': 'gzip',
            'Cookie': 'ig_pr=1'
            }
        self.base_url = 'https://www.instagram.com/'
        # NOTE: both 472f257a40c653c64c666ce877d59d2b and 42323d64886122307be10013ad2dcc44 work for query_hash
        self.media_url = 'graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables={}'
        self.stories_url = self.base_url + 'graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables={}'
        self.stories_user_id_url = self.base_url + 'graphql/query/?query_hash=c9100bf9110dd6361671f113dd02e7d6&variables={}'
        self.stories_reel_id_url = self.base_url + 'graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables={}'
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

    def get_user_data(self):
        response = json.loads(re.search(r'sharedData\s*=\s*({.+?})\s*;\s*[<\n]', self.get_html(f'{self.base_url}{self.username}/')).group().lstrip('sharedData = ').rstrip(';<'))
        self.user_id = response['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        self.csrf_token = response['config']['csrf_token']
        self.rhx_gis = response.get('rhx_gis', '3c7ca9dcefcf966d11dacf1f151335e8')

    def find_posts(self):
        '''parse instagram page for posts'''
        posts = []
        cursor = ''
        if not self.args['silent']:
            print(f'[{self.__str__()}] <collecting posts>')
        while True:
            variables = json.dumps(
                {
                    'id': self.user_id,
                    'first': 100,
                    'after': cursor
                }
            )
            self.headers.update(
                {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-Instagram-GIS': self.hash(f'{self.rhx_gis}:{self.csrf_token}:{self.headers["User-Agent"]}:{variables}')
                }
            )
            response = self.get_html(self.base_url + self.media_url.format(quote(variables, safe='"')))
            for post in {re.sub('"shortcode":', '', n.group()).strip('"') for n in re.finditer(r'"shortcode":"[^"]+"', response)}:
                posts.append(post)
            cursor = json.loads(response)['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            if not cursor:
                break
            sleep(self.args['delay'])
        return posts

    def find_media(self, posts):
        '''parses each post for media'''
        for post in posts:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <parsing post> /p/{post}/')
            content = self.extract_urls(self.url_pat, f'{self.base_url}p/{post}/')
            for url in content:
                if re.search(r'(?:/[a-z]\d{3}x\d{3}/|c\d\.\d+\.\d+)', url):
                    continue
                self.collect(re.sub(r'\\?u?0026', '&', url), f'{self.username}_{self.extract_filename(url)}')
            sleep(self.args['delay'])
        print(f'[{self.__str__()}] <parsing complete>')

    # def find_stories(self, url):
    #     response = json.loads(self.get_html(url))
    #     items = []
    #     for reel_media in response['data']['reels_media']:
    #         items.extend([self.set_story_url(item) for item in reel_media['items']])
    #         for item in reel_media['items']:
    #             item['highlight'] = fetching_highlights_metadata
    #             self.stories.append(item)
    #     return items

    # def find_main_stories(self):
    #     return self.get_stories(self.stories_url.format(quote('{{"reel_ids":["{}"],"tag_names":[],"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false}}'.format(self.user_id), safe='"')))
    
    # def find_highlight_stories(self):
    #     response = json.loads(self.get_html('{{"user_id":"{}","include_chaining":false,"include_reel":false,"include_suggested_users":false,"include_logged_out_extras":false,"include_highlight_reels":true,"include_related_profiles":false}}'.format(user_id)))
    #     higlight_stories_ids = [item['node']['id'] for item in response['data']['user']['edge_highlight_reels']['edges']]
    #     ids_chunks = [higlight_stories_ids[i:i + 3] for i in range(0, len(higlight_stories_ids), 3)]
    #     stories = []
    #     for ids_chunk in ids_chunks:
    #         stories.extend(self.get_stories(self.stories_reel_id_url.format('{{"reel_ids":[],"tag_names":[],"location_ids":[],"highlight_reel_ids":["{}"],"precomposed_overlay":false}}'.format('%22%2C%22'.join(str(x) for x in ids_chunk)))))
    #     return stories

    def run(self):
        self.get_user_data()
        posts = self.find_posts()
        self.find_media(posts)
        self.loot(save_loc=self.insta_dir)
        self.move_vid(self.insta_dir)
        if not self.args['nodl'] and not self.args['noclean']:
            self.cleanup(self.insta_dir)
