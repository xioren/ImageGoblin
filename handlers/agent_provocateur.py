from handlers.generic_alpha import AlphaGoblin


class AgentProvocateurGoblin(AlphaGoblin):

    def __init__(self, args):
        super().__init__(args)

    def __str__(self):
        return 'agent provocateur goblin'
