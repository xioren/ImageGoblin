import os
import re
import json

from time import sleep
from hashlib import md5
from urllib.parse import quote
from goblins.meta import MetaGoblin

# TODO:
#   - finish stories implementation? needs login method if so.
#   - add support for specifying # of posts to retrieve
#   - add handling of single posts

class InstagramGoblin(MetaGoblin):
    '''code inspired by:
        - https://github.com/ytdl-org/youtube-dl
        - https://github.com/rarcega/instagram-scraper
        - various stack overflow posts
    '''

    def __init__(self, args):
        super().__init__(args)
        self.base_url = 'https://www.instagram.com/'
        # NOTE: both 472f257a40c653c64c666ce877d59d2b and 42323d64886122307be10013ad2dcc44 work for query_hash
        self.media_url = 'graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables={}'
        # self.stories_url = self.base_url + 'graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables={}'
        # self.stories_user_id_url = self.base_url + 'graphql/query/?query_hash=c9100bf9110dd6361671f113dd02e7d6&variables={}'
        # self.stories_reel_id_url = self.base_url + 'graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables={}'

    def __str__(self):
        return 'instagram goblin'

    def __repr__(self):
        return 'instagram'

    def setup(self, url):
        '''initialize values per user (for handling multiple users)'''
        self.username = self.extract_username(url)
        self.insta_dir = os.path.join(self.path_main, self.username)
        self.vid_dir = os.path.join(self.insta_dir, 'vid')
        if not self.args['nodl']:
            self.make_dirs(self.insta_dir, self.vid_dir)

    def extract_username(self, url):
        if '/p/' in url:
            return re.search(r'(?<="alternateName":"@)[^"]+', self.get_webpage(url)).group()
        else:
            return re.search(r'(/?[^/]+/?)$', url).group().strip('/')

    def move_vid(self):
        '''move videos into seperate directory'''
        for file in os.listdir(self.insta_dir):
            if '.mp4' in file:
                os.rename(os.path.join(self.insta_dir, file), os.path.join(self.vid_dir, file))

    def hash(self, string):
        return md5(string.encode()).hexdigest()

    def get_user_data(self):
        '''make initial request to recieve necessary variables'''
        self.headers.update({'Cookie': 'ig_pr=1'})
        response = json.loads(re.search(r'(?<=sharedData\s=\s){[^;]+', self.get_webpage(f'{self.base_url}{self.username}')).group())
        self.user_id = response['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        self.csrf_token = response['config']['csrf_token']
        self.rhx_gis = response.get('rhx_gis', '3c7ca9dcefcf966d11dacf1f151335e8')

    def get_posts(self):
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
            response = self.get_webpage(self.base_url + self.media_url.format(quote(variables, safe='"')))
            posts.extend([n.group() for n in re.finditer(r'(?<="shortcode":")[^"]+', response)])
            cursor = json.loads(response)['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            if not cursor:
                break
            sleep(self.args['delay'])
        return posts

    def get_media(self, posts):
        '''parses each post for media'''
        for post in posts:
            if not self.args['silent']:
                print(f'[{self.__str__()}] <parsing post> /p/{post}')
            content = self.extract_urls(r'(?<="display_url":")[^"]+|(?<="video_url":")[^"]+', f'{self.base_url}p/{post}/?__a=1')
            for url in content:
                self.collect(re.sub(r'\\?u?0026', '&', url), f'{self.username}_{self.extract_filename(url)}')
            sleep(self.args['delay'])
        print(f'[{self.__str__()}] <parsing complete>')

    # def get_stories(self, url):
    #     response = json.loads(self.get_webpage(url))
    #     items = []
    #     for reel_media in response['data']['reels_media']:
    #         items.extend([item for item in reel_media['items']])
    #     return items

    # def get_main_stories(self):
    #     return self.get_stories(self.stories_url.format(quote('{{"reel_ids":["{}"],"tag_names":[],"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false}}'.format(self.user_id), safe='"')))

    # def get_highlight_stories(self):
    #     stories = []
    #     response = json.loads(self.get_webpage('{{"user_id":"{}","include_chaining":false,"include_reel":false,"include_suggested_users":false,"include_logged_out_extras":false,"include_highlight_reels":true,"include_related_profiles":false}}'.format(user_id)))
    #     higlight_stories_ids = [item['node']['id'] for item in response['data']['user']['edge_highlight_reels']['edges']]
    #     ids_chunks = [higlight_stories_ids[i:i + 3] for i in range(0, len(higlight_stories_ids), 3)]
    #     for ids_chunk in ids_chunks:
    #         stories.extend(self.get_stories(self.stories_reel_id_url.format('{{"reel_ids":[],"tag_names":[],"location_ids":[],"highlight_reel_ids":["{}"],"precomposed_overlay":false}}'.format('%22%2C%22'.join(str(x) for x in ids_chunk)))))
    #     return stories

    def run(self):
        for target in self.args['targets'][self.__repr__()]:
            self.new_collection()
            self.setup(target)
            if '/p/' in target:
                self.get_media([re.search(r'(?<=/p/)[^/]+', target).group()])
            else:
                self.get_user_data()
                posts = self.get_posts()
                self.get_media(posts)
            self.loot(save_loc=self.insta_dir)
            if not self.args['nodl']:
                self.move_vid()
