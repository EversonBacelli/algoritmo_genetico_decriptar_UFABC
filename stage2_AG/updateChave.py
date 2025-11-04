
import random
import copy
from typing import List, Tuple, Dict, Set, Iterable

# ATENÇÃO: Definindo o ALFABETO COMPLETO para permitir a geração aleatória de substitutos.

ALFABETO_COMPLETO = 'abcdefghijklmnopqrstuvwxyz' 

def estender_chave_segura(
    chave_base: List[Tuple[str, str]], 
    novos_mapeamentos: List[Tuple[str, str]]
) -> List[Tuple[str, str]]:
    
    # 1. PREPARAÇÃO
    chave_estendida_dict: Dict[str, str] = dict(copy.deepcopy(chave_base))
    letras_decifradas_usadas: Set[str] = set(chave_estendida_dict.values())
    alfabeto_set = set(ALFABETO_COMPLETO)
    
    # 2. PROCESSAMENTO E SUBSTITUIÇÃO DE CONFLITOS
    for cifrado, decifrado in novos_mapeamentos:
        
        # A. Conflito 1: Letra Cifrada (Maiúscula) JÁ MAPEADA (Ignora)
        if cifrado in chave_estendida_dict:
            continue 

        # B. Conflito 2: Letra Decifrada (Minúscula) JÁ USADA (Força Substituição Aleatória)
        if decifrado in letras_decifradas_usadas:
            
            # 1. Encontra as letras decifradas disponíveis (do alfabeto - as usadas)
            letras_disponiveis = list(alfabeto_set - letras_decifradas_usadas)

            if not letras_disponiveis:
                # Se o alfabeto estiver esgotado, não podemos mapear este item.
                continue 

            # 2. Escolhe uma letra aleatória disponível
            novo_decifrado = random.choice(letras_disponiveis)
            
            # Adiciona o mapeamento com a letra aleatória
            chave_estendida_dict[cifrado] = novo_decifrado
            letras_decifradas_usadas.add(novo_decifrado)
            
        else:
            # SEM CONFLITO: Adiciona o mapeamento original
            chave_estendida_dict[cifrado] = decifrado
            letras_decifradas_usadas.add(decifrado)
            
    # 3. CONVERTE DE VOLTA PARA LISTA DE TUPLAS ORDENADA
    chave_final_lista = sorted(
        list(chave_estendida_dict.items()), 
        key=lambda item: item[0]
    )
    
    return chave_final_lista