#!/usr/bin/env python3
from sys import exit
from argparse import ArgumentParser

from dispatching import Dispatcher


parser = ArgumentParser(usage='goblin [URL] [OPTIONS]')

parser.add_argument('-d', '--delay', help='request delay, default: 0', type=float, default=0)

parser.add_argument('--feed', help='input urls one at a time', action='store_true')

parser.add_argument('--force', help='force a specific goblin')

parser.add_argument('-f', '--format', nargs='+', help='formatting modifier (action modifier[ modifier])')

parser.add_argument('--greedy', help='find urls based on regex instead of html tags (only applies to generic goblin)', action='store_true')

parser.add_argument('--list', help='list available goblins', action='store_true')

parser.add_argument('-l', '--local', help='filename of local text file containing urls')

parser.add_argument('--login', help='log in to instagram', action='store_true')

parser.add_argument('--mask', help='use a common user agent header', action='store_true')

parser.add_argument('-m', '--mode', help='mode of operation')

parser.add_argument('--noclean', help='do not remove small files', action='store_true')

parser.add_argument('--nodl', help='skip downloading and print urls to stdout', action='store_true')

parser.add_argument('--noskip', help='make filename unique if a file with the same filename already exists, instead of skipping', action='store_true')

parser.add_argument('--nosort', help='download directly to current directory, without creating sub dirs', action='store_true')

parser.add_argument('--noup', help='do not remove cropping from urls', action='store_true')

parser.add_argument('--posts', help='number of instagram posts (n) to fetch (optional, n<100)', type=int, default=100)

parser.add_argument('-s', '--silent', help='suppress output', action='store_true')

parser.add_argument('--step', help='iteration step size (n)', type=int, default=1)

parser.add_argument('-t', '--timeout', help='iteration timeout threshold (n)', type=int, default=5)

parser.add_argument('url', nargs='?', help='webpage or image url')

parser.add_argument('-v', '--verbose', help='output error messages for debugging', action='store_true')

args = vars(parser.parse_args())

if not args['url'] and not args['feed'] and not args['local']:
    parser.print_help()
    exit(22) # invalid argument

if __name__ == '__main__':
    try:
        Dispatcher(args).dispatch()
    except KeyboardInterrupt:
        print('\n-----exiting-----')
        exit(125) # operation cancelled
