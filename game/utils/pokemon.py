"""
pokemon.py
Classe Pokemon: nome, tipos e imagem (pixel art). HP e ataque são opcionais.
"""
import random

from game.utils.tipos import multiplicador_tipo


class Pokemon:
    _CACHE_IMAGENS = {}   # compartilhado: cada imagem é carregada só uma vez

    def __init__(self, nome, tipos, img, hp, ataque, usos_especial=1):
        self.nome = nome
        self.tipos = tipos                  # lista; tipos[0] é o tipo do golpe
        self.img = img                      # caminho do arquivo da imagem
        self.hp_max = hp
        self.hp = hp
        self.ataque = ataque
        self.usos_especial_max = usos_especial
        self.usos_especial = usos_especial

    # ---------------- estado ----------------
    @property
    def vivo(self):
        return self.hp > 0

    @property
    def tipo_principal(self):
        return self.tipos[0]

    # ---------------- combate ----------------
    def atacar(self, alvo, especial=False):
        """Ataca o alvo. Devolve (dano, multiplicador) para a interface exibir."""
        if especial and self.usos_especial <= 0:
            especial = False                # sem usos: vira ataque normal
        base = 0.55 if especial else 0.30
        mult = multiplicador_tipo(self.tipo_principal, alvo.tipos)
        dano = round(self.ataque * base * mult * random.uniform(0.85, 1.0))
        if mult > 0:
            dano = max(1, dano)
        if especial:
            self.usos_especial -= 1
        alvo.receber_dano(dano)
        return dano, mult

    def receber_dano(self, dano):
        self.hp = max(0, self.hp - dano)

    # ---------------- imagem (pygame) ----------------
    def carregar_imagem(self, tamanho=(160, 160), espelhar=False):
        """Surface do pygame, já redimensionada sem borrar a pixel art.
        espelhar=True serve para o Pokémon do jogador (de costas)."""
        import pygame                       # import aqui: a lógica roda sem pygame
        chave = (self.img, tamanho, espelhar)
        if chave not in Pokemon._CACHE_IMAGENS:
            original = pygame.image.load(self.img).convert_alpha()
            # encaixa dentro da caixa sem distorcer (mantém a proporção)
            escala = min(tamanho[0] / original.get_width(),
                        tamanho[1] / original.get_height())
            novo = (max(1, round(original.get_width() * escala)),
                    max(1, round(original.get_height() * escala)))
            redim = pygame.transform.scale(original, novo)  # sem suavização
            # coloca numa caixa transparente: centralizado e com os "pés" embaixo
            surf = pygame.Surface(tamanho, pygame.SRCALPHA)
            surf.blit(redim, ((tamanho[0] - novo[0]) // 2, tamanho[1] - novo[1]))
            if espelhar:
                surf = pygame.transform.flip(surf, True, False)
            Pokemon._CACHE_IMAGENS[chave] = surf
        return Pokemon._CACHE_IMAGENS[chave]

    # ---------------- utilidades ----------------
    def copia(self):
        """Pokémon novo, com HP e especial cheios (uma cópia por partida)."""
        return Pokemon(self.nome, list(self.tipos), self.img,
                        self.hp_max, self.ataque, self.usos_especial_max)

    def __repr__(self):
        return f"{self.nome} {self.hp}/{self.hp_max}"
