from handlers.generic_alpha import AlphaGoblin


class AgentProvocateurGoblin(AlphaGoblin):

    def __init__(self, url, mode, timeout, format, increment, nodl, verbose, tickrate):
        super().__init__(url, mode, timeout, format, increment, nodl, verbose, tickrate)
        print(f'[{self.__str__()}] <deployed>')

    def __str__(self):
        return 'agent provocateur goblin'
