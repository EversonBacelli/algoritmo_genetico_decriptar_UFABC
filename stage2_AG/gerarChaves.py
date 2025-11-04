import random

from ..utils_processar_texto.utils import pegarAlfabeto, pegarLetrasMaisFrequentes

def gerarChaves(caracteres):
    letras = [item[0] for item in caracteres]
    alfabeto = pegarAlfabeto()
    
    chaves = []
    for l in letras:
        indice_aleatorio = random.randrange(len(alfabeto))
        # 2. Usa pop() para retirar o item nessa posição
        item_retirado = alfabeto.pop(indice_aleatorio)
        chaves.append((l, item_retirado))
    
    return chaves