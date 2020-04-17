import os
import re
import json

from time import sleep
from hashlib import md5
from getpass import getpass
from urllib.parse import quote
from goblins.meta import MetaGoblin

# TODO:
#   - finish support for specifying # of posts to retrieve

class InstagramGoblin(MetaGoblin):
    '''code inspired by:
        - https://github.com/rarcega/instagram-scraper
        - https://github.com/ytdl-org/youtube-dl
        - various stack overflow posts
    '''

    def __init__(self, args):
        super().__init__(args)
        # self.posts = self.args['posts']
        self.logged_in = False
        self.base_url = 'https://www.instagram.com/'
        # NOTE: both 472f257a40c653c64c666ce877d59d2b and 42323d64886122307be10013ad2dcc44 work for query_hash
        self.media_url = 'graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables={}'
        self.stories_url = self.base_url + 'graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables={}'
        self.stories_user_id_url = self.base_url + 'graphql/query/?query_hash=c9100bf9110dd6361671f113dd02e7d6&variables={}'
        self.stories_reel_id_url = self.base_url + 'graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables={}'

    def __str__(self):
        return 'instagram goblin'

    def __repr__(self):
        return 'instagram'

    def setup(self, url):
        '''initialize values per user (for handling multiple users)'''
        self.username = self.extract_username(url)
        self.insta_dir = os.path.join(self.path_main, self.username)
        self.vid_dir = os.path.join(self.insta_dir, 'vid')
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

    def authenticate(self):
        '''login to instagram or authenticate as guest'''
        response = self.get(self.base_url)
        self.csrf_token = re.search(r'(?<=csrftoken=)[^;]+', response.info).group()
        self.headers.update({'X-CSRFToken': self.csrf_token})
        if self.args['login']:
            # username = input(f'[{self.__str__()}] username: ')
            # password = getpass(f'[{self.__str__()}] password: ')
            username = 'danya__flor'
            password = 'danystar05'
            response = self.post(self.base_url + 'accounts/login/ajax/',  data={'username': username, 'password': password})
            del username
            del password
            login_text = json.loads(response.content)
            if login_text.get('authenticated') and response.code == 200:
                self.extend_cookie('Cookie', re.search(r'sessionid=[^\n]+', response.info).group())
                self.csrf_token = re.search(r'(?<=csrftoken=)[^;]+', response.info).group()
                self.headers.update({'X-CSRFToken': self.csrf_token})
                self.logged_in = True
                self.logger.log(0, self.__str__(), 'logged in')
            elif 'checkpoint_url' in login_text:
                self.logger.log(0, self.__str__(), 'WARNING', 'account verification required')
                self.verify_account(login_text.get('checkpoint_url'))
            else:
                self.logger.log(0, self.__str__(), 'ERROR', 'login failed')

    def logout(self):
        response = self.post(self.base_url + 'accounts/logout/', {'csrfmiddlewaretoken': self.csrf_token})
        logout_text = json.loads(response.content)
        if logout_text.get('status') == 'ok' and response.code == 200:
            self.logger.log(0, self.__str__(), 'logged out')
        else:
            self.logger.log(0, self.__str__(), 'ERROR', 'logout failed')

    def verify_account(self, checkpoint_url):
        '''complete challenge response to verify account'''
        # QUESTION: are all these header updates necessary? test without.
        response = self.get(self.base_url + checkpoint_url)
        self.headers.update({'X-CSRFToken': re.search(r'(?<=csrftoken=)[^;]+', response.info).group(), 'X-Instagram-AJAX': '1'})
        self.headers.update({'Referer': self.base_url[:-1] + checkpoint_url})
        mode = input(f'[{self.__str__()}] receive code via (0 - sms, 1 - email): ')
        challenge_data = {'choice': mode}
        challenge = self.post(self.base_url[:-1] + checkpoint_url, data=challenge_data)
        self.headers.update({'X-CSRFToken': re.search(r'(?<=csrftoken=)[^;]+', challenge.info).group(), 'X-Instagram-AJAX': '1'})
        code = int(input(f'[{self.__str__()}] enter security code: '))
        code_data = {'security_code': code}
        code = self.post(self.base_url[:-1] + checkpoint_url, data=code_data)
        self.headers.update({'X-CSRFToken': re.search(r'(?<=csrftoken=)[^;]+', code.info).group()})
        code_text = json.loads(code.content)
        if code_text.get('status') == 'ok':
            self.logged_in = True
            self.logger.log(0, self.__str__(), 'logged in')
        else:
            self.logger.log(0, self.__str__(), 'ERROR', 'challenge response failed')

    def get_initial_data(self):
        '''make initial request to recieve necessary variables'''
        self.extend_cookie('Cookie', 'ig_pr=1')
        response = json.loads(re.search(r'(?<=sharedData\s=\s){[^;]+', self.get(f'{self.base_url}{self.username}').content).group())
        self.user_id = response['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        # self.csrf_token = response['config']['csrf_token']
        self.rhx_gis = response.get('rhx_gis', '3c7ca9dcefcf966d11dacf1f151335e8')

    def get_posts(self):
        '''parse instagram page for posts'''
        posts = []
        cursor = ''
        self.logger.log(1, self.__str__(), 'collecting posts')
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
            response = self.get(self.base_url + self.media_url.format(quote(variables, safe='"')))
            posts.extend([n.group() for n in re.finditer(r'(?<="shortcode":")[^"]+', response.content)])
            cursor = json.loads(response.content)['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
            if not cursor:
                break
            sleep(self.args['delay'])
        return posts

    def get_media(self, posts):
        '''parses each post for media'''
        for post in posts:
            self.logger.log(1, self.__str__(), 'parsing post', f'/p/{post}')
            content = self.extract_urls(r'(?<="display_url":")[^"]+|(?<="video_url":")[^"]+', f'{self.base_url}p/{post}/?__a=1')
            for url in content:
                self.collect(re.sub(r'\\?u?0026', '&', url), f'{self.username}_{self.extract_filename(url)}')
            sleep(self.args['delay'])
        print(f'[{self.__str__()}] <parsing complete>')

    def get_stories(self, url):
        response = json.loads(self.get(url).content)
        for reel_media in response['data']['reels_media']:
            for item in reel_media['items']:
                if 'video_resources' in item:
                    url = item['video_resources'][-1]['src']
                    self.collect(url, f'{self.username}_{self.extract_filename(url)}')
                if 'display_resources' in item:
                    url = item['display_resources'][-1]['src']
                    self.collect(url, f'{self.username}_{self.extract_filename(url)}')

    def get_main_stories(self):
        self.get_stories(self.stories_url.format(quote('{{"reel_ids":["{}"],"tag_names":[],' \
        '"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false}}'.format(self.user_id), safe='"')))

    def get_highlight_stories(self):
        response = json.loads(self.get(self.stories_user_id_url.format(quote('{{"user_id":"{}",' \
        '"include_chaining":false,"include_reel":false,"include_suggested_users":false,' \
        '"include_logged_out_extras":false,"include_highlight_reels":true,' \
        '"include_related_profiles":false}}'.format(self.user_id), safe='"'))).content)
        higlight_stories_ids = [item['node']['id'] for item in response['data']['user']['edge_highlight_reels']['edges']]
        ids_chunks = [higlight_stories_ids[i:i + 3] for i in range(0, len(higlight_stories_ids), 3)]
        for ids_chunk in ids_chunks:
            self.get_stories(self.stories_reel_id_url.format(quote('{{"reel_ids":[],' \
            '"tag_names":[],"location_ids":[],"highlight_reel_ids":["{}"],' \
            '"precomposed_overlay":false}}'.format('","'.join(str(x) for x in ids_chunk)), safe='"')))


    def run(self):
        self.authenticate()
        for target in self.args['targets'][self.__repr__()]:
            self.new_collection()
            self.setup(target)
            if '/p/' in target:
                self.get_media([re.search(r'(?<=/p/)[^/]+', target).group()])
            else:
                self.get_initial_data()
                if self.logged_in:
                    self.logger.log(1, self.__str__(), 'collecting stories')
                    self.get_main_stories()
                    self.get_highlight_stories()
                posts = self.get_posts()
                self.get_media(posts)
            self.loot(save_loc=self.insta_dir)
            if not self.args['nodl']:
                self.move_vid()
        if self.logged_in:
            self.logout()
