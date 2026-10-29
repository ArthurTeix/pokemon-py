"""
giovanni.py
Classe Giovanni: sorteia 3 Pokémon entre as opções e escolhe as ações da luta.
"""
import random

from game.elements.treinador import Treinador


class Giovanni(Treinador):
    CHANCE_ESPECIAL = 0.30

    def __init__(self, pokemons_disponiveis):
        super().__init__("Giovanni")
        self.disponiveis = pokemons_disponiveis
        self.sortear_time()

    def sortear_time(self):
        """3 Pokémon aleatórios, sem repetir."""
        escolhidos = random.sample(self.disponiveis, self.TAMANHO_TIME)
        self.time = [p.copia() for p in escolhidos]
        self.indice_ativo = 0

    def escolher_acao(self):
        """IA simples: às vezes usa o especial, se ainda tiver usos."""
        if self.ativo.usos_especial > 0 and random.random() < self.CHANCE_ESPECIAL:
            return "especial"
        return "ataque"

    def enviar_proximo(self):
        """Quando o ativo desmaia: devolve o próximo Pokémon, ou None se acabou."""
        i = self.proximo_vivo()
        if i is None:
            return None
        self.indice_ativo = i
        return self.ativo
