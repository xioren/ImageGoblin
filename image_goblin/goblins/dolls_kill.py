from meta import MetaGoblin


# NOTE: 1 = higher res jpeg | 36 = lower res png


class DollsKillGoblin(MetaGoblin):
	'''accepts:
		- image*
		- webpage
	'''

	NAME = 'dolls kill goblin'
	ID = 'dollskill'
	URL_PAT = r'(?<=img\ssrc=")https?://media\.dollskill\.com[^"\s\']+-\d+\.jpe?g'

	def __init__(self, args):
		super().__init__(args)

	def main(self):
		self.logger.log(1, self.NAME, 'collecting urls')
		urls = []

		for target in self.args['targets'][self.ID]:
			if 'media.dollskill' in target:
				self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
				urls.append(target)
			else:
				urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

			self.delay()

		for url in urls:
			if self.args['mode'] == 'png':
				self.collect(f'{url.split("-")[0]}-36.png')
			else:
				self.collect(f'{url.split("-")[0]}-1.jpeg')

		self.loot()
