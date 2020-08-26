from meta import MetaGoblin

# NOTE: same as francina

class MonsterGoblin(MetaGoblin):
	'''accepts:
		- webpage
	'''

	NAME = 'monster management goblin'
	ID = 'monster'
	API_URL = 'https://monster-mgmt.com/api/models/details'

	def __init__(self, args):
		super().__init__(args)

	def extract_id(self, url):
		'''extract model id from url'''
		return url.split('-')[1].split('/')[-1]

	def main(self):
		self.logger.log(1, self.NAME, 'collecting urls')
		urls = []

		for target in self.args['targets'][self.ID]:
			model_id = self.extract_id(target)

			response = self.parser.load_json(self.get(f'{self.API_URL}/{model_id}').content)

			# NOTE: video book present in json but not used
			if 'ActiveBook' in response:
				for page in response['ActiveBook'].get('Pages', ''):
					urls.append(page['Picture']['URL'])

			self.delay()

		for url in urls:
			self.collect(url)

		self.loot()
