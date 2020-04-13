from goblins.agent_provocateur import AgentProvocateurGoblin
from goblins.american_apparel import AmericanApparelGoblin
from goblins.ami_clubwear import AMIGoblin
from goblins.ann_summers import AnnSummersGoblin
from goblins.anthropologie import AnthropologieGoblin
from goblins.asos import ASOSGoblin
from goblins.bamba_swim import BambaSwimGoblin
from goblins.behance import BehanceGoblin
from goblins.bershka import BershkaGoblin
from goblins.bikini_lovers import BikiniLoversGoblin
from goblins.bluebella import BlueBellaGoblin
from goblins.blush import BlushGoblin
from goblins.boohoo import BoohooGoblin
from goblins.bordelle import BordelleGoblin
from goblins.boux_avenue import BouxAvenueGoblin
from goblins.burberry import BurberryGoblin
from goblins.c_and_a import CAGoblin
from goblins.calvin_klein import CalvinKleinGoblin
from goblins.caroswim import CaroSwimGoblin
from goblins.cecilie_copenhagen import CecilieGoblin
from goblins.dolls_kill import DollsKillGoblin
from goblins.dora_larsen import DoraLarsenGoblin
from goblins.else_lingerie import ElseGoblin
from goblins.esprit import EspritGoblin
from goblins.etam import EtamGoblin
from goblins.fae import FaeGoblin
from goblins.faithfull_the_brand import FaithfullTheBrandGoblin
from goblins.fashion_nova import FashionNovaGoblin
from goblins.five_dancewear import FiveDancewearGoblin
from goblins.fleur_du_mal import FleurDuMalGoblin
from goblins.flickr import FlickrGoblin
from goblins.for_love_and_lemons import ForLoveAndLemonsGoblin
from goblins.fortnight import FortnightGoblin
from goblins.fredericks import FredericksGoblin
from goblins.free_people import FreePeopleGoblin
from goblins.generic_omega import OmegaGoblin
from goblins.getty import GettyGoblin
from goblins.guess import GuessGoblin
from goblins.h_and_m import HMGoblin
from goblins.hungry import HungryGoblin
from goblins.hunkemoller import HunkemollerGoblin
from goblins.hot_topic import HotTopicGoblin
from goblins.instagram import InstagramGoblin
from goblins.intimissimi import IntimissimiGoblin
from goblins.iterator import IteratorGoblin
from goblins.jennyfer import JennyferGoblin
from goblins.katherine_hamilton import KatherineHamiltonGoblin
from goblins.kiki_de_montparnasse import KikiDeMontparnasseGoblin
from goblins.koton import KotonGoblin
from goblins.le_petit_trou import LePetitTrouGoblin
from goblins.livy import LivyGoblin
from goblins.lounge import LoungeGoblin
from goblins.maison_lejaby import MaisonLejabyGoblin
from goblins.maison_close import MaisonCloseGoblin
from goblins.mango import MangoGoblin
from goblins.marlies_dekkers import MarliesDekkersGoblin
from goblins.massimodutti import MassimoDuttiGoblin
from goblins.missguided import MissguidedGoblin
from goblins.nasty_gal import NastyGalGoblin
from goblins.only_hearts import OnlyHeartsGoblin
from goblins.oysho import OyshoGoblin
from goblins.prettylittlething import PrettyLittleThingGoblin
from goblins.promise import PromiseGoblin
from goblins.pull_and_bear import PullandBearGoblin
from goblins.reserved import ReservedGoblin
from goblins.sandro import SandroGoblin
from goblins.savagex import SavageXGoblin
from goblins.shopbop import ShopbopGoblin
from goblins.shopify import ShopifyGoblin
from goblins.simone_perele import SimonePereleGoblin
from goblins.skin import SkinGoblin
from goblins.springfield import SpringfieldGoblin
from goblins.ssense import SsenseGoblin
from goblins.stradivarius import StradivariusGoblin
from goblins.tally_weijl import TallyWeijlGoblin
from goblins.tezenis import TezenisGoblin
from goblins.the_great_eros import TheGreatErosGoblin
from goblins.the_iconic import TheIconicGoblin
from goblins.tommy_hilfiger import TommyHilfigerGoblin
from goblins.topshop import TopshopGoblin
from goblins.trendyol import TrendyolGoblin
from goblins.triangl import TrianglGoblin
from goblins.underprotection import UnderprotectionGoblin
from goblins.urban_outfitters import UrbanOutfittersGoblin
from goblins.victorias_secret import VictoriasSecretGoblin
from goblins.vila import VilaGoblin
from goblins.vitamin_a import VitaminAGoblin
from goblins.watercult import WatercultGoblin
from goblins.wolford import WolfordGoblin
from goblins.womens_secret import WomensSecretGoblin
from goblins.wood_wood import WoodWoodGoblin
from goblins.yandy import YandyGoblin
from goblins.yargici import YargiciGoblin
from goblins.zalando import ZalandoGoblin
from goblins.zara import ZaraGoblin
from goblins.generic_zeta import ZetaGoblin


goblins = {
    'agentprovocateur': ('agentprovocateur', AgentProvocateurGoblin),
    'americanapparel': ('americanapparel', AmericanApparelGoblin),
    'amiclubwear': ('amiclubwear', AMIGoblin),
    'annsummers': ('annsummers', AnnSummersGoblin),
    'anthropologie': ('anthropologie', AnthropologieGoblin),
    'asos': (r'asos|(\d+-\d(-[a-z-9]+)?(\.jpe?g)?)$', ASOSGoblin),
    'bambaswim': ('bambaswim', BambaSwimGoblin),
    'behance': (r'behance|mir\-s3\-cdn', BehanceGoblin),
    'bershka': ('bershka', BershkaGoblin),
    'bikinilovers': ('bikinilovers', BikiniLoversGoblin),
    'bluebella': ('bluebella.com', BlueBellaGoblin),
    'blush': ('blushlingerie', BlushGoblin),
    'boohoo': (r'boohoo|adis\.ws', BoohooGoblin),
    'bordelle': ('bordelle', BordelleGoblin),
    'bouxavenue': ('bouxavenue', BouxAvenueGoblin),
    'burberry': ('burberry', BurberryGoblin),
    'canda': ('c-and-a', CAGoblin),
    'calvinklein': (r'calvinklein(eu)?', CalvinKleinGoblin),
    'caroswim': ('caroswim', CaroSwimGoblin),
    'ceciliecopenhagen': ('ceciliecopenhagen', CecilieGoblin),
    'dollskill': ('dollskill', DollsKillGoblin),
    'doralarsen': ('doralarsen', DoraLarsenGoblin),
    'else': ('elselingerie', ElseGoblin),
    'esprit': (r'esprit\.[a-z]+', EspritGoblin),
    'etam': ('etam', EtamGoblin),
    'fae': ('fae.house', FaeGoblin),
    'fashionnova': ('fashionnova', FashionNovaGoblin),
    'faithfullthebrand': ('faithfullthebrand', FaithfullTheBrandGoblin),
    'fivedancewear': ('fivedancewear', FiveDancewearGoblin),
    'fleurdumal': ('fleurdumal', FleurDuMalGoblin),
    'flickr': ('flickr', FlickrGoblin),
    'fredericks': ('fredericks', FredericksGoblin),
    'forloveandlemons': ('forloveandlemons', ForLoveAndLemonsGoblin),
    'fortnight': ('fortnightlingerie', FortnightGoblin),
    'freepeople': ('freepeople', FreePeopleGoblin),
    'generic': ('#####', OmegaGoblin),
    'getty': ('gettyimages', GettyGoblin),
    'guess': (r'guess(-img)?', GuessGoblin),
    'handm': ('hm.com', HMGoblin),
    'hungry': ('#####', HungryGoblin),
    'hunkemoller': ('hunkemoller', HunkemollerGoblin),
    'hottopic': ('hottopic', HotTopicGoblin),
    'instagram': ('instagram', InstagramGoblin),
    'intimissimi': ('intimissimi', IntimissimiGoblin),
    'iterator': (r'#\d+#', IteratorGoblin),
    'jennyfer': ('jennyfer', JennyferGoblin),
    'katherinehamilton': ('katherinehamilton', KatherineHamiltonGoblin),
    'kikidemontparnasse': ('kikidm', KikiDeMontparnasseGoblin),
    'koton': (r'koton|ktnimg', KotonGoblin),
    'lepetittrou': ('le-petit-trou.com', LePetitTrouGoblin),
    'livy': ('li-vy', LivyGoblin),
    'lounge': ('loungeunderwear', LoungeGoblin),
    'maisonclose': ('maison-close', MaisonCloseGoblin),
    'maisonlejaby': ('maisonlejaby', MaisonLejabyGoblin),
    'mango': (r'mango|mngbcn', MangoGoblin),
    'marliesdekkers': ('marliesdekkers', MarliesDekkersGoblin),
    'massimodutti': ('massimodutti', MassimoDuttiGoblin),
    'missguided': ('missguided', MissguidedGoblin),
    'nastygal': (r'nastygal|i\d.adis.ws', NastyGalGoblin),
    'onlyhearts': ('onlyhearts', OnlyHeartsGoblin),
    'oysho': ('oysho', OyshoGoblin),
    'prettylittlething': ('prettylittlething', PrettyLittleThingGoblin),
    'promise': ('tienda.promise', PromiseGoblin),
    'pullandbear': ('pullandbear', PullandBearGoblin),
    'reserved': ('reserved', ReservedGoblin),
    'sandro': ('sandro-paris', SandroGoblin),
    'savagex': ('savagex', SavageXGoblin),
    'shopbop': ('shopbop', ShopbopGoblin),
    'shopify': ('shopify', ShopifyGoblin),
    'simoneperele': (r'simone-?perele', SimonePereleGoblin),
    'skin': ('skinworldwide', SkinGoblin),
    'springfield': ('myspringfield', SpringfieldGoblin),
    'ssense': (r'ssense(media)?', SsenseGoblin),
    'stradivarius': ('stradivarius', StradivariusGoblin),
    'tallyweijl': ('tally-weijl', TallyWeijlGoblin),
    'tezenis': ('tezenis', TezenisGoblin),
    'thegreateros': ('thegreateros', TheGreatErosGoblin),
    'theiconic': ('theiconic', TheIconicGoblin),
    'tommyhilfiger':(r'tommy-europe|shoptommy', TommyHilfigerGoblin),
    'topshop': ('topshop.com', TopshopGoblin),
    'trendyol': ('trendyol', TrendyolGoblin),
    'triangl': ('triangl.com', TrianglGoblin),
    'underprotection': ('underprotection', UnderprotectionGoblin),
    'urbanoutfitters':(r'urbanoutfitters(eu)?', UrbanOutfittersGoblin),
    'victoriassecret': ('victoriassecret', VictoriasSecretGoblin),
    'vila': ('vila', VilaGoblin),
    'vitamina': ('vitaminaswim', VitaminAGoblin),
    'watercult': ('watercult.com', WatercultGoblin),
    'wolford': ('wolfordshop', WolfordGoblin),
    'womensecret': ('womensecret', WomensSecretGoblin),
    'woodwood': ('woodwood', WoodWoodGoblin),
    'yandy': (r'yandy(cdn)?', YandyGoblin),
    'yargici': ('yargici', YargiciGoblin),
    'zalando': (r'zalando|ztat\.net|[A-Z0-9]+-[A-Z]\d{2}@\d', ZalandoGoblin),
    'zara': ('zara', ZaraGoblin),
    'zeta': ('calzedonia', ZetaGoblin)
    }
