"""
jogador.py
Classe Jogador: cadastro (nome) e escolha de 3 Pokémon entre os disponíveis.
"""
from game.elements.treinador import Treinador


class Jogador(Treinador):
    TAMANHO_MAX_NOME = 14

    def __init__(self, nome, pokemons_disponiveis):
        super().__init__(nome.strip()[:self.TAMANHO_MAX_NOME])
        self.disponiveis = pokemons_disponiveis
        self.selecionados = []              # índices marcados na tela de seleção

    @staticmethod
    def nome_valido(nome):
        return len(nome.strip()) > 0

    # ---- usado pela tela de seleção (clicar marca/desmarca) ----
    def alternar_selecao(self, indice):
        if indice in self.selecionados:
            self.selecionados.remove(indice)
        elif len(self.selecionados) < self.TAMANHO_TIME:
            self.selecionados.append(indice)

    def selecao_completa(self):
        return len(self.selecionados) == self.TAMANHO_TIME

    def confirmar_time(self):
        """Monta o time com cópias novas dos Pokémon marcados."""
        if not self.selecao_completa():
            return False
        self.time = [self.disponiveis[i].copia() for i in self.selecionados]
        self.indice_ativo = 0
        return True
