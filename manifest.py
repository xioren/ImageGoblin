from handlers.asos import ASOSGoblin
from handlers.behance import BehanceGoblin
from handlers.bershka import BershkaGoblin
from handlers.boohoo import BoohooGoblin
from handlers.calvin_klein import CalvinKleinGoblin
from handlers.elcorte import ElcorteGoblin
from handlers.etam import EtamGoblin
from handlers.fashion_nova import FashionNovaGoblin
from handlers.five_dancewear import FiveDancewearGoblin
from handlers.format import FormatGoblin
from handlers.free_people import FreePeopleGoblin
from handlers.generic_omega import OmegaGoblin
from handlers.getty import GettyGoblin
from handlers.hunkemoller import HunkemollerGoblin
from handlers.instagram import InstagramGoblin
from handlers.iterator import IteratorGoblin
from handlers.lemanagement import LemanagementGoblin
from handlers.mango import MangoGoblin
from handlers.missguided import MissguidedGoblin
from handlers.next import NextGoblin
from handlers.oysho import OyshoGoblin
from handlers.pull_and_bear import PullandBearGoblin
from handlers.sandro import SandroGoblin
from handlers.shopbop import ShopbopGoblin
from handlers.shopify import ShopifyGoblin
from handlers.springfield import SpringfieldGoblin
from handlers.stockholmsgruppen import StockholmsgruppenGoblin
from handlers.stradivarius import StradivariusGoblin
from handlers.tommy_hilfiger import TommyHilfigerGoblin
from handlers.topshop import TopshopGoblin
from handlers.urban_outfitters import UrbanOutfittersGoblin
from handlers.victorias_secret import VictoriasSecretGoblin
from handlers.wix import WixGoblin
from handlers.womens_secret import WomensSecretGoblin
from handlers.zalando import ZalandoGoblin


handlers = {
            'asos': (r'asos|(\d+\-\d(\-\[a-z-9]+)*)$', ASOSGoblin),
            'behance': (r'behance', BehanceGoblin),
            'bershka': (r'bershka', BershkaGoblin),
            'boohoo': (r'boohoo|adis\.ws', BoohooGoblin),
            'calvin': (r'CalvinKlein(EU)*', CalvinKleinGoblin),
            'elcorte': (r'elcorteingles', ElcorteGoblin),
            'etam': (r'etam', EtamGoblin),
            'fashionnova': (r'fashionnova', FashionNovaGoblin),
            'fivedance': (r'fivedancewear', FiveDancewearGoblin),
            'format': (r'format', FormatGoblin),
            'free': (r'FreePeople', FreePeopleGoblin),
            'generic_omega': ('#####', OmegaGoblin),
            'getty': (r'getty', GettyGoblin),
            'hunk': (r'hunkemoller', HunkemollerGoblin),
            'insta': (r'instagram', InstagramGoblin),
            'iter': (r'%%%\d+%%%', IteratorGoblin),
            'leman': (r'lemanagement', LemanagementGoblin),
            'mango': (r'mango|mngbcn', MangoGoblin),
            'miss': (r'missguided', MissguidedGoblin),
            'next': (r'(s\d\.amazonaws|res\.cloudinary)\.com/next\-management', NextGoblin),
            'oysho': (r'oysho', OyshoGoblin),
            'pull': (r'pullandbear', PullandBearGoblin),
            'sandro': (r'sandro-paris', SandroGoblin),
            'shopbop': (r'(S|s)hopbop', ShopbopGoblin),
            'shopify': (r'shopify', ShopifyGoblin),
            'spring': (r'myspringfield', SpringfieldGoblin),
            'stock': (r'stockholmsgruppen', StockholmsgruppenGoblin),
            'strat': (r'stradivarius', StradivariusGoblin),
            'tommy':(r'tommy-europe|shoptommy', TommyHilfigerGoblin),
            'topshop': (r'topshop', TopshopGoblin),
            'urban':(r'UrbanOutfitters(EU)*', UrbanOutfittersGoblin),
            'victoria': (r'victoriassecret', VictoriasSecretGoblin),
            'wix': (r'wix', WixGoblin),
            'women': (r'womenssecret', WomensSecretGoblin),
            'zalando': (r'zalando|ztat\.net|[A-Z0-9]+-[A-Z]\d{2}(@\d)*', ZalandoGoblin)
            }
