import os
import re
import json

from time import sleep
from hashlib import md5
from getpass import getpass
from urllib.parse import quote, urljoin
from goblins.meta import MetaGoblin

class InstagramGoblin(MetaGoblin):
    '''code inspired by:
        - https://github.com/rarcega/instagram-scraper
        - https://github.com/ytdl-org/youtube-dl
        - various stack overflow posts
    '''

    NAME = 'instagram goblin'
    ID = 'instagram'
    BASE_URL = 'https://www.instagram.com/'
    # NOTE: both 472f257a40c653c64c666ce877d59d2b and 42323d64886122307be10013ad2dcc44 work for media query_hash
    MEDIA_URL = 'graphql/query/?query_hash=42323d64886122307be10013ad2dcc44&variables={}'
    STORIES_URL = BASE_URL + 'graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables={}'
    STORIES_USER_ID_URL = BASE_URL + 'graphql/query/?query_hash=c9100bf9110dd6361671f113dd02e7d6&variables={}'
    STORIES_REEL_ID_URL = BASE_URL + 'graphql/query/?query_hash=45246d3fe16ccc6577e0bd297a5db1ab&variables={}'

    def __init__(self, args):
        super().__init__(args)
        self.logged_in = False
        self.num_posts = self.args['posts'] if self.args['posts'] <= 100 else 100

    def setup(self, url):
        '''initialize user'''
        self.username = self.extract_username(url)
        self.insta_dir = os.path.join(self.path_main, self.username)
        self.vid_dir = os.path.join(self.insta_dir, 'vid')

        self.make_dirs(self.insta_dir, self.vid_dir)

    def extract_username(self, url):
        if '/p/' in url:
            return re.search(r'(?<="alternateName":"@)[^"]+', self.get(url).content).group()
        else:
            return re.search(r'(/?[^/]+/?)$', url).group().strip('/')

    def move_vid(self):
        '''move videos into seperate directory'''
        for file in os.listdir(self.insta_dir):
            if '.mp4' in file:
                os.rename(os.path.join(self.insta_dir, file), os.path.join(self.vid_dir, file))

    def extract_csrf_token(self, response):
        if 'csrftoken' in response.info.as_string():
            return re.search(r'(?<=csrftoken=)[^;]+', response.info.as_string()).group()
        else:
            data = json.loads(re.search(r'(?<=sharedData\s=\s){[^;]+',
                                        response.content).group())
            return data['config']['csrf_token']

    def hash(self, string):
        return md5(string.encode()).hexdigest()

    def authenticate(self, login):
        '''login to instagram or authenticate as guest'''
        response = self.get(self.BASE_URL)
        self.csrf_token = self.extract_csrf_token(response)
        self.headers.update({'X-CSRFToken': self.csrf_token})

        if login:
            while True:
                username = input(f'[{self.NAME}] username: ')
                password = getpass(f'[{self.NAME}] password: ')
                response = self.post(urljoin(self.BASE_URL, 'accounts/login/ajax/'),
                                     data={'username': username, 'password': password})
                del username, password
                answer = json.loads(response.content)

                if answer.get('authenticated') and response.code == 200:
                    self.extend_cookie('Cookie', re.search(r'sessionid=[^\n]+', response.info.as_string()).group())
                    self.csrf_token = self.extract_csrf_token(response)
                    self.headers.update({'X-CSRFToken': self.csrf_token})
                    self.logged_in = True
                    self.logger.log(0, self.NAME, 'logged in')
                elif 'checkpoint_url' in answer:
                    self.logger.log(0, self.NAME, 'WARNING', 'account verification required')
                    self.verify_account(answer.get('checkpoint_url'))
                else:
                    self.logger.log(0, self.NAME, 'ERROR', 'login failed')
                    retry = input(f'[{self.NAME}] retry? (y/n): ')
                    if retry == 'y':
                        continue
                    self.logger.log(0, self.NAME, 'continuing as guest')
                break

    def logout(self):
        response = self.post(urljoin(self.BASE_URL, 'accounts/logout/'),
                             data={'csrfmiddlewaretoken': self.csrf_token})

        if response.code == 200:
            self.logger.log(0, self.NAME, 'logged out')
        else:
            self.logger.log(0, self.NAME, 'ERROR', 'logout failed')

    def verify_account(self, checkpoint_url):
        '''complete security challenge to verify account'''
        # WARNING: untested
        # QUESTION: are all these header updates necessary? test without. and
        # should they be assigned to self.csrf_token?
        verify_url = urljoin(self.BASE_URL, checkpoint_url)
        response = self.get(verify_url)

        self.headers.update(
            {
                'X-CSRFToken': self.extract_csrf_token(response),
                'X-Instagram-AJAX': '1',
                'Referer': verify_url
            }
        )

        mode = input(f'[{self.NAME}] receive code via (0 - sms, 1 - email): ')
        challenge = self.post(verify_url, data= {'choice': mode})
        self.headers.update({'X-CSRFToken': self.extract_csrf_token(challenge)})

        while True:
            code = int(input(f'[{self.NAME}] enter security code: '))
            response = self.post(verify_url, data={'security_code': code})
            self.headers.update({'X-CSRFToken': self.extract_csrf_token(response)})
            answer = json.loads(response.content)

            if answer.get('status') == 'ok':
                self.logged_in = True
                self.logger.log(0, self.NAME, 'logged in')
            else:
                self.logger.log(0, self.NAME, 'ERROR', 'security challenge failed')
                retry = input(f'[{self.NAME}] retry? (y/n): ')
                if retry == 'y':
                    continue
                else:
                    self.logger.log(0, self.NAME, 'continuing as guest')
            break

    def get_initial_data(self):
        '''make initial request to recieve necessary variables'''
        self.extend_cookie('Cookie', 'ig_pr=1')
        response = json.loads(re.search(r'(?<=sharedData\s=\s){.+?}(?=;)',
                                        self.get(urljoin(self.BASE_URL, self.username)).content).group())

        self.user_id = response['entry_data']['ProfilePage'][0]['graphql']['user']['id']
        self.rhx_gis = response.get('rhx_gis', '3c7ca9dcefcf966d11dacf1f151335e8')

    def get_posts(self):
        '''parse instagram page for posts'''
        posts = []
        cursor = ''
        POST_PAT = re.compile(r'(?<="shortcode":")[^"]+')

        self.logger.log(1, self.NAME, 'collecting posts')

        while True:
            variables = json.dumps(
                {
                    'id': self.user_id,
                    'first': self.num_posts,
                    'after': cursor
                }
            )
            self.headers.update(
                {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-Instagram-GIS': self.hash(f'{self.rhx_gis}:{self.csrf_token}:{self.headers["User-Agent"]}:{variables}')
                }
            )

            response = self.get(self.BASE_URL + self.MEDIA_URL.format(quote(variables, safe='"')))
            posts.extend([post.group() for post in re.finditer(POST_PAT, response.content)])
            cursor = json.loads(response.content)['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']

            if not cursor or self.num_posts < 100:
                # end of profile or user specified finite number of posts.
                break

            sleep(self.args['delay'])

        return posts

    def get_media(self, posts):
        '''parses each post for media'''
        post_num = 1
        MEDIA_PAT = re.compile(r'(?<="display_url":")[^"]+|(?<="video_url":")[^"]+')

        for post in posts:
            self.logger.progress(self.NAME, 'parsing posts', post_num, len(posts))
            self.logger.log(2, self.NAME, 'parsing post', f'/p/{post}')

            for url in self.parser.extract_by_regex(self.get(urljoin(self.BASE_URL, f'p/{post}/?__a=1')).content, MEDIA_PAT):
                self.collect(url, f'{self.username}_{self.parser.extract_filename(url)}')

            post_num += 1
            sleep(self.args['delay'])

        self.logger.log(1, self.NAME, 'parsing complete', clear=True)

    def get_stories(self, url):
        response = json.loads(self.get(url).content)

        for reel_media in response['data']['reels_media']:
            for item in reel_media['items']:
                url = item['display_url']
                self.collect(url, f'{self.username}_{self.parser.extract_filename(url)}')

                if 'video_resources' in item:
                    url = item['video_resources'][-1]['src']
                    self.collect(url, f'{self.username}_{self.parser.extract_filename(url)}')

    def get_main_stories(self):
        self.get_stories(self.STORIES_URL.format(quote('{{"reel_ids":["{}"],"tag_names":[],' \
        '"location_ids":[],"highlight_reel_ids":[],"precomposed_overlay":false}}'.format(self.user_id), safe='"')))

    def get_highlight_stories(self):
        response = json.loads(self.get(self.STORIES_USER_ID_URL.format(quote('{{"user_id":"{}",' \
        '"include_chaining":false,"include_reel":false,"include_suggested_users":false,' \
        '"include_logged_out_extras":false,"include_highlight_reels":true,' \
        '"include_related_profiles":false}}'.format(self.user_id), safe='"'))).content)

        higlight_stories_ids = [item['node']['id'] for item in response['data']['user']['edge_highlight_reels']['edges']]
        ids_chunks = [higlight_stories_ids[i:i + 3] for i in range(0, len(higlight_stories_ids), 3)]

        for ids_chunk in ids_chunks:
            self.get_stories(self.STORIES_REEL_ID_URL.format(quote('{{"reel_ids":[],' \
            '"tag_names":[],"location_ids":[],"highlight_reel_ids":["{}"],' \
            '"precomposed_overlay":false}}'.format('","'.join(str(x) for x in ids_chunk)), safe='"')))

    def run(self):
        self.authenticate(self.args['login'])

        for target in self.args['targets'][self.ID]:
            self.new_collection()
            self.setup(target)

            if '/p/' in target:
                self.get_media([re.search(r'(?<=/p/)[^/]+', target).group()])
            else:
                if self.args['mode'] == 'latest' or self.args['mode'] == 'recent':
                    self.num_posts = 6
                self.get_initial_data()

                if self.logged_in:
                    self.logger.log(1, self.NAME, 'collecting stories')
                    self.get_main_stories()
                    if self.args['mode'] != 'latest' and self.args['mode'] != 'recent':
                        self.get_highlight_stories()

                posts = self.get_posts()
                self.get_media(posts)

            self.loot(save_loc=self.insta_dir)
            if not self.args['nodl']:
                self.move_vid()
        if self.logged_in:
            self.logout()
