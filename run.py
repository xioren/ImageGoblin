#!/usr/bin/env python3
from argparse import ArgumentParser


def main(url, mode, timeout, save_loc, format, overwrite, increment, nodl):
    if mode == 2:
        from iterator import IterGoblin
        goblin = IterGoblin(url=url, timeout=timeout,
                            save_loc=save_loc, overwrite=overwrite,
                            increment=increment)
        goblin.iterate()
    elif mode == 3:
        from instagram import InstaGoblin
        goblin = InstaGoblin(url=url, save_loc=save_loc, overwrite=overwrite)
        goblin.find_posts()
        goblin.find_media()
        goblin.down_media()
    else:
        from grabber import GrabberGoblin
        goblin = GrabberGoblin(url=url, format=format,
                               save_loc=save_loc, overwrite=overwrite, nodl=nodl)
        goblin.link_grab()
        if not nodl:
            goblin.link_dl()


parser = ArgumentParser()
parser.add_argument('-u', '--url', help='webpage or media url',
                    default=None)
parser.add_argument('-m', '--mode', help='mode of operation',
                    type=int, default=1)
parser.add_argument('-t', '--timeout', help='iteration timeout',
                    type=int, default=5)
parser.add_argument('-s', '--save', help='save location',
                    default=None)
parser.add_argument('-f', '--format', help='custom formating',
                    default=None)
parser.add_argument('-o', '--overwrite', help='overwrite duplicate files',
                    type=bool, default=False)
parser.add_argument('-i', '--increment', help='iteration step size',
                    type=int, default=1)
parser.add_argument('-n', '--nodl', help='skip downloading and print or write links',
                    type=int, default=0)
args = parser.parse_args()


if __name__ == '__main__':
    main(url=args.url, mode=args.mode, timeout=args.timeout,
         save_loc=args.save, format=args.format, overwrite=args.overwrite,
         increment=args.increment, nodl=args.nodl)

# main(url='http://www.just.pt/model.php?department=allmodels&type=Main_Women&id=2339',
#      mode=2, timeout=5, save_loc=None, format='auto', overwrite=True, increment=1)
