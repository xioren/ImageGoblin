from meta import MetaGoblin


class TumblrGoblin(MetaGoblin):
	'''accepts:
		- image
		- webpage
	'''

	NAME = 'tumblr goblin'
	ID = 'tumblr'
	URL_PAT = r'https://\d+\.media\.tumblr\.com/[a-z\-/\d]+\.[a-z\d]+'

	def __init__(self, args):
		super().__init__(args)

	def main(self):
		self.logger.log(1, self.NAME, 'collecting urls')
		urls = []
		self.headers.update({'Accept': 'text/html'})

		for target in self.args['targets'][self.ID]:
			if 'media.tumblr' in target:
				urls.append(target)
			else:
				self.logger.log(2, self.NAME, 'WARNING', 'webpage urls not fully supported', once=True)
				urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

			self.delay()

		for url in urls:
			if 'tumblr_' in url:
				if '.gif' in target:
					self.collect(self.parser.regex_sub(r'\d+(?=\.gif)', '540', url))
				else:
					self.collect(self.parser.regex_sub(r'\d+(?=\.jpg)', '1280', url))
			else:
				for alt_url in self.parser.extract_by_regex(self.get(self.parser.regex_sub(r's\d+x\d+', f's10000x10000', url)).content, self.URL_PAT):
					if 's10000x10000' not in alt_url:
						self.collect(alt_url)
				self.delay()

		self.headers.update({'Accept': 'image/webp,*/*'})
		self.loot()
