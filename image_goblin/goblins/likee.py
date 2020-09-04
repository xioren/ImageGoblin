from meta import MetaGoblin


class LikeeGoblin(MetaGoblin):
    '''accepts:
        - image
        - webpage
    '''

    NAME = 'likee goblin'
    ID = 'likee'
    MEDIA_URL = 'https://likee.video/bg_ci_index.php/live/share/getUserPost?u={}&count={}&last_postid={}'

    def __init__(self, args):
        super().__init__(args)
        self.num_posts = self.args['posts'] if self.args['posts'] < 100 else 100

    def main(self):
        self.logger.log(1, self.NAME, 'collecting urls')
        urls = []

        for target in self.args['targets'][self.ID]:
            if '/s/' in target:
                response = self.get(target).content
                urls.append(self.parser.regex_search(r'(?<=video_url":")[^"]+', response))
                urls.append(self.parser.regex_search(r'(?<=thumbnailUrl":\[")[^"]+', response))
            else:
                last_postid = ''
                init_response = self.get(self.parser.dequery(target)).content
                uid = self.parser.regex_search(r'(?<=uid=)\d+', init_response)

                while True:
                    response = self.parser.load_json(self.get(self.MEDIA_URL.format(uid, self.num_posts, last_postid)).content)
                    if response['result'] == 200:
                        if not response['post_list']:
                            break
                        for post in response['post_list']:
                            urls.append(post['thumbnailUrl'])
                            urls.append(post['contentUrl'])
                        last_postid = response['post_list'][-1]['post_id']
                    else:
                        # OPTIMIZE: two breaks, should be combined.
                        break

                    if self.num_posts < 100:
                        # end of profile or user specified finite number of posts.
                        break

                    self.delay()

        for url in urls:
            self.collect(url)

        self.loot()
