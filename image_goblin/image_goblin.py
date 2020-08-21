#!/usr/bin/env python3
from sys import exit
from argparse import ArgumentParser

from dispatching import Dispatcher
from version import __version__


parser = ArgumentParser(usage='image-goblin [URL] [OPTIONS]')

parser.add_argument('-d', '--delay', help='delay ("-1" for randomized delay), default: 0', type=float, default=0)

parser.add_argument('--dir', nargs='+', help='specify name or relative path of the download directory', type=str, default='')

parser.add_argument('--feed', help='input urls one at a time', action='store_true')

parser.add_argument('--filename', help='specify filename to use', type=str, default='')

parser.add_argument('--filter', help='specify which extension(s) to download jpg,png[,...]', type=str, default='')

parser.add_argument('--force', help='force a specific goblin')

parser.add_argument('-f', '--format', nargs='+', help='formatting modifier (action modifier[ modifier])')

parser.add_argument('--greedy', help='find urls based on regex instead of html tags (only applies to generic goblin)', action='store_true')

parser.add_argument('--list', help='list available goblins', action='store_true')

parser.add_argument('-l', '--local', help='filename of local text file containing urls')

parser.add_argument('--login', help='log in (goblin dependant)', action='store_true')

parser.add_argument('--mask', help='use a common user agent header', action='store_true')

parser.add_argument('--minsize', help='minimum filesize to download (in bytes) default: 30000 (30kb)', type=int, default=30000)

parser.add_argument('-m', '--mode', help='mode settings (goblin dependant)')

parser.add_argument('--nodl', help='print urls to stdout instead of downloading', action='store_true')

parser.add_argument('--noskip', help='make filename unique if a file with the same filename already exists, instead of skipping', action='store_true')

parser.add_argument('--nosort', help='download directly to current directory, without creating sub dirs', action='store_true')

parser.add_argument('--noup', help='do not remove cropping from urls', action='store_true')

parser.add_argument('--posts', help='number of posts (n<100) to fetch (goblin dependant)', type=int, default=100)

parser.add_argument('-s', '--silent', help='suppress output', action='store_true')

parser.add_argument('--step', help='iteration step size (n)', type=int, default=1)

parser.add_argument('-t', '--timeout', help='iteration timeout threshold (n)', type=int, default=5)

parser.add_argument('url', nargs='?', help='webpage or image url')

parser.add_argument('-v', '--verbose', help='verbose output', action='store_true')

parser.add_argument('--version', help='program version', action='store_true')

args = vars(parser.parse_args())


if not (args['url'] or args['feed'] or args['local'] or args['list']):
	parser.print_help()
	exit(22) # NOTE: invalid argument
elif args['version']:
	print(__version__)
	exit(0)


if __name__ == '__main__':
	try:
		Dispatcher(args).dispatch()
	except KeyboardInterrupt:
		print('\n<-----exiting----->')
		exit(125) # NOTE: operation cancelled
