"""
Listas de Pokémon do jogador e do Giovanni.
Status = HP base e Ataque base (físico) de cada espécie, na forma normal
(sem Mega Evolução), conforme Bulbapedia / Pokémon Database.
O ataque especial só pode ser usado 1 vez por Pokémon.
"""
from game.utils.pokemon import Pokemon

PASTA_IMG = "img/pokemon/"
USOS_ESPECIAL = 1   # cada Pokémon só pode usar o especial 1 vez


# nome do poke, tipagem, arquivo da img, hp base e ataque base
def _p(nome, tipos, arquivo, hp, ataque):
    return Pokemon(nome, tipos, f"{PASTA_IMG}{arquivo}.png",
                    hp=hp, ataque=ataque, usos_especial=USOS_ESPECIAL)


OPCOES_JOGADOR = [
    #   nome          tipos                    img          HP   ATK
    _p("Snorlax",   ["normal"],               "snorlax",   160, 110),
    _p("Ho-Oh",     ["fogo", "voador"],       "ho-oh",     106, 130),
    _p("Greninja",  ["agua", "sombrio"],      "greninja",   72,  95),
    _p("Venusaur",  ["planta", "veneno"],     "venosaur",   80,  82),
    _p("Luxray",    ["eletrico"],             "luxray",     80, 120),
    _p("Regice",    ["gelo"],                 "regice",     80,  50),
    _p("Lucario",   ["lutador", "aco"],       "lucario",    70, 110),
    _p("Toxicroak", ["veneno", "lutador"],    "toxicroak",  83, 106),
    _p("Darkrai",   ["sombrio"],              "darkrai",    70,  90),
    _p("Groudon",   ["terra"],                "groudon",   100, 150),
    _p("Tyranitar", ["pedra", "sombrio"],     "tyranitar", 100, 134),
    _p("Dragonite", ["voador", "dragao"],     "dragonite",  91, 134),
    _p("Metagross", ["psiquico", "aco"],      "metagross",  80, 135),
    _p("Heracross", ["inseto", "lutador"],    "heracross",  80, 125),
    _p("Gengar",    ["fantasma", "veneno"],   "gengar",     60,  65),
    _p("Rayquaza",  ["dragao", "voador"],     "rayquaza",  105, 150),
]

OPCOES_GIOVANNI = [
    #   nome          tipos                    img          HP   ATK
    _p("Persian",   ["normal"],               "persian",    65,  70),
    _p("Moltres",   ["fogo", "voador"],       "moltres",    90, 100),
    _p("Lapras",    ["agua", "gelo"],         "lapras",    130,  85),
    _p("Exeggutor", ["planta", "psiquico"],   "exeggutor",  95,  95),
    _p("Zapdos",    ["eletrico", "voador"],   "zapdos",     90,  90),
    _p("Articuno",  ["gelo", "voador"],       "articuno",   90,  85),
    _p("Machamp",   ["lutador"],              "machamp",    90, 130),
    _p("Nidoking",  ["veneno", "terra"],      "nidoking",   81, 102),
    _p("Umbreon",   ["sombrio"],              "umbreon",    95,  65),
    _p("Regirock",  ["pedra"],                "regirock",   80, 100),
    _p("Rhyperior", ["pedra", "terra"],       "rhyperior", 115, 140),
    _p("Latios",    ["dragao", "psiquico"],   "latios",     80,  90),
    _p("Mewtwo",    ["psiquico"],             "mewtwo",    106, 110),
    _p("Scizor",    ["inseto", "aco"],        "scizor",     70, 130),
    _p("Sableye",   ["sombrio", "fantasma"],  "sableye",     50,  75),
    _p("Garchomp",  ["dragao", "terra"],      "garchomp",  108, 130),
]
