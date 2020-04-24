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
from goblins.brownie import BrownieGoblin
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
from goblins.hanne_bloch import HanneBlochGoblin
from goblins.hungry import HungryGoblin
from goblins.hunkemoller import HunkemollerGoblin
from goblins.hot_topic import HotTopicGoblin
from goblins.image_fap import ImageFapGoblin
from goblins.imgur import ImgurGoblin
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
from goblins.only import OnlyGoblin
from goblins.only_hearts import OnlyHeartsGoblin
from goblins.oysho import OyshoGoblin
from goblins.prettylittlething import PrettyLittleThingGoblin
from goblins.promise import PromiseGoblin
from goblins.pull_and_bear import PullandBearGoblin
from goblins.reserved import ReservedGoblin
from goblins.sandro import SandroGoblin
from goblins.savagex import SavageXGoblin
from goblins.shopbop import ShopbopGoblin
from goblins.simone_perele import SimonePereleGoblin
from goblins.skin import SkinGoblin
from goblins.springfield import SpringfieldGoblin
from goblins.ssense import SsenseGoblin
from goblins.stradivarius import StradivariusGoblin
from goblins.tally_weijl import TallyWeijlGoblin
from goblins.tezenis import TezenisGoblin
from goblins.the_great_eros import TheGreatErosGoblin
from goblins.the_iconic import TheIconicGoblin
from goblins.tisja_damen import TisjaDamenGoblin
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


goblins = {
    'agentprovocateur': (r'agentprovocateur\.[a-z]+', AgentProvocateurGoblin),
    'americanapparel': (r'americanapparel\.[a-z]+', AmericanApparelGoblin),
    'amiclubwear': (r'amiclubwear\.[a-z]+', AMIGoblin),
    'annsummers': (r'annsummers(\.[a-z]+|/)', AnnSummersGoblin),
    'anthropologie': (r'anthropologie(\.[a-z]+|/)', AnthropologieGoblin),
    'asos': (r'asos(-media)?\.[a-z]+', ASOSGoblin),
    'bambaswim': (r'bambaswim\.[a-z]+', BambaSwimGoblin),
    'behance': (r'behance\.[a-z]+|mir\-s3\-cdn', BehanceGoblin),
    'bershka': (r'bershka\.[a-z]+', BershkaGoblin),
    'bikinilovers': (r'bikinilovers\.[a-z]+', BikiniLoversGoblin),
    'bluebella': (r'bluebella\.[a-z]+', BlueBellaGoblin),
    'blush': (r'blushlingerie\.[a-z]+', BlushGoblin),
    'boohoo': (r'boohoo\.[a-z]+|adis\.ws', BoohooGoblin),
    'bordelle': (r'bordelle\.[a-z]+', BordelleGoblin),
    'bouxavenue': (r'bouxavenue\.[a-z]+', BouxAvenueGoblin),
    'brownie': (r'browniespain\.[a-z]+', BrownieGoblin),
    'burberry': (r'burberry\.[a-z]+', BurberryGoblin),
    'canda': (r'c-and-a\.[a-z]+', CAGoblin),
    'calvinklein': (r'calvinklein(eu)?(\.[a-z]+|/)', CalvinKleinGoblin),
    'caroswim': (r'caroswim\.[a-z]+', CaroSwimGoblin),
    'ceciliecopenhagen': (r'ceciliecopenhagen\.[a-z]+', CecilieGoblin),
    'dollskill': (r'dollskill\.[a-z]+', DollsKillGoblin),
    'doralarsen': (r'doralarsen\.[a-z]+', DoraLarsenGoblin),
    'else': (r'elselingerie\.[a-z]+', ElseGoblin),
    'esprit': (r'esprit\.[a-z]+', EspritGoblin),
    'etam': (r'etam\.[a-z]+', EtamGoblin),
    'fae': (r'fae.house\.[a-z]+', FaeGoblin),
    'fashionnova': (r'fashionnova\.[a-z]+', FashionNovaGoblin),
    'faithfullthebrand': (r'faithfullthebrand\.[a-z]+', FaithfullTheBrandGoblin),
    'fivedancewear': (r'fivedancewear\.[a-z]+', FiveDancewearGoblin),
    'fleurdumal': (r'fleurdumal\.[a-z]+', FleurDuMalGoblin),
    'flickr': (r'flickr\.[a-z]+', FlickrGoblin),
    'fredericks': (r'fredericks(\.[a-z]+|/)', FredericksGoblin),
    'forloveandlemons': (r'forloveandlemons\.[a-z]+', ForLoveAndLemonsGoblin),
    'fortnight': (r'fortnightlingerie\.[a-z]+', FortnightGoblin),
    'freepeople': (r'freepeople(\.[a-z]+|/)', FreePeopleGoblin),
    'generic': ('#####', OmegaGoblin),
    'getty': (r'gettyimages\.[a-z]+', GettyGoblin),
    'guess': (r'guess(-img)?', GuessGoblin),
    'handm': (r'hm\.[a-z]+', HMGoblin),
    'hannebloch': (r'hanne-bloch\.[a-z]+', HanneBlochGoblin),
    'hungry': ('#####', HungryGoblin),
    'hunkemoller': (r'hunkemoller\.[a-z]+', HunkemollerGoblin),
    'hottopic': (r'hottopic\.[a-z]+', HotTopicGoblin),
    'imagefap': (r'imagefap\.[a-z]+', ImageFapGoblin),
    'imgur': (r'imgur\.[a-z]+', ImgurGoblin),
    'instagram': (r'instagram\.[a-z]+', InstagramGoblin),
    'intimissimi': (r'intimissimi\.[a-z]+', IntimissimiGoblin),
    'iterator': (r'#\d+#', IteratorGoblin),
    'jennyfer': (r'jennyfer\.[a-z]+', JennyferGoblin),
    'katherinehamilton': (r'katherinehamilton\.[a-z]+', KatherineHamiltonGoblin),
    'kikidemontparnasse': (r'kikidm\.[a-z]+', KikiDeMontparnasseGoblin),
    'koton': (r'koton\.[a-z]+|ktnimg', KotonGoblin),
    'lepetittrou': (r'(le-petit-trou|shoplo)\.[a-z]+', LePetitTrouGoblin),
    'livy': (r'li-vy\.[a-z]+', LivyGoblin),
    'lounge': (r'loungeunderwear\.[a-z]+', LoungeGoblin),
    'maisonclose': (r'maison-close\.[a-z]+', MaisonCloseGoblin),
    'maisonlejaby': (r'maisonlejaby\.[a-z]+', MaisonLejabyGoblin),
    'mango': (r'mango\.[a-z]+|mngbcn', MangoGoblin),
    'marliesdekkers': (r'marliesdekkers\.[a-z]+', MarliesDekkersGoblin),
    'massimodutti': (r'massimodutti\.[a-z]+', MassimoDuttiGoblin),
    'missguided': (r'missguided(us)?\.[a-z]+', MissguidedGoblin),
    'nastygal': (r'nastygal\.[a-z]+', NastyGalGoblin),
    'only': (r'only\.[a-z]+', OnlyGoblin),
    'onlyhearts': (r'onlyhearts\.[a-z]+', OnlyHeartsGoblin),
    'oysho': (r'oysho\.[a-z]+', OyshoGoblin),
    'prettylittlething': (r'prettylittlething\.[a-z]+', PrettyLittleThingGoblin),
    'promise': ('tienda.promise', PromiseGoblin),
    'pullandbear': (r'pullandbear\.[a-z]+', PullandBearGoblin),
    'reserved': (r'reserved\.[a-z]+', ReservedGoblin),
    'sandro': (r'sandro-paris\.[a-z]+', SandroGoblin),
    'savagex': (r'savagex\.[a-z]+', SavageXGoblin),
    'shopbop': (r'shopbop(\.[a-z]+|/)', ShopbopGoblin),
    'simoneperele': (r'simone-?perele\.[a-z]+', SimonePereleGoblin),
    'skin': (r'skinworldwide\.[a-z]+', SkinGoblin),
    'springfield': (r'myspringfield\.[a-z]+', SpringfieldGoblin),
    'ssense': (r'ssense(media)?', SsenseGoblin),
    'stradivarius': (r'stradivarius\.[a-z]+', StradivariusGoblin),
    'tallyweijl': (r'tally-weijl\.[a-z]+', TallyWeijlGoblin),
    'tezenis': (r'(calzedonia|tezenis)\.[a-z]+', TezenisGoblin),
    'thegreateros': (r'thegreateros\.[a-z]+', TheGreatErosGoblin),
    'theiconic': (r'theiconic\.[a-z]+', TheIconicGoblin),
    'tommyhilfiger':(r'tommy-europe|shoptommy|tommy\.[a-z]+', TommyHilfigerGoblin),
    'tisjadamen': (r'tisjadamen\.[a-z]+', TisjaDamenGoblin),
    'topshop': (r'topshop\.[a-z]+', TopshopGoblin),
    'trendyol': (r'trendyol\.[a-z]+', TrendyolGoblin),
    'triangl': (r'triangl\.[a-z]+', TrianglGoblin),
    'underprotection': (r'underprotection\.[a-z]+', UnderprotectionGoblin),
    'urbanoutfitters':(r'urbanoutfitters(eu)?(\.[a-z]+|/)', UrbanOutfittersGoblin),
    'victoriassecret': (r'victoriassecret\.[a-z]+', VictoriasSecretGoblin),
    'vila': (r'vila\.[a-z]+', VilaGoblin),
    'vitamina': (r'vitaminaswim\.[a-z]+', VitaminAGoblin),
    'watercult': (r'watercult\.[a-z]+', WatercultGoblin),
    'wolford': (r'wolfordshop\.[a-z]+', WolfordGoblin),
    'womensecret': (r'womensecret\.[a-z]+', WomensSecretGoblin),
    'woodwood': (r'woodwood\.[a-z]+', WoodWoodGoblin),
    'yandy': (r'yandy(cdn)?\.[a-z]+', YandyGoblin),
    'yargici': (r'yargici\.[a-z]+', YargiciGoblin),
    'zalando': (r'zalando\.[a-z]+|ztat\.net|[A-Z0-9]+-[A-Z]\d{2}@\d', ZalandoGoblin),
    'zara': (r'zara\.[a-z]+', ZaraGoblin)
    }
