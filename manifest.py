from handlers.agent_provocateur import AgentProvocateurGoblin
from handlers.ami_clubwear import AMIGoblin
from handlers.anthropologie import AnthropologieGoblin
from handlers.asos import ASOSGoblin
from handlers.bamba_swim import BambaSwimGoblin
from handlers.behance import BehanceGoblin
from handlers.bershka import BershkaGoblin
from handlers.bikini_lovers import BikiniLoversGoblin
from handlers.bluebella import BlueBellaGoblin
from handlers.blush import BlushGoblin
from handlers.boohoo import BoohooGoblin
from handlers.bordelle import BordelleGoblin
from handlers.boux_avenue import BouxAvenueGoblin
from handlers.burberry import BurberryGoblin
from handlers.calvin_klein import CalvinKleinGoblin
from handlers.caroswim import CaroSwimGoblin
from handlers.cecilie_copenhagen import CecilieGoblin
from handlers.dolls_kill import DollsKillGoblin
from handlers.dora_larsen import DoraLarsenGoblin
from handlers.elcorte import ElcorteGoblin
from handlers.else_lingerie import ElseGoblin
from handlers.esprit import EspritGoblin
from handlers.etam import EtamGoblin
from handlers.fae import FaeGoblin
from handlers.faithfull_the_brand import FaithfullTheBrandGoblin
from handlers.fashion_nova import FashionNovaGoblin
from handlers.five_dancewear import FiveDancewearGoblin
from handlers.fleur_du_mal import FleurDuMalGoblin
from handlers.for_love_and_lemons import ForLoveAndLemonsGoblin
from handlers.fortnight import FortnightGoblin
from handlers.fredericks import FredericksGoblin
from handlers.free_people import FreePeopleGoblin
from handlers.generic_omega import OmegaGoblin
from handlers.getty import GettyGoblin
from handlers.h_and_m import HMGoblin
from handlers.hunkemoller import HunkemollerGoblin
from handlers.hot_topic import HotTopicGoblin
from handlers.instagram import InstagramGoblin
from handlers.iterator import IteratorGoblin
from handlers.jennyfer import JennyferGoblin
from handlers.katherine_hamilton import KatherineHamiltonGoblin
from handlers.le_petit_trou import LePetitTrouGoblin
from handlers.lounge import LoungeGoblin
from handlers.maison_lejaby import MaisonLejabyGoblin
from handlers.maison_close import MaisonCloseGoblin
from handlers.mango import MangoGoblin
from handlers.massimodutti import MassimoDuttiGoblin
from handlers.missguided import MissguidedGoblin
from handlers.nasty_gal import NastyGalGoblin
from handlers.only_hearts import OnlyHeartsGoblin
from handlers.oysho import OyshoGoblin
from handlers.prettylittlething import PrettyLittleThingGoblin
from handlers.pull_and_bear import PullandBearGoblin
from handlers.sandro import SandroGoblin
from handlers.savagex import SavageXGoblin
from handlers.shopbop import ShopbopGoblin
from handlers.shopify import ShopifyGoblin
from handlers.simone_perele import SimonePereleGoblin
from handlers.skin import SkinGoblin
from handlers.springfield import SpringfieldGoblin
from handlers.ssense import SsenseGoblin
from handlers.stockholmsgruppen import StockholmsgruppenGoblin
from handlers.stradivarius import StradivariusGoblin
from handlers.tally_weijl import TallyWeijlGoblin
from handlers.the_great_eros import TheGreatErosGoblin
from handlers.the_iconic import TheIconicGoblin
from handlers.tommy_hilfiger import TommyHilfigerGoblin
from handlers.topshop import TopshopGoblin
from handlers.trendyol import TrendyolGoblin
from handlers.triangl import TrianglGoblin
from handlers.underprotection import UnderprotectionGoblin
from handlers.urban_outfitters import UrbanOutfittersGoblin
from handlers.victorias_secret import VictoriasSecretGoblin
from handlers.vitamin_a import VitaminAGoblin
from handlers.wix import WixGoblin
from handlers.wolford import WolfordGoblin
from handlers.womens_secret import WomensSecretGoblin
from handlers.wood_wood import WoodWoodGoblin
from handlers.yandy import YandyGoblin
from handlers.zalando import ZalandoGoblin


handlers = {
            'agentprovocateur': (r'agentprovocateur', AgentProvocateurGoblin),
            'amiclubwear': (r'amiclubwear', AMIGoblin),
            'anthropologie': (r'anthropologie', AnthropologieGoblin),
            'asos': (r'asos|(\d+\-\d(\-\[a-z-9]+)*)$', ASOSGoblin),
            'bambaswim': (r'bambaswim', BambaSwimGoblin),
            'behance': (r'behance|mir\-s3\-cdn', BehanceGoblin),
            'bershka': (r'bershka', BershkaGoblin),
            'bikinilovers': (r'bikinilovers', BikiniLoversGoblin),
            'bluebella': (r'bluebella.com', BlueBellaGoblin),
            'blushlingerie': (r'blushlingerie', BlushGoblin),
            'boohoo': (r'boohoo|adis\.ws', BoohooGoblin),
            'bordelle': (r'bordelle', BordelleGoblin),
            'bouxavenue': (r'bouxavenue', BouxAvenueGoblin),
            'burberry': (r'burberry', BurberryGoblin),
            'calvinklein': (r'calvinklein(eu)*', CalvinKleinGoblin),
            'caroswim': (r'caroswim', CaroSwimGoblin),
            'ceciliecopenhagen': (r'ceciliecopenhagen', CecilieGoblin),
            'dollskill': (r'dollskill', DollsKillGoblin),
            'doralarsen': (r'doralarsen', DoraLarsenGoblin),
            'elcorteingles': (r'elcorteingles', ElcorteGoblin),
            'else': (r'elselingerie', ElseGoblin),
            'esprit': (r'esprit', EspritGoblin),
            'etam': (r'etam', EtamGoblin),
            'fae': (r'fae\.house', FaeGoblin),
            'fashionnova': (r'fashionnova', FashionNovaGoblin),
            'faithfullthebrand': (r'faithfullthebrand', FaithfullTheBrandGoblin),
            'fivedancewear': (r'fivedancewear', FiveDancewearGoblin),
            'fleurdumal': (r'fleurdumal', FleurDuMalGoblin),
            'fredericks': (r'fredericks', FredericksGoblin),
            'forloveandlemons': (r'forloveandlemons', ForLoveAndLemonsGoblin),
            'fortnight': (r'fortnightlingerie', FortnightGoblin),
            'freepeople': (r'freepeople', FreePeopleGoblin),
            'generic': ('#####', OmegaGoblin),
            'getty': (r'gettyimages', GettyGoblin),
            'h&m': (r'hm\.com', HMGoblin),
            'hunkemoller': (r'hunkemoller', HunkemollerGoblin),
            'hottopic': (r'hottopic', HotTopicGoblin),
            'instagram': (r'instagram', InstagramGoblin),
            'iterator': (r'%%%\d+%%%', IteratorGoblin),
            'jennyfer': (r'jennyfer', JennyferGoblin),
            'katherinehamilton': (r'katherinehamilton', KatherineHamiltonGoblin),
            'lepetittrou': (r'le-petit-trou', LePetitTrouGoblin),
            'lounge': (r'loungeunderwear', LoungeGoblin),
            'maisonclose': (r'maison-close', MaisonCloseGoblin),
            'maisonlejaby': (r'maisonlejaby', MaisonLejabyGoblin),
            'mango': (r'mango|mngbcn', MangoGoblin),
            'massimodutti': (r'massimodutti', MassimoDuttiGoblin),
            'missguided': (r'missguided', MissguidedGoblin),
            'nastygal': (r'nastygal|i\d.adis.ws', NastyGalGoblin),
            'onlyhearts': (r'onlyhearts', OnlyHeartsGoblin),
            'oysho': (r'oysho', OyshoGoblin),
            'prettylittlething': (r'prettylittlething', PrettyLittleThingGoblin),
            'pullandbear': (r'pullandbear', PullandBearGoblin),
            'sandro': (r'sandro-paris', SandroGoblin),
            'savagex': (r'savagex', SavageXGoblin),
            'shopbop': (r'shopbop', ShopbopGoblin),
            'shopify': (r'shopify', ShopifyGoblin),
            'simoneperele': (r'simoneperele', SimonePereleGoblin),
            'skin': (r'skinworldwide', SkinGoblin),
            'springfield': (r'myspringfield', SpringfieldGoblin),
            'ssense': (r'ssense(media)*', SsenseGoblin),
            'stockholmsgruppen': (r'stockholmsgruppen', StockholmsgruppenGoblin),
            'stradivarius': (r'stradivarius', StradivariusGoblin),
            'tallyweijl': (r'tally-weijl', TallyWeijlGoblin),
            'thegreateros': (r'thegreateros', TheGreatErosGoblin),
            'theiconic': (r'theiconic', TheIconicGoblin),
            'tommyhilfiger':(r'tommy-europe|shoptommy', TommyHilfigerGoblin),
            'topshop': (r'topshop.com', TopshopGoblin),
            'trendyol': (r'trendyol', TrendyolGoblin),
            'triangl': (r'triangl', TrianglGoblin),
            'underprotection': (r'underprotection', UnderprotectionGoblin),
            'urbanoutfitters':(r'urbanoutfitters(eu)*', UrbanOutfittersGoblin),
            'victoriassecret': (r'victoriassecret', VictoriasSecretGoblin),
            'vitaminaswim': (r'vitaminaswim', VitaminAGoblin),
            'wix': (r'wix', WixGoblin),
            'wolford': (r'wolfordshop', WolfordGoblin),
            'womensecret': (r'womensecret', WomensSecretGoblin),
            'woodwood': (r'woodwood', WoodWoodGoblin),
            'yandy': (r'yandy(cdn)*', YandyGoblin),
            'zalando': (r'zalando|ztat\.net|[A-Z0-9]+-[A-Z]\d{2}(@\d)*', ZalandoGoblin)
            }
