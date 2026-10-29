"""
tipos.py
Tabela de vantagens de tipos (atacante -> defensor -> multiplicador).
Tipo que não aparece = dano normal (x1). Tipo de Fada não incluído (nenhum
Pokémon da lista usa).
"""

TABELA_TIPOS = {
    "normal":   {"pedra": 0.5, "aco": 0.5, "fantasma": 0},
    "fogo":     {"planta": 2, "gelo": 2, "inseto": 2, "aco": 2,
                "fogo": 0.5, "agua": 0.5, "pedra": 0.5, "dragao": 0.5},
    "agua":     {"fogo": 2, "terra": 2, "pedra": 2,
                "agua": 0.5, "planta": 0.5, "dragao": 0.5},
    "eletrico": {"agua": 2, "voador": 2,
                "eletrico": 0.5, "planta": 0.5, "dragao": 0.5, "terra": 0},
    "planta":   {"agua": 2, "terra": 2, "pedra": 2,
                "fogo": 0.5, "planta": 0.5, "veneno": 0.5, "voador": 0.5,
                "inseto": 0.5, "dragao": 0.5, "aco": 0.5},
    "gelo":     {"planta": 2, "terra": 2, "voador": 2, "dragao": 2,
                "fogo": 0.5, "agua": 0.5, "gelo": 0.5, "aco": 0.5},
    "lutador":  {"normal": 2, "gelo": 2, "pedra": 2, "sombrio": 2, "aco": 2,
                "veneno": 0.5, "voador": 0.5, "psiquico": 0.5, "inseto": 0.5,
                "fantasma": 0},
    "veneno":   {"planta": 2,
                "veneno": 0.5, "terra": 0.5, "pedra": 0.5, "fantasma": 0.5,
                "aco": 0},
    "terra":    {"fogo": 2, "eletrico": 2, "veneno": 2, "pedra": 2, "aco": 2,
                "planta": 0.5, "inseto": 0.5, "voador": 0},
    "voador":   {"planta": 2, "lutador": 2, "inseto": 2,
                "eletrico": 0.5, "pedra": 0.5, "aco": 0.5},
    "psiquico": {"lutador": 2, "veneno": 2,
                "psiquico": 0.5, "aco": 0.5, "sombrio": 0},
    "inseto":   {"planta": 2, "psiquico": 2, "sombrio": 2,
                "fogo": 0.5, "lutador": 0.5, "veneno": 0.5, "voador": 0.5,
                "fantasma": 0.5, "aco": 0.5},
    "pedra":    {"fogo": 2, "gelo": 2, "voador": 2, "inseto": 2,
                "lutador": 0.5, "terra": 0.5, "aco": 0.5},
    "fantasma": {"psiquico": 2, "fantasma": 2, "sombrio": 0.5, "normal": 0},
    "dragao":   {"dragao": 2, "aco": 0.5},
    "sombrio":  {"psiquico": 2, "fantasma": 2, "lutador": 0.5, "sombrio": 0.5},
    "aco":      {"gelo": 2, "pedra": 2,
                "fogo": 0.5, "agua": 0.5, "eletrico": 0.5, "aco": 0.5},
}


def multiplicador_tipo(tipo_ataque, tipos_defensor):
    """Multiplicador total do ataque contra um defensor (suporta tipo duplo)."""
    mult = 1.0
    for t in tipos_defensor:
        mult *= TABELA_TIPOS.get(tipo_ataque, {}).get(t, 1)
    return mult


def descricao_efetividade(mult):
    """Texto para mostrar na tela de batalha."""
    if mult == 0:
        return "Não afeta..."
    if mult > 1:
        return "É super efetivo!"
    if mult < 1:
        return "Não é muito efetivo..."
    return ""
