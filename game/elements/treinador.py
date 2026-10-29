"""
treinador.py
Classe base com o que o Jogador e o Giovanni têm em comum.
"""


class Treinador:
    TAMANHO_TIME = 3

    def __init__(self, nome):
        self.nome = nome
        self.time = []
        self.indice_ativo = 0

    @property
    def ativo(self):
        return self.time[self.indice_ativo]

    def tem_pokemon_vivo(self):
        return any(p.vivo for p in self.time)

    def proximo_vivo(self):
        """Índice do primeiro Pokémon vivo, ou None se todos desmaiaram."""
        for i, p in enumerate(self.time):
            if p.vivo:
                return i
        return None

    def trocar(self, indice):
        """Troca o Pokémon ativo. Devolve True se a troca foi possível."""
        if 0 <= indice < len(self.time) and self.time[indice].vivo:
            self.indice_ativo = indice
            return True
        return False
