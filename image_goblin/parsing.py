import re
import json
import mimetypes
import urllib.parse

from os.path import join, exists


class Parser:
	'''generic url/html/string parsing and manipulation utilities'''

	QUALITY_PAT = re.compile(r'q((ua)?li?ty)?=\d+')
	FILTER_PAT = re.compile(r'(?:\.(js|css|pdf|php|html|svg(\+xml)?)|favicon|[{}])', flags=re.IGNORECASE)
	MISC_REPLACEMENTS = {'amp;': '', 'background-image:url(': ''}
	ABSOLUTE_PAT = r'(?:/?[^/\.]+\.[^/]+(?=/))'
	CROPPING_PATS = (
		re.compile(r'[\-_]?((x+)?-?(?<![\w\-])l(arge)?(?!\w)|profile|square)(?![\w])[\-_/]?', flags=re.IGNORECASE),
		re.compile(r'[\.-_]\d+w(?=[-_\.])|[\.-_]w\d+(?=[-_\.])'), # -000w
		re.compile(r'(?<=/)([a-z]_[a-z\d:]+,?)+/(v\d/)?'), # cloudfront (probably too general and will catch false positives)
		re.compile(r'[@\-_/\.]\d+x(\d+)?(?![a-z\d])'), # 000x000
		re.compile(r'expanded_[a-z]+/'),
		re.compile(r'/v/\d/.+\.webp$'), # wix
		re.compile(r'-e\d+(?=\.)'),
		re.compile(r'@\d+x')
	)

	def __init__(self, origin_url, user_formatting, ext_filter):
		self.ext_filter = [self.extension(f'null.{ext.lstrip(".")}') for ext in ext_filter.split(',')]
		self.origin_url = self.add_scheme(self.dequery(origin_url))
		self.user_formatting = user_formatting
		mimetypes.add_type('image/webp', '.webp')

####################################################################
# sub classes
####################################################################

	class GoblinHTMLParser:
		'''html tag parser'''

		ELEMENT_PAT = re.compile(r'<[a-z]+\s[^>]+>')
		TAG_PAT = re.compile(r'(?<=<)[a-z\-]+')
		ATTRIBUTE_PAT = re.compile(r'[a-z\d\-]+="[^"]+')

		def __init__(self, content):
			self.html = content
			self.elements = {}

		def parse_elements(self):
			'''extract all elements from an html source'''
			for element in re.findall(self.ELEMENT_PAT, self.html):
				tag = re.search(self.TAG_PAT, element).group()
				if tag not in self.elements:
					self.elements[tag] = {}

				for attribute in re.findall(self.ATTRIBUTE_PAT, element):
					attr, value = attribute.split('="')
					if attr not in self.elements[tag]:
						self.elements[tag][attr] = [value]
					else:
						self.elements[tag][attr].append(value)

####################################################################
# methods
####################################################################

	def extract_by_tag(self, html, tags:'list of (tag, attr) tuples'=None):
		'''extract from html by tag'''
		html_parser = self.GoblinHTMLParser(html)
		html_parser.parse_elements()

		if tags:
			urls = []
			for item in tags:
				tag, attr = item
				if tag in html_parser.elements:
					urls.extend(html_parser.elements[tag].get(attr))
			return urls
		else:
			return html_parser.elements

	def extract_by_regex(self, html, pattern):
		'''extract from html by regex'''
		# NOTE: left in for compatibility, regex_findall does the work.
		return self.regex_findall(pattern, html)

	def extract_filename(self, url):
		'''extract filename from url'''
		filename = self.dequery(url).rstrip('/').split('/')[-1]
		return self.unquote(re.sub(r'\.\w{,4}$', '', filename))

	def decrop(self, url):
		'''remove common cropping from url'''
		for pat in self.CROPPING_PATS:
			url = re.sub(pat, '', url)
		return url

	def dequery(self, url):
		'''remove query string from url'''
		return url.split('?')[0]

	def sanitize(self, url):
		'''combine dequery and decrop'''
		return self.decrop(self.dequery(url))

	def unquote(self, filename):
		'''unquote filenames'''
		while '%' in filename:
			filename = urllib.parse.unquote(filename)
		return filename

	def make_url_safe(self, url):
		'''quote control characters in url (filename portion only)'''
		# NOTE: some morons have both quoted and unquoted control characters in the same url,
		# easiest approach --> unquote then requote all filenames.
		filename = self.extract_filename(url)

		return url.replace(filename, urllib.parse.quote(self.unquote(filename)))

	def extension(self, url):
		'''extract file extension from url'''
		ext = mimetypes.guess_type(self.dequery(url))[0]
		if ext:
			return f'.{ext.split("/")[1]}'.replace('svg+xml', 'svg')
		return ''

	def add_scheme(self, url):
		'''checks for and adds https scheme'''
		if not urllib.parse.urlparse(url)[0]:
			if url.startswith('.') or url.startswith('/'):
				pass
			else:
				return f'https://{url}'
		return url

	def finalize(self, url):
		'''prepare a url for an http request
		- add missing scheme
		- expand relative urls
		- handle control characters
		'''
		if re.search(self.ABSOLUTE_PAT, url): # absolute path
			url = self.add_scheme(url.lstrip('/'))
		else: # relative path
			url = urllib.parse.urljoin(self.origin_url, url)

		for item in self.MISC_REPLACEMENTS:
			url = url.replace(item, self.MISC_REPLACEMENTS[item])

		return self.make_url_safe(url.replace('\\', '').rstrip(')'))

	def make_unique(self, path):
		'''make filepath unique'''
		n = 1
		while True:
			new_path = join(path, f'({n}).'.join(path.split('.')))
			if exists(new_path):
				n += 1
			else:
				return new_path

	@staticmethod
	def valid_url(url):
		'''test url validity'''
		if not urllib.parse.urlparse(url).hostname:
			if not re.search(r'(?:(\.[a-z]+){1,2}/)', url):
				return False
		return True

	def regex_search(self, this, string, capture=True):
		'''safely make one line regex searches'''
		match = re.search(this, string)
		if match:
			if capture:
				return match.group()
			return True
		return ''

	def regex_findall(self, this, string):
		'''safely make one line iterative regex searches'''
		matches = re.finditer(this, string)
		if matches:
			return {match.group() for match in matches}
		return ''

	def regex_sub(self, this, that, string):
		'''make regex substitutions'''
		return re.sub(this, that, string)

	def regex_split(self, this, string, maxsplit=0):
		'''split a string via regex pattern'''
		return re.split(this, string, maxsplit=maxsplit)

	def regex_startswith(self, this, string):
		'''check if string starts with regex pattern'''
		return re.match(this, string)

	def regex_pattern(self, string, ignore=0):
		'''compile a regex pattern'''
		if ignore:
			flags = re.IGNORECASE
		else:
			flags = ignore
		return re.compile(string, flags=flags)

	def filter(self, url):
		'''filter unwanted urls'''
		if re.search(self.FILTER_PAT, url):
			return True
		elif self.ext_filter[0] and self.extension(url) not in self.ext_filter:
			return True
		return False

	def load_json(self, json_string):
		'''load JSON safely and if necessary fix improper use of double quote delimiters (*cough* imgur)'''
		if not json_string:
			return {}
		try:
			return json.loads(json_string)
		except json.JSONDecodeError:
			json_string = json_string.replace('\n', '').replace('\.', '.')
			values = self.regex_findall(r'(?<=:").+?(?="(,"|}))', json_string)
			for val in values:
				json_string = json_string.replace(val, val.replace('"', "'"))
			try:
				return json.loads(json_string)
			except json.JSONDecodeError:
				return {}

	def make_json(self, object):
		'''safely convert an object json'''
		try:
			return json.dumps(object)
		except TypeError:
			return '{}'

	def user_format(self, url):
		'''add, substitute, or remove arbitrary elements from a url'''
		if self.user_formatting[0] == 'add':
			# QUESTION: add auto query formatting? use urlencode?
			return self.dequery(url) + self.user_formatting[1]
		elif self.user_formatting[0] == 'sub':
			return re.sub(fr'{self.user_formatting[1]}', self.user_formatting[2], url)
		elif self.user_formatting[0] == 'rem':
			return re.sub(fr'{self.user_formatting[1]}', '', url)
		else:
			return url

	def auto_format(self, url):
		'''attempt to upscale common url formats'''
		quality = re.search(self.QUALITY_PAT, url)
		url = self.sanitize(url)

		if 'acidimg' in url:
			url = url.replace('small', 'big')
		elif 'i.f1g.fr' in url:
			url = re.sub(r'madame/(x\d+/)?', 'madame/orig/', url)
		elif 'imagetwist' in url:
			url = url.replace('/th/', '/i/').replace('.jpg', '.JPG')
		elif 'imgbox' in url:
			if '-t' in url or '.t' in url:
				url = re.sub(r'\d[\-\.]t', 'i', url)
			else:
				url = url.replace('_t', '_o').replace('thumb', 'image').replace('_b', '_o')
		elif 'imgcredit' in url:
			url = url.replace('.th', '').replace('.md', '')
		elif 'imx.to' in url:
			url = url.replace('/t/', '/i/')
		elif 'i.mdel.net' in url:
			url = url.replace('.jpg', '-orig.jpg')
		elif 'pimpandhost' in url:
			url = url.replace('_s', '').replace('_m', '')
		elif 'pixhost' in url:
			url = re.sub(r't(?![a-z])', 'img', url.replace('thumb', 'image'))
		elif 'pixroute' in url:
			url = url.replace('_t', '')
		elif 'redd.it' in url:
			url = self.dequery(url).replace('preview', 'i')
		elif 'cdn.shoplo' in url:
			url = re.sub(r'/th\d+/', '/orig/', url)
		elif 'squarespace' in url:
			url += '?format=original'
		elif 'tumblr' in url:
			if '.gif' in url:
				url = re.sub(r'\d+(?=\.gif)', '540', url)
			else:
				url = re.sub(r'\d+(?=\.jpg)', '1280', url)
		elif 'wix' in url:
			url = re.sub(r'(?<=\.jpg).+$', '', url)

		if quality:
			url += '?{}'.format(re.sub(r'\d+', '100', quality.group()))

		return url
