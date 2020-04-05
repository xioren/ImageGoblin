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
from goblins.elcorte import ElcorteGoblin
from goblins.else_lingerie import ElseGoblin
from goblins.esprit import EspritGoblin
from goblins.etam import EtamGoblin
from goblins.fae import FaeGoblin
from goblins.faithfull_the_brand import FaithfullTheBrandGoblin
from goblins.fashion_nova import FashionNovaGoblin
from goblins.five_dancewear import FiveDancewearGoblin
from goblins.fleur_du_mal import FleurDuMalGoblin
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
from goblins.pull_and_bear import PullandBearGoblin
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
from goblins.vitamin_a import VitaminAGoblin
from goblins.wolford import WolfordGoblin
from goblins.womens_secret import WomensSecretGoblin
from goblins.wood_wood import WoodWoodGoblin
from goblins.yandy import YandyGoblin
from goblins.yargici import YargiciGoblin
from goblins.zalando import ZalandoGoblin
from goblins.zara import ZaraGoblin
from goblins.generic_zeta import ZetaGoblin


goblins = {
            'agentprovocateur': (r'agentprovocateur', AgentProvocateurGoblin),
            'americanapparel': (r'americanapparel', AmericanApparelGoblin),
            'amiclubwear': (r'amiclubwear', AMIGoblin),
            'annsummers': (r'annsummers', AnnSummersGoblin),
            'anthropologie': (r'anthropologie', AnthropologieGoblin),
            'asos': (r'asos|(\d+\-\d(\-\[a-z-9]+)*)$', ASOSGoblin),
            'bambaswim': (r'bambaswim', BambaSwimGoblin),
            'behance': (r'behance|mir\-s3\-cdn', BehanceGoblin),
            'bershka': (r'bershka', BershkaGoblin),
            'bikinilovers': (r'bikinilovers', BikiniLoversGoblin),
            'bluebella': (r'bluebella.com', BlueBellaGoblin),
            'blush': (r'blushlingerie', BlushGoblin),
            'boohoo': (r'boohoo|adis\.ws', BoohooGoblin),
            'bordelle': (r'bordelle', BordelleGoblin),
            'bouxavenue': (r'bouxavenue', BouxAvenueGoblin),
            'burberry': (r'burberry', BurberryGoblin),
            'canda': (r'c-and-a', CAGoblin),
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
            'geuss': (r'guess(-img)?', GuessGoblin),
            'handm': (r'hm\.com', HMGoblin),
            'hungry': ('#####', HungryGoblin),
            'hunkemoller': (r'hunkemoller', HunkemollerGoblin),
            'hottopic': (r'hottopic', HotTopicGoblin),
            'instagram': (r'instagram', InstagramGoblin),
            'intimissimi': (r'intimissimi', IntimissimiGoblin),
            'iterator': (r'@@@\d+@@@', IteratorGoblin),
            'jennyfer': (r'jennyfer', JennyferGoblin),
            'katherinehamilton': (r'katherinehamilton', KatherineHamiltonGoblin),
            'kikidemontparnasse': (r'kikidm', KikiDeMontparnasseGoblin),
            'koton': (r'koton|ktnimg', KotonGoblin),
            'lepetittrou': (r'le-petit-trou\.com', LePetitTrouGoblin),
            'livy': (r'li-vy', LivyGoblin),
            'lounge': (r'loungeunderwear', LoungeGoblin),
            'maisonclose': (r'maison-close', MaisonCloseGoblin),
            'maisonlejaby': (r'maisonlejaby', MaisonLejabyGoblin),
            'mango': (r'mango|mngbcn', MangoGoblin),
            'marliesdekkers': (r'marliesdekkers', MarliesDekkersGoblin),
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
            'stradivarius': (r'stradivarius', StradivariusGoblin),
            'tallyweijl': (r'tally-weijl', TallyWeijlGoblin),
            'tezenis': (r'tezenis', TezenisGoblin),
            'thegreateros': (r'thegreateros', TheGreatErosGoblin),
            'theiconic': (r'theiconic', TheIconicGoblin),
            'tommyhilfiger':(r'tommy-europe|shoptommy', TommyHilfigerGoblin),
            'topshop': (r'topshop.com', TopshopGoblin),
            'trendyol': (r'trendyol', TrendyolGoblin),
            'triangl': (r'triangl', TrianglGoblin),
            'underprotection': (r'underprotection', UnderprotectionGoblin),
            'urbanoutfitters':(r'urbanoutfitters(eu)*', UrbanOutfittersGoblin),
            'victoriassecret': (r'victoriassecret', VictoriasSecretGoblin),
            'vitamina': (r'vitaminaswim', VitaminAGoblin),
            'wolford': (r'wolfordshop', WolfordGoblin),
            'womensecret': (r'womensecret', WomensSecretGoblin),
            'woodwood': (r'woodwood', WoodWoodGoblin),
            'yandy': (r'yandy(cdn)*', YandyGoblin),
            'yargici': (r'yargici', YargiciGoblin),
            'zalando': (r'zalando|ztat\.net|[A-Z0-9]+-[A-Z]\d{2}(@\d)*', ZalandoGoblin),
            'zara': (r'zara', ZaraGoblin),
            'zeta': (r'calzedonia', ZetaGoblin)
            }
