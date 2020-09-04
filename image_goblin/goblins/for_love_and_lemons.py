from goblins.generic_theta import ThetaGoblin

# NOTE: collections use amazonaws and the filenames are horrendous.
# https://fll-image-uploads.s3.amazonaws.com/uploads/photo_lrg/large_2020-03-24_19%3A32-%20c7a18d16bc.jpeg

class ForLoveAndLemonsGoblin(ThetaGoblin):

    NAME = 'for love and lemons goblin'
    ID = 'forloveandlemons'

    def __init__(self, args):
        super().__init__(args)
