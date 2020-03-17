#!/usr/bin/env python3
from argparse import ArgumentParser


def main(url, mode, timeout, format, increment, nodl, verbose, tickrate):
    if mode == 2:
        from iterator import IterGoblin
        goblin = IterGoblin(url=url, timeout=timeout, nodl=nodl, increment=increment,
                            verbose=verbose, tickrate=tickrate)
        goblin.iterate()
    elif mode == 3:
        from instagram import InstaGoblin
        goblin = InstaGoblin(url=url, verbose=verbose,
                             tickrate=tickrate, nodl=nodl)
        posts = goblin.find_posts()
        media = goblin.find_media(posts)
        goblin.down_media(media)
    else:
        from grabber import GrabberGoblin
        goblin = GrabberGoblin(url=url, format=format, nodl=nodl,
                               verbose=verbose, tickrate=tickrate)
        links = goblin.link_grab()
        if not nodl:
            goblin.link_dl(links)


parser = ArgumentParser()
parser.add_argument('url', help='webpage or media url',
                    default=None)
parser.add_argument('-m', '--mode', help='mode of operation',
                    type=int, default=1)
parser.add_argument('-v', '--verbose', help='verbosity',
                    type=bool, default=True)
parser.add_argument('-t', '--timeout', help='iteration timeout',
                    type=int, default=5)
parser.add_argument('-f', '--format', nargs='+', help='custom formating',
                    default=None)
parser.add_argument('-i', '--increment', help='iteration step size',
                    type=int, default=1)
parser.add_argument('-n', '--nodl', help='skip downloading and print or write links',
                    type=int, default=0)
parser.add_argument('-r', '--rate', help='program tickrate',
                    type=int, default=1)
args = parser.parse_args()


if __name__ == '__main__':
    main(url=args.url, mode=args.mode, timeout=args.timeout,
         verbose=args.verbose, format=args.format,
         increment=args.increment, nodl=args.nodl, tickrate=args.rate)
