#!/usr/bin/env python3
from argparse import ArgumentParser
from coordinator import Coordinator


parser = ArgumentParser()
parser.add_argument('url', help='webpage or media url')
parser.add_argument('-m', '--mode', help='mode of operation (1, 2, 3)')
parser.add_argument('-v', '--verbose', help='verbose output',
                    action='store_true')
parser.add_argument('-t', '--timeout', help='iteration timeout threshold (n)',
                    type=int, default=5)
parser.add_argument('-f', '--format', nargs='+', help='formatting modifier (action modifier[ modifier])',
                    default=None)
parser.add_argument('-i', '--increment', help='iteration step size (n)',
                    type=int, default=1)
parser.add_argument('-n', '--nodl', help='skip downloading and print (1) or write (2) links',
                    action='store_true')
parser.add_argument('-r', '--rate', help='program tickrate (n)',
                    type=int, default=1)
args = parser.parse_args()


if __name__ == '__main__':
    Coordinator(args.url, args.mode, args.timeout, args.format,
                args.increment, args.nodl, args.verbose, args.rate).deploy()
