#!/usr/bin/env python3
from argparse import ArgumentParser
from dispatcher import Dispatcher


parser = ArgumentParser()

parser.add_argument('-d', '--delay', help='request delay, default: 0', type=float, default=0)

parser.add_argument('--feed', help='input urls one at a time', action='store_true')

parser.add_argument('--force', help='force a specific goblin')

parser.add_argument('-f', '--format', nargs='+', help='formatting modifier (action modifier[ modifier])')

parser.add_argument('-i', '--increment', help='iteration step size (n)', type=int, default=1)

parser.add_argument('--list', help='list available goblins', action='store_true')

parser.add_argument('-l', '--local', help='filename of local text file containing urls')

parser.add_argument('-m', '--mode', help='mode of operation')

parser.add_argument('--noclean', help='do not remove small files', action='store_true')

parser.add_argument('-n', '--nodl', help='skip downloading and print urls to stdout', action='store_true')

parser.add_argument('--nosort', help='download directly to current directory, without creating sub dirs', action='store_true')

parser.add_argument('--noupgrade', help='do not remove cropping', action='store_true')

# parser.add_argument('--posts', help='number of instagram posts to fetch (optional)', type=int, default=0)

parser.add_argument('-s', '--silent', help='suppress output', action='store_true')

parser.add_argument('target', nargs='?', help='webpage or image url')

parser.add_argument('-t', '--timeout', help='iteration timeout threshold (n)', type=int, default=5)

parser.add_argument('-v', '--verbose', help='output error messages for debugging', action='store_true')

args = parser.parse_args()

args_dict = {
    'delay': args.delay,
    'feed': args.feed,
    'force': args.force,
    'format': args.format,
    'increment': args.increment,
    'list': args.list,
    'local': args.local,
    'mode': args.mode,
    'noclean': args.noclean,
    'nodl': args.nodl,
    'nosort': args.nosort,
    'noupgrade': args.noupgrade,
    # 'posts': args.posts,
    'silent': args.silent,
    'targets': args.target,
    'timeout': args.timeout,
    'verbose': args.verbose
    }

if __name__ == '__main__':
    Dispatcher(args_dict).dispatch()
