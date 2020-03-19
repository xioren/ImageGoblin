from handlers.agent_provocateur import AgentProvocateurGoblin
from handlers.ami_clubwear import AMIGoblin
from handlers.anthropologie import AnthropologieGoblin
from handlers.asos import ASOSGoblin
from handlers.behance import BehanceGoblin
from handlers.bershka import BershkaGoblin
from handlers.bluebella import BlueBellaGoblin
from handlers.blush import BlushGoblin
from handlers.boohoo import BoohooGoblin
from handlers.boux_avenue import BouxAvenueGoblin
from handlers.calvin_klein import CalvinKleinGoblin
from handlers.caroswim import CaroSwimGoblin
from handlers.dolls_kill import DollsKillGoblin
from handlers.dora_larsen import DoraLarsenGoblin
from handlers.elcorte import ElcorteGoblin
from handlers.etam import EtamGoblin
from handlers.fashion_nova import FashionNovaGoblin
from handlers.five_dancewear import FiveDancewearGoblin
from handlers.format import FormatGoblin
from handlers.fredericks import FredericksGoblin
from handlers.free_people import FreePeopleGoblin
from handlers.generic_omega import OmegaGoblin
from handlers.getty import GettyGoblin
from handlers.hunkemoller import HunkemollerGoblin
from handlers.instagram import InstagramGoblin
from handlers.iterator import IteratorGoblin
from handlers.katherine_hamilton import KatherineHamiltonGoblin
from handlers.lemanagement import LemanagementGoblin
from handlers.maison_lejaby import MaisonLejabyGoblin
from handlers.mango import MangoGoblin
from handlers.maison_close import MaisonCloseGoblin
from handlers.missguided import MissguidedGoblin
from handlers.only_hearts import OnlyHeartsGoblin
from handlers.oysho import OyshoGoblin
from handlers.prettylittlething import PrettyLittleThingGoblin
from handlers.pull_and_bear import PullandBearGoblin
from handlers.sandro import SandroGoblin
from handlers.savagex import SavageXGoblin
from handlers.shopbop import ShopbopGoblin
from handlers.shopify import ShopifyGoblin
from handlers.springfield import SpringfieldGoblin
from handlers.stockholmsgruppen import StockholmsgruppenGoblin
from handlers.stradivarius import StradivariusGoblin
from handlers.tommy_hilfiger import TommyHilfigerGoblin
from handlers.topshop import TopshopGoblin
from handlers.triangl import TrianglGoblin
from handlers.underprotection import UnderprotectionGoblin
from handlers.urban_outfitters import UrbanOutfittersGoblin
from handlers.victorias_secret import VictoriasSecretGoblin
from handlers.vitamin_a import VitaminAGoblin
from handlers.wix import WixGoblin
from handlers.womens_secret import WomensSecretGoblin
from handlers.yandy import YandyGoblin
from handlers.zalando import ZalandoGoblin


handlers = {
            'agent': (r'agentprovocateur', AgentProvocateurGoblin),
            'ami': (r'amiclubwear', AMIGoblin),
            'anthropologie': (r'anthropologie', AnthropologieGoblin),
            'asos': (r'asos|(\d+\-\d(\-\[a-z-9]+)*)$', ASOSGoblin),
            'behance': (r'behance', BehanceGoblin),
            'bershka': (r'bershka', BershkaGoblin),
            'bluebella': (r'bluebella', BlueBellaGoblin),
            'blushlingerie': (r'blushlingerie', BlushGoblin),
            'boohoo': (r'boohoo|adis\.ws', BoohooGoblin),
            'boux': (r'bouxavenue', BouxAvenueGoblin),
            'calvin': (r'calvinklein(eu)*', CalvinKleinGoblin),
            'caroswim': (r'caroswim', CaroSwimGoblin),
            'dolls': (r'dollskill', DollsKillGoblin),
            'dora': (r'doralarsen', DoraLarsenGoblin),
            'elcorte': (r'elcorteingles', ElcorteGoblin),
            'etam': (r'etam', EtamGoblin),
            'fashionnova': (r'fashionnova', FashionNovaGoblin),
            'fivedance': (r'fivedancewear', FiveDancewearGoblin),
            'fredericks': (r'fredericks', FredericksGoblin),
            'format': (r'format', FormatGoblin),
            'free': (r'freepeople', FreePeopleGoblin),
            'generic_omega': ('#####', OmegaGoblin),
            'getty': (r'getty', GettyGoblin),
            'hunk': (r'hunkemoller', HunkemollerGoblin),
            'insta': (r'instagram', InstagramGoblin),
            'iter': (r'%%%\d+%%%', IteratorGoblin),
            'katherine': (r'katherinehamilton', KatherineHamiltonGoblin),
            'leman': (r'lemanagement', LemanagementGoblin),
            'maisonclose': (r'maison-close', MaisonCloseGoblin),
            'maisonlejaby': (r'maisonlejaby', MaisonLejabyGoblin),
            'mango': (r'mango|mngbcn', MangoGoblin),
            'miss': (r'missguided', MissguidedGoblin),
            'onlyhearts': (r'onlyhearts', OnlyHeartsGoblin),
            'oysho': (r'oysho', OyshoGoblin),
            'prettylittlething': (r'prettylittlething', PrettyLittleThingGoblin),
            'pull': (r'pullandbear', PullandBearGoblin),
            'sandro': (r'sandro-paris', SandroGoblin),
            'savagex': (r'savagex', SavageXGoblin),
            'shopbop': (r'shopbop', ShopbopGoblin),
            'shopify': (r'shopify', ShopifyGoblin),
            'spring': (r'myspringfield', SpringfieldGoblin),
            'stock': (r'stockholmsgruppen', StockholmsgruppenGoblin),
            'strat': (r'stradivarius', StradivariusGoblin),
            'tommy':(r'tommy-europe|shoptommy', TommyHilfigerGoblin),
            'topshop': (r'topshop', TopshopGoblin),
            'triangl': (r'triangl', TrianglGoblin),
            'under': (r'underprotection', UnderprotectionGoblin),
            'urban':(r'urbanoutfitters(eu)*', UrbanOutfittersGoblin),
            'victoria': (r'victoriassecret', VictoriasSecretGoblin),
            'vitamina': (r'vitaminaswim', VitaminAGoblin),
            'wix': (r'wix', WixGoblin),
            'women': (r'womenssecret', WomensSecretGoblin),
            'yandy': (r'yandy(cdn)*', YandyGoblin),
            'zalando': (r'zalando|ztat\.net|[A-Z0-9]+-[A-Z]\d{2}(@\d)*', ZalandoGoblin)
            }
