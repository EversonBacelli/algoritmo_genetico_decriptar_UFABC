import random
import copy
from typing import List, Tuple, Dict, Set, Any

def criar_crossover_chaves(
    chave1_lista: List[Tuple[str, str]], 
    chave2_lista: List[Tuple[str, str]]
) -> List[Tuple[str, str]]:
    try:
        """
        Cria uma chave híbrida (permutação válida) a partir de duas chaves de substituição.
        Utiliza um Crossover de Permutação Simplificado (Baseado em Slice/Preenchimento).
        """
        
        # -----------------------------------------------
        # 1. PREPARAÇÃO (Usamos Dicionário para mapeamento, Listas para ordem)
        # -----------------------------------------------
        chave1_dict = dict(chave1_lista)
        chave2_dict = dict(chave2_lista)
        
        # Lista ordenada das letras cifradas (maiúsculas) para garantir a ordem
        letras_cifradas = list(chave1_dict.keys()) 
        n = len(letras_cifradas)
        
        # -----------------------------------------------
        # 2. LÓGICA DE CROSSOVER (Garante Permutação)
        # -----------------------------------------------
        
        # 2a. Escolher Ponto de Corte (Slice do Pai 1)
        ponto_corte = random.randrange(1, n - 1) 
        
        # Segmento de letras cifradas (posições) que herdarão do Pai 1
        segmento_cifradas = letras_cifradas[:ponto_corte]
        
        chave_hibrida_dict: Dict[str, str] = {}
        
        # 2b. Herdar Segmento (Pai 1)
        # Copia o mapeamento do segmento para a chave híbrida
        for letra_cifrada in segmento_cifradas:
            mapeamento = chave1_dict[letra_cifrada]
            chave_hibrida_dict[letra_cifrada] = mapeamento
        
        # Mapeamentos (minúsculas) que JÁ foram usados pelo Pai 1
        mapeamentos_usados = set(chave_hibrida_dict.values())
        
        # 2c. Preencher com o Resto (Pai 2)
        # Obtém todos os mapeamentos do Pai 2, APENAS se ainda não foram usados
        mapeamentos_pai2_ordenados = []
        for letra_cifrada in letras_cifradas:
            mapeamento_pai2 = chave2_dict[letra_cifrada]
            # Só adiciona se o mapeamento (letra minúscula) não foi usado
            if mapeamento_pai2 not in mapeamentos_usados:
                mapeamentos_pai2_ordenados.append(mapeamento_pai2)
                
        # As letras cifradas (maiúsculas) que AINDA não têm mapeamento na híbrida
        letras_vazias = letras_cifradas[ponto_corte:]
        
        # Preenche as posições restantes com os mapeamentos restantes do Pai 2, 
        # na ordem em que apareceram em 'mapeamentos_pai2_ordenados'
        for i, letra_cifrada in enumerate(letras_vazias):
            chave_hibrida_dict[letra_cifrada] = mapeamentos_pai2_ordenados[i]
            
        # -----------------------------------------------
        # 3. CONVERSÃO DE SAÍDA (Dicionário -> Lista de Tuplas)
        # -----------------------------------------------
        
        # Garante a ordem original das chaves (A, B, C, ...)
        chave_hibrida_lista_tuplas = [
            (letra, chave_hibrida_dict[letra]) 
            for letra in letras_cifradas
        ]
        
        return chave_hibrida_lista_tuplas
    except Exception as e:
        return []
    

LETRAS_FIXAS = {'A', 'I'} 
TAXA_DE_MUTACAO = 0.40 # 15% é um bom ponto de partida para a taxa de mutação

def mutar_chave_segura(
    chave_lista: List[Tuple[str, str]], 
    taxa_mutacao: float 
) -> List[Tuple[str, str]]:
    """
    Realiza a Mutação por Troca (Swap Mutation) de forma segura:
    Somente troca mapeamentos de letras que NÃO estão no conjunto LETRAS_FIXAS.
    """
    
    # 1. DECISÃO DE MUTAÇÃO: A mutação é um evento probabilístico
    if random.random() > taxa_mutacao:
        # Se o número aleatório for maior que a taxa (ex: 0.90 > 0.15), não muta
        return chave_lista
    
    # 2. PREPARAÇÃO
    chave_dict: Dict[str, str] = dict(chave_lista)
    
    # Identifica as letras que podem ser mutadas (Maiúsculas, que não são 'A', 'I', etc.)
    letras_mutaveis: List[str] = [
        letra for letra in chave_dict.keys() 
        if letra not in LETRAS_FIXAS
    ]
    
    # Se houver menos de 2 letras mutáveis, o swap não pode ocorrer
    if len(letras_mutaveis) < 2:
        return chave_lista

    # 3. SELEÇÃO E EXECUÇÃO DO SWAP
    
    # Escolhe duas letras aleatórias APENAS do conjunto mutável
    letra1, letra2 = random.sample(letras_mutaveis, 2)
    
    # Obtém os mapeamentos decifrados (minúsculos)
    mapeamento1 = chave_dict[letra1]
    mapeamento2 = chave_dict[letra2]
    
    # Realiza a troca (swap)
    chave_dict[letra1] = mapeamento2
    chave_dict[letra2] = mapeamento1
    
    # 4. CONVERSÃO DE SAÍDA (De volta para lista de tuplas ordenada)
    # Garante que a ordem alfabética das letras cifradas é mantida
    return sorted(list(chave_dict.items()), key=lambda item: item[0])

## Estratégia diferente de selecionar 
def selecao_por_torneio(populacao , tamanho_torneio: int = 3, ):
    """Seleciona o melhor indivíduo de um subconjunto aleatório."""
    # 1. Escolhe 'tamanho_torneio' indivíduos aleatórios
    candidatos_com_indice = []
    
    # 1. Escolhe os índices aleatórios e associa o objeto
    indices_candidatos = random.sample(range(len(populacao)), tamanho_torneio)
    
    for idx in indices_candidatos:
        candidatos_com_indice.append((idx, populacao[idx]))

    # 2. Encontra o candidato com o melhor score
    # max() retorna a tupla (índice, Alternativa) com o maior score.
    idx_melhor, melhor_pai = max(
        candidatos_com_indice, 
        key=lambda item: item[1].scoreFitness
    )
    
    return melhor_pai, idx_melhor