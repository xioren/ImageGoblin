from meta import MetaGoblin


class BurberryGoblin(MetaGoblin):
	'''accepts:
		- image*
		- webpage
	'''

	NAME = 'burberry goblin'
	ID = 'burberry'
	URL_PAT = r'https?://assets\.burberry\.com/is/image/Burberryltd/[^"\s]+'

	def __init__(self, args):
		super().__init__(args)

	def main(self):
		self.logger.log(1, self.NAME, 'collecting urls')
		urls = []

		for target in self.args['targets'][self.ID]:
			if 'assets.burberry' in target:
				self.logger.log(2, self.NAME, 'WARNING', 'image urls not fully supported', once=True)
				urls.append(target)
			else:
				urls.extend(self.parser.extract_by_regex(self.get(target).content, self.URL_PAT))

			self.delay()

		for url in urls:
			self.collect(f'{self.parser.dequery(url)}?scl=1')

		self.loot()
