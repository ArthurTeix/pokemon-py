"""
engine.py
Monta e roda o jogo: menu -> (sobre) | cadastro -> seleção -> batalha -> fim.
Fica em game/engine.py e é chamado pelo main.py.
"""
import pygame

from game.elements.jogador import Jogador
from game.elements.giovanni import Giovanni
from game.utils.dados_pokemon import OPCOES_JOGADOR, OPCOES_GIOVANNI

LARGURA, ALTURA, FPS = 960, 640, 60
TITULO = "Mestre Pokémon vs Giovanni"
PASTA_PERSONAGENS = "img/personagens/"   # cleyton.png e giovanni.png

# ---------------------------------------------------------------- cores
FUNDO = (223, 233, 200)
PAINEL = (255, 253, 240)
BORDA = (34, 34, 34)
TEXTO = (34, 34, 34)
BRANCO = (255, 255, 255)
BTN = (232, 66, 63)
BTN_HOVER = (255, 106, 95)
BTN_OFF = (176, 176, 160)
AMARELO = (255, 216, 74)
CHAO = (180, 200, 150)

CORES_TIPO = {
    "normal": "#a8a878", "fogo": "#f08030", "agua": "#6890f0",
    "eletrico": "#d8b010", "planta": "#78c850", "gelo": "#98d8d8",
    "lutador": "#c03028", "veneno": "#a040a0", "terra": "#c0a048",
    "voador": "#a890f0", "psiquico": "#f85888", "inseto": "#a8b820",
    "pedra": "#b8a038", "fantasma": "#705898", "dragao": "#7038f8",
    "sombrio": "#705848", "aco": "#b8b8d0",
}
NOMES_TIPO = {
    "agua": "Água", "eletrico": "Elétrico", "psiquico": "Psíquico",
    "dragao": "Dragão", "aco": "Aço",
}


def cor_tipo(tipo):
    return pygame.Color(CORES_TIPO.get(tipo, "#888888"))


def nome_tipo(tipo):
    return NOMES_TIPO.get(tipo, tipo.capitalize())


def efetividade(mult):
    if mult == 0:
        return "Não afeta..."
    if mult > 1:
        return "É super efetivo!"
    if mult < 1:
        return "Não é muito efetivo..."
    return ""


# ---------------------------------------------------------------- UI
class SairDoJogo(Exception):
    """Levantada quando o jogador fecha a janela."""


class UI:
    """Janela, fontes e funções de desenho usadas por todas as telas."""

    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        fam = "couriernew,courier,dejavusansmono,monospace"
        self.f_g = pygame.font.SysFont(fam, 36, bold=True)
        self.f_m = pygame.font.SysFont(fam, 22, bold=True)
        self.f_p = pygame.font.SysFont(fam, 16, bold=True)
        self.f_xs = pygame.font.SysFont(fam, 12, bold=True)
        self._cache_img = {}

    # ---- laço básico ----
    def eventos(self):
        lista = pygame.event.get()
        for e in lista:
            if e.type == pygame.QUIT:
                raise SairDoJogo
        return lista

    def quadro(self):
        pygame.display.flip()
        self.clock.tick(FPS)

    def esperar(self, ms, desenhar):
        """Mostra a tela por 'ms' milissegundos (sem travar a janela)."""
        fim = pygame.time.get_ticks() + ms
        while pygame.time.get_ticks() < fim:
            self.eventos()
            desenhar()
            self.quadro()

    # ---- desenho ----
    def texto(self, txt, fonte, cor, pos, centro=False):
        surf = fonte.render(txt, True, cor)
        rect = surf.get_rect()
        if centro:
            rect.center = pos
        else:
            rect.topleft = pos
        self.tela.blit(surf, rect)
        return rect

    def texto_multilinha(self, txt, fonte, cor, rect, espaco=4):
        linha, y = "", rect.y
        for palavra in txt.split(" "):
            teste = (linha + " " + palavra).strip()
            if fonte.size(teste)[0] > rect.width and linha:
                self.texto(linha, fonte, cor, (rect.x, y))
                y += fonte.get_linesize() + espaco
                linha = palavra
            else:
                linha = teste
        if linha:
            self.texto(linha, fonte, cor, (rect.x, y))

    def caixa(self, rect, cor=PAINEL, borda=BORDA):
        pygame.draw.rect(self.tela, cor, rect, border_radius=8)
        pygame.draw.rect(self.tela, borda, rect, 3, border_radius=8)

    def botao(self, rect, txt, ativo=True, fonte=None, sub=None, destaque=False):
        fonte = fonte or self.f_m
        mouse = pygame.mouse.get_pos()
        if not ativo:
            cor = BTN_OFF
        elif rect.collidepoint(mouse):
            cor = BTN_HOVER
        else:
            cor = BTN
        pygame.draw.rect(self.tela, cor, rect, border_radius=8)
        pygame.draw.rect(self.tela, AMARELO if destaque else BORDA, rect, 3, border_radius=8)
        if sub:
            self.texto(txt, fonte, BRANCO, (rect.centerx, rect.centery - 10), True)
            self.texto(sub, self.f_xs, BRANCO, (rect.centerx, rect.centery + 12), True)
        else:
            self.texto(txt, fonte, BRANCO, rect.center, True)

    def tags_tipos(self, tipos, x, y):
        for t in tipos:
            surf = self.f_xs.render(nome_tipo(t), True, BRANCO)
            r = pygame.Rect(x, y, surf.get_width() + 8, surf.get_height() + 4)
            pygame.draw.rect(self.tela, cor_tipo(t), r, border_radius=4)
            pygame.draw.rect(self.tela, BORDA, r, 1, border_radius=4)
            self.tela.blit(surf, (x + 4, y + 2))
            x += r.width + 4

    def barra_hp(self, x, y, w, hp, hp_max):
        pygame.draw.rect(self.tela, (90, 90, 90), (x, y, w, 12), border_radius=6)
        frac = hp / hp_max if hp_max else 0
        cor = (59, 181, 74) if frac > 0.5 else (240, 200, 40) if frac > 0.2 else (220, 60, 50)
        if hp > 0:
            pygame.draw.rect(self.tela, cor, (x, y, max(4, int(w * frac)), 12), border_radius=6)
        pygame.draw.rect(self.tela, BORDA, (x, y, w, 12), 2, border_radius=6)

    # ---- imagens dos Pokémon (com plano B se a imagem não existir) ----
    def imagem(self, pokemon, tamanho, espelhar=False):
        chave = (pokemon.nome, tamanho, espelhar)
        if chave not in self._cache_img:
            try:
                surf = pokemon.carregar_imagem(tamanho, espelhar)
            except (FileNotFoundError, pygame.error):
                surf = self._placeholder(pokemon, tamanho)
            self._cache_img[chave] = surf
        return self._cache_img[chave]

    def _placeholder(self, pokemon, tamanho):
        surf = pygame.Surface(tamanho, pygame.SRCALPHA)
        r = surf.get_rect().inflate(-4, -4)
        pygame.draw.rect(surf, cor_tipo(pokemon.tipo_principal), r, border_radius=10)
        pygame.draw.rect(surf, BORDA, r, 2, border_radius=10)
        if tamanho[0] < 60:
            linhas = [(pokemon.nome[:3].upper(), self.f_xs)]
        elif tamanho[0] < 150:
            linhas = [(pokemon.nome, self.f_xs), ("sem imagem", self.f_xs)]
        else:
            linhas = [(pokemon.nome, self.f_p), ("sem imagem", self.f_xs)]
        for i, (linha, fonte) in enumerate(linhas):
            t = fonte.render(linha, True, BRANCO)
            y = tamanho[1] // 2 + i * 16 - (8 if len(linhas) > 1 else 0)
            surf.blit(t, t.get_rect(center=(tamanho[0] // 2, y)))
        return surf

    # ---- personagens em pixel art (cleyton.png / giovanni.png) ----
    def personagem(self, arquivo, altura):
        """Imagem do personagem na altura pedida (mantém a proporção).
        Devolve None se o arquivo não existir."""
        chave = ("personagem", arquivo, altura)
        if chave not in self._cache_img:
            try:
                orig = pygame.image.load(f"{PASTA_PERSONAGENS}{arquivo}.png").convert_alpha()
                escala = altura / orig.get_height()
                novo = (max(1, round(orig.get_width() * escala)), altura)
                if escala < 1:
                    surf = pygame.transform.smoothscale(orig, novo)
                else:
                    surf = pygame.transform.scale(orig, novo)
            except (FileNotFoundError, pygame.error):
                surf = None
            self._cache_img[chave] = surf
        return self._cache_img[chave]

    def blit_personagem(self, arquivo, altura, x, base_y, alinhar="esq"):
        """Desenha o personagem com os pés em base_y.
        alinhar='esq': x é a borda esquerda; 'dir': x é a borda direita."""
        surf = self.personagem(arquivo, altura)
        if surf is None:
            return
        px = x if alinhar == "esq" else x - surf.get_width()
        self.tela.blit(surf, (px, base_y - surf.get_height()))

    def personagens_laterais(self, altura):
        """Cleyton na esquerda e Giovanni na direita (menu e fim de jogo)."""
        self.blit_personagem("cleyton", altura, 30, ALTURA - 20, "esq")
        self.blit_personagem("giovanni", altura, LARGURA - 30, ALTURA - 20, "dir")


# ---------------------------------------------------------------- TELA: menu
def tela_menu(ui):
    """Devolve 'jogar', 'sobre' ou 'sair'."""
    x = LARGURA // 2 - 150
    botoes = [("jogar", "Jogar", pygame.Rect(x, 290, 300, 60)),
                ("sobre", "Sobre", pygame.Rect(x, 370, 300, 60)),
                ("sair", "Sair", pygame.Rect(x, 450, 300, 60))]

    while True:
        for e in ui.eventos():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for chave, _, r in botoes:
                    if r.collidepoint(e.pos):
                        return chave

        ui.tela.fill(FUNDO)
        ui.personagens_laterais(460)
        ui.texto("MESTRE POKÉMON", ui.f_g, TEXTO, (LARGURA // 2, 110), True)
        ui.texto("vs", ui.f_m, TEXTO, (LARGURA // 2, 160), True)
        ui.texto("GIOVANNI", ui.f_g, (200, 30, 30), (LARGURA // 2, 210), True)
        for _, txt, r in botoes:
            ui.botao(r, txt)
        ui.quadro()


# ---------------------------------------------------------------- TELA: sobre
RESUMO = ("Jogo criado para a disciplina Princípios de Programação de Sistemas de "
          "Informação, da UFRPE. Escolha 3 Pokémon e enfrente o Giovanni, líder da "
          "Equipe Rocket, em batalhas por turnos com vantagens e desvantagens de tipo. "
          "Cada Pokémon pode usar o ataque especial apenas 1 vez. Os 3 Pokémon do "
          "Giovanni são sorteados entre os da tabela dele.")
TAB_LARG, TAB_ALT, TAB_COLS, TAB_CAB = 115, 80, 4, 28


def desenhar_tabela(ui, titulo, lista, x, y):
    """Tabela 4x4 com a imagem e o nome de cada Pokémon."""
    larg_total = TAB_LARG * TAB_COLS
    linhas = (len(lista) + TAB_COLS - 1) // TAB_COLS
    cab = pygame.Rect(x, y, larg_total, TAB_CAB)
    pygame.draw.rect(ui.tela, AMARELO, cab)
    ui.texto(titulo, ui.f_p, TEXTO, cab.center, True)

    for i, p in enumerate(lista):
        lin, col = divmod(i, TAB_COLS)
        r = pygame.Rect(x + col * TAB_LARG, y + TAB_CAB + lin * TAB_ALT, TAB_LARG, TAB_ALT)
        pygame.draw.rect(ui.tela, PAINEL, r)
        pygame.draw.rect(ui.tela, BORDA, r, 1)
        ui.tela.blit(ui.imagem(p, (48, 48)), (r.centerx - 24, r.y + 5))
        ui.texto(p.nome, ui.f_xs, TEXTO, (r.centerx, r.y + 64), True)

    pygame.draw.rect(ui.tela, BORDA, (x, y, larg_total, TAB_CAB + linhas * TAB_ALT), 3)


def tela_sobre(ui):
    voltar = pygame.Rect(LARGURA // 2 - 120, 568, 240, 46)

    while True:
        for e in ui.eventos():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if voltar.collidepoint(e.pos):
                    return

        ui.tela.fill(FUNDO)
        ui.texto("SOBRE O JOGO", ui.f_m, TEXTO, (LARGURA // 2, 28), True)
        ui.texto_multilinha(RESUMO, ui.f_p, TEXTO, pygame.Rect(40, 56, LARGURA - 80, 110))
        desenhar_tabela(ui, "Pokémon do jogador", OPCOES_JOGADOR, 15, 180)
        desenhar_tabela(ui, "Pokémon do Giovanni", OPCOES_GIOVANNI, 485, 180)
        ui.botao(voltar, "Voltar", fonte=ui.f_p)
        ui.quadro()


# ---------------------------------------------------------------- TELA: cadastro
def tela_cadastro(ui):
    """Devolve o nome digitado, ou None se o jogador voltar ao menu."""
    nome = ""
    continuar = pygame.Rect(LARGURA // 2 - 140, 420, 280, 56)
    voltar = pygame.Rect(LARGURA // 2 - 140, 490, 280, 46)
    caixa_nome = pygame.Rect(LARGURA // 2 - 220, 310, 440, 56)

    while True:
        for e in ui.eventos():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if Jogador.nome_valido(nome):
                        return nome.strip()
                elif (e.unicode and e.unicode.isprintable()
                    and len(nome) < Jogador.TAMANHO_MAX_NOME):
                    nome += e.unicode
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if continuar.collidepoint(e.pos) and Jogador.nome_valido(nome):
                    return nome.strip()
                if voltar.collidepoint(e.pos):
                    return None

        ui.tela.fill(FUNDO)
        ui.texto("MESTRE POKÉMON", ui.f_g, TEXTO, (LARGURA // 2, 120), True)
        ui.texto("vs", ui.f_m, TEXTO, (LARGURA // 2, 170), True)
        ui.texto("GIOVANNI", ui.f_g, (200, 30, 30), (LARGURA // 2, 220), True)
        ui.texto("Cadastro do jogador - digite seu nome:", ui.f_p, TEXTO,
                 (LARGURA // 2, 285), True)
        ui.caixa(caixa_nome)
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        ui.texto(nome + cursor, ui.f_m, TEXTO, (caixa_nome.x + 16, caixa_nome.y + 15))
        ui.botao(continuar, "Continuar", Jogador.nome_valido(nome))
        ui.botao(voltar, "Voltar", fonte=ui.f_p)
        ui.quadro()


# TELA: seleção
COLUNAS, CARTA_W, CARTA_H, GAP_X, GAP_Y = 4, 222, 116, 8, 6
BOTAO_LUTAR = pygame.Rect(LARGURA // 2 - 160, 574, 320, 52)
BOTAO_VOLTAR = pygame.Rect(24, 574, 140, 52)


def retangulos_cartas(qtd):
    x0 = (LARGURA - (COLUNAS * CARTA_W + (COLUNAS - 1) * GAP_X)) // 2
    rects = []
    for i in range(qtd):
        lin, col = divmod(i, COLUNAS)
        rects.append(pygame.Rect(x0 + col * (CARTA_W + GAP_X),
                                 62 + lin * (CARTA_H + GAP_Y), CARTA_W, CARTA_H))
    return rects


def tela_selecao(ui, jogador):
    """True se o time foi confirmado, False se o jogador voltou ao menu."""
    cartas = retangulos_cartas(len(jogador.disponiveis))

    while True:
        for e in ui.eventos():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for i, r in enumerate(cartas):
                    if r.collidepoint(e.pos):
                        jogador.alternar_selecao(i)
                if BOTAO_VOLTAR.collidepoint(e.pos):
                    return False
                if BOTAO_LUTAR.collidepoint(e.pos) and jogador.selecao_completa():
                    jogador.confirmar_time()
                    return True

        ui.tela.fill(FUNDO)
        ui.texto(f"{jogador.nome}, escolha {jogador.TAMANHO_TIME} Pokémon "
                f"({len(jogador.selecionados)}/{jogador.TAMANHO_TIME})",
                ui.f_m, TEXTO, (LARGURA // 2, 32), True)

        mouse = pygame.mouse.get_pos()
        for i, (r, p) in enumerate(zip(cartas, jogador.disponiveis)):
            marcado = i in jogador.selecionados
            cor = AMARELO if marcado else (255, 245, 200) if r.collidepoint(mouse) else PAINEL
            ui.caixa(r, cor)
            ui.tela.blit(ui.imagem(p, (80, 80)), (r.x + 6, r.y + 18))
            ui.texto(p.nome, ui.f_p, TEXTO, (r.x + 92, r.y + 8))
            ui.tags_tipos(p.tipos, r.x + 92, r.y + 32)
            ui.texto(f"HP  {p.hp_max}", ui.f_p, TEXTO, (r.x + 92, r.y + 58))
            ui.texto(f"ATK {p.ataque}", ui.f_p, TEXTO, (r.x + 92, r.y + 78))
            if marcado:
                ordem = jogador.selecionados.index(i) + 1
                ui.texto(str(ordem), ui.f_m, (200, 30, 30), (r.right - 22, r.y + 8))

        ui.botao(BOTAO_VOLTAR, "Voltar", fonte=ui.f_p)
        ui.botao(BOTAO_LUTAR, "Lutar contra Giovanni!", jogador.selecao_completa(),
                fonte=ui.f_p)
        ui.quadro()


# ---------------------------------------------------------------- TELA: batalha
BOTAO_ATAQUE = pygame.Rect(520, 470, 205, 50)
BOTAO_ESPECIAL = pygame.Rect(735, 470, 205, 50)
BOTOES_TIME = [pygame.Rect(520 + i * 142, 530, 134, 90) for i in range(3)]


def desenhar_batalha(ui, jogador, giovanni, msg, modo):
    """modo: None (só mostra) | 'normal' (turno do jogador) | 'forcado' (trocar)."""
    foe, eu = giovanni.ativo, jogador.ativo
    ui.tela.fill(FUNDO)

    # lado do Giovanni (em cima, à direita): Pokémon e treinador parado ao lado
    pygame.draw.ellipse(ui.tela, CHAO, (620, 207, 200, 36))
    pygame.draw.ellipse(ui.tela, CHAO, (825, 212, 120, 28))
    ui.tela.blit(ui.imagem(foe, (180, 180)), (630, 45))
    ui.blit_personagem("giovanni", 200, LARGURA - 25, 225, "dir")

    # lado do jogador (embaixo, à esquerda): treinador parado ao lado do Pokémon
    pygame.draw.ellipse(ui.tela, CHAO, (20, 438, 135, 26))
    pygame.draw.ellipse(ui.tela, CHAO, (140, 432, 230, 36))
    ui.blit_personagem("cleyton", 230, 30, 450, "esq")
    ui.tela.blit(ui.imagem(eu, (210, 210), True), (150, 240))

    # info do Giovanni
    ui.caixa(pygame.Rect(30, 40, 430, 100))
    ui.texto(f"Giovanni · {foe.nome}", ui.f_m, TEXTO, (46, 50))
    ui.tags_tipos(foe.tipos, 46, 82)
    ui.barra_hp(46, 104, 398, foe.hp, foe.hp_max)
    vivos = sum(1 for p in giovanni.time if p.vivo)
    ui.texto(f"{foe.hp}/{foe.hp_max}  ·  restam {vivos}/{len(giovanni.time)}",
            ui.f_xs, TEXTO, (46, 120))

    # info do jogador
    ui.caixa(pygame.Rect(500, 310, 430, 100))
    ui.texto(f"{jogador.nome} · {eu.nome}", ui.f_m, TEXTO, (516, 320))
    ui.tags_tipos(eu.tipos, 516, 352)
    ui.barra_hp(516, 374, 398, eu.hp, eu.hp_max)
    ui.texto(f"{eu.hp}/{eu.hp_max}  ·  especial {eu.usos_especial}/{eu.usos_especial_max}",
            ui.f_xs, TEXTO, (516, 390))

    # mensagem
    caixa_msg = pygame.Rect(20, 470, 480, 150)
    ui.caixa(caixa_msg)
    ui.texto_multilinha(msg, ui.f_m, TEXTO, caixa_msg.inflate(-30, -24))

    # botões
    normal = modo == "normal"
    ui.botao(BOTAO_ATAQUE, "Atacar", normal)
    ui.botao(BOTAO_ESPECIAL, f"Especial ({eu.usos_especial})",
            normal and eu.usos_especial > 0)
    for i, p in enumerate(jogador.time):
        pode = modo in ("normal", "forcado") and p.vivo and i != jogador.indice_ativo
        ui.botao(BOTOES_TIME[i], p.nome, pode, fonte=ui.f_p,
                sub=f"{p.hp}/{p.hp_max}", destaque=(i == jogador.indice_ativo))


def turno_ataque(atacante, alvo, especial):
    """Executa um ataque entre dois treinadores e devolve o texto para a tela."""
    a, d = atacante.ativo, alvo.ativo
    usos_antes = a.usos_especial
    dano, mult = a.atacar(d, especial)
    tipo_golpe = "ataque especial" if a.usos_especial < usos_antes else "ataque"
    texto = f"{a.nome} usou {tipo_golpe} ({a.tipo_principal})! Causou {dano} de dano."
    return f"{texto} {efetividade(mult)}".strip()


def tela_batalha(ui, jogador, giovanni):
    """Roda a luta. Devolve True se o jogador venceu, False se perdeu."""
    estado = {"msg": ""}

    def desenhar(modo=None):
        desenhar_batalha(ui, jogador, giovanni, estado["msg"], modo)

    def dizer(texto, ms=1400):
        estado["msg"] = texto
        ui.esperar(ms, desenhar)

    def escolher(modo):
        """Espera o clique do jogador. Devolve ('ataque'|'especial'|'trocar', indice)."""
        while True:
            for e in ui.eventos():
                if e.type != pygame.MOUSEBUTTONDOWN or e.button != 1:
                    continue
                if modo == "normal":
                    if BOTAO_ATAQUE.collidepoint(e.pos):
                        return "ataque", None
                    if (BOTAO_ESPECIAL.collidepoint(e.pos)
                            and jogador.ativo.usos_especial > 0):
                        return "especial", None
                for i, r in enumerate(BOTOES_TIME[:len(jogador.time)]):
                    p = jogador.time[i]
                    if r.collidepoint(e.pos) and p.vivo and i != jogador.indice_ativo:
                        return "trocar", i
            desenhar(modo)
            ui.quadro()

    dizer(f"Giovanni quer lutar! Ele envia {giovanni.ativo.nome}!")
    dizer(f"Vai, {jogador.ativo.nome}!", 1000)

    while True:
        # ---------- turno do jogador ----------
        estado["msg"] = f"O que {jogador.ativo.nome} vai fazer?"
        acao, idx = escolher("normal")

        if acao == "trocar":
            jogador.trocar(idx)
            dizer(f"Você trocou para {jogador.ativo.nome}!", 1000)
        else:
            dizer(turno_ataque(jogador, giovanni, acao == "especial"))
            if not giovanni.ativo.vivo:
                dizer(f"{giovanni.ativo.nome} desmaiou!", 1100)
                if giovanni.enviar_proximo() is None:
                    return True
                dizer(f"Giovanni envia {giovanni.ativo.nome}!", 1100)
                continue

        # turno do Giovanni
        especial = giovanni.escolher_acao() == "especial"

        dizer("Giovanni: " + turno_ataque(giovanni, jogador, especial))
        if not jogador.ativo.vivo:
            dizer(f"{jogador.ativo.nome} desmaiou!", 1100)
            if jogador.proximo_vivo() is None:
                return False
            estado["msg"] = "Escolha o próximo Pokémon!"
            _, idx = escolher("forcado")
            jogador.trocar(idx)
            dizer(f"Vai, {jogador.ativo.nome}!", 1000)


# TELA: fim
def tela_fim(ui, venceu, jogador, giovanni):
    """Devolve 'novamente', 'menu' ou 'sair'."""
    x = LARGURA // 2 - 180

    botoes = [("novamente", "Jogar de novo", pygame.Rect(x, 400, 360, 56)),
                ("menu", "Voltar ao menu", pygame.Rect(x, 470, 360, 56)),
                ("sair", "Sair", pygame.Rect(x, 540, 360, 56))]

    while True:
        for e in ui.eventos():
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for chave, _, r in botoes:
                    if r.collidepoint(e.pos):
                        return chave

        ui.tela.fill(FUNDO)
        ui.personagens_laterais(320)
        if venceu:
            ui.texto("VITÓRIA!", ui.f_g, (30, 140, 50), (LARGURA // 2, 130), True)
            frase = f"{jogador.nome} derrotou Giovanni e acabou com a Equipe Rocket!"
        else:
            ui.texto("DERROTA...", ui.f_g, (200, 30, 30), (LARGURA // 2, 130), True)
            frase = f"Giovanni venceu desta vez, {jogador.nome}. Tente outro time!"
        ui.texto(frase, ui.f_p, TEXTO, (LARGURA // 2, 195), True)

        ui.texto("Seu time:", ui.f_p, TEXTO, (LARGURA // 2, 245), True)
        ui.texto(", ".join(f"{p.nome} {p.hp}/{p.hp_max}" for p in jogador.time),
                 ui.f_xs, TEXTO, (LARGURA // 2, 270), True)
        ui.texto("Time do Giovanni:", ui.f_p, TEXTO, (LARGURA // 2, 315), True)
        ui.texto(", ".join(f"{p.nome} {p.hp}/{p.hp_max}" for p in giovanni.time),
                 ui.f_xs, TEXTO, (LARGURA // 2, 340), True)

        for _, txt, r in botoes:
            ui.botao(r, txt)
        ui.quadro()


# função principal
def jogar_partidas(ui, nome):
    """Seleção -> batalha -> fim, repetindo enquanto o jogador quiser."""
    while True:
        jogador = Jogador(nome, OPCOES_JOGADOR)
        if not tela_selecao(ui, jogador):
            return "menu"

        giovanni = Giovanni(OPCOES_GIOVANNI)
        venceu = tela_batalha(ui, jogador, giovanni)
        resposta = tela_fim(ui, venceu, jogador, giovanni)

        if resposta != "novamente":
            return resposta


def jogo():
    ui = UI()
    nome = None
    try:
        while True:
            escolha = tela_menu(ui)

            if escolha == "sair":
                break

            if escolha == "sobre":
                tela_sobre(ui)
                continue
            
            if nome is None:
                nome = tela_cadastro(ui)
                if nome is None:
                    continue

            if jogar_partidas(ui, nome) == "sair":
                break
    except SairDoJogo:
        pass
    finally:
        pygame.quit()
