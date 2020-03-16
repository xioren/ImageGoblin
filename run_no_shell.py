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


main(url='http://www.just.pt/model.php?department=allmodels&type=Main_Women&id=2339',
     mode=1, timeout=5, save_loc=None, format='auto', overwrite=False, increment=1, nodl=0)
