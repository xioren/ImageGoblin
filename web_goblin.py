#!/usr/bin/env python3
from argparse import ArgumentParser
from coordinator import Coordinator


parser = ArgumentParser()
parser.add_argument('url', nargs='?', help='webpage or media url')
parser.add_argument('-m', '--mode', help='mode of operation')
parser.add_argument('-s', '--silent', help='suppress output', action='store_true')
parser.add_argument('-t', '--timeout', help='iteration timeout threshold (n)',
                    type=int, default=5)
parser.add_argument('-f', '--format', nargs='+', help='formatting modifier (action modifier[ modifier])')
parser.add_argument('-i', '--increment', help='iteration step size (n)',
                    type=int, default=1)
parser.add_argument('-n', '--nodl', help='skip downloading and print links to stdout',
                    action='store_true')
parser.add_argument('-r', '--rate', help='program tickrate (n)', type=float, default=1)
parser.add_argument('-l', '--local', help='filename of local text file containing links')
parser.add_argument('--force', help='force a specific handler')
parser.add_argument('--list', help='list available handlers', action='store_true')
parser.add_argument('--nosort', help='download directly to current directory, without creating a sub dirs',
                    action='store_true')
parser.add_argument('--noclean', help='do not remove small files',
                    action='store_true')
args = parser.parse_args()


args_dict = {'url': args.url, 'mode': args.mode, 'timeout': args.timeout,
             'format': args.format, 'increment': args.increment, 'nodl': args.nodl,
             'silent': args.silent, 'tickrate': args.rate, 'local': args.local,
             'handler': args.force, 'list': args.list, 'nosort': args.nosort}


if __name__ == '__main__':
    Coordinator(args_dict).deploy()
