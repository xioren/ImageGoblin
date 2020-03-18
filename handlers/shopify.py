import re
from time import sleep
from parsing import *
from handlers.meta_goblin import MetaGoblin


class ShopifyGoblin(MetaGoblin):

    '''
    mode options:
        - iter: for multiple links (using external links file)
    format option:
        - clean: decrop image
    url types:
        - webpage
    back end for:
        - fashion nova
        - five dancewear
    '''

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, tickrate, verbose, nodl)
        self.mode = mode
        self.format = format
        self.image_pat = r'//cdn.shopify.com/[^" \n]+\d+x[^" \n]+'

    # TODO: add shopify __str__ for non matched inputs?

    def clean(self, url):
        # NOTE: changed to 4 instead of +...check if always 4 with different urls
        return re.sub(r'_[a-z\d]+(\-[a-z\d]+){4}', '', url)

    def run(self):
        if self.mode == 'iter':
            links = self.read_file(self.external_links, True)
        else:
            links = [self.url]
        for link in links:
            parsed_links = re.finditer(self.image_pat, self.get_html(link))
            for parsed in {p.group() for p in parsed_links}:
                if format == 'clean':
                    self.loot(self.clean(sanitize('https:' + parsed)))
                else:
                    self.loot(sanitize('https:' + parsed))
                sleep(self.tickrate)
        self.cleanup(self.path_main)
