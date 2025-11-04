from ..utils_processar_texto.updateText import updateTexto
from typing import Dict, List, Set, Tuple

def calcular_score_palavras(
    palavras_decifradas: List[str], 
    dicionario_validas: Set[str], 

) -> Tuple[int, float]:
    tamanho = len(palavras_decifradas)
    
    palavras_limpas = [
        palavra
        for palavra in palavras_decifradas
        if "_" not in palavra  # Condição de filtro: não pode conter o coringa
    ]

    palavras_decifradas = palavras_limpas

    palavras_decifradas = [palavra.lower() for palavra in palavras_decifradas]  # Normaliza para minúsculas
    
    palavras_certas = []
    palavras_erradas = []
    # 2. Contagem de Acertos
    for palavra in palavras_decifradas:
        if palavra in dicionario_validas: 
            palavras_certas.append(palavra)
        else:
            palavras_erradas.append(palavra)
            
    numero_de_palavras_certas = len(list(set(palavras_certas)))  # Remove duplicatas

    porcentagem_acerto = ( len(palavras_certas) / tamanho) * 100
    
    return numero_de_palavras_certas, porcentagem_acerto, palavras_certas, palavras_erradas, palavras_certas



def getBigramas() -> Dict[str, float]:
    """Retorna o vetor (dicionário) de Bigramas em Inglês e seus LL Scores."""
    return {
        'th': -1.449, 'he': -1.513, 'in': -1.614, 'er': -1.688, 
        'an': -1.701, 're': -1.733, 'on': -1.754, 'at': -1.827, 
        'en': -1.839, 'nd': -1.870, 'ti': -1.873, 'es': -1.879, 
        'or': -1.893, 'te': -1.921, 'of': -1.928, 'it': -1.936, 
        'is': -1.939, 'ed': -1.947, 'ra': -1.955, 'st': -1.967,
        'default': -10.0 # Penalidade para Bigramas não listados
    }

def getTrigramas() -> Dict[str, float]:
    """Retorna o vetor (dicionário) de Trigramas em Inglês e seus LL Scores."""
    return {
        'the': -1.703, 'ing': -2.076, 'and': -2.187, 'ion': -2.292, 
        'ent': -2.377, 'tio': -2.409, 'ati': -2.432, 'for': -2.444, 
        'her': -2.456, 'ter': -2.469, 'was': -2.481, 'ers': -2.495, 
        'his': -2.509, 'res': -2.523, 'are': -2.537, 'ive': -2.553, 
        'ver': -2.569, 'all': -2.585, 'thi': -2.602, 'iti': -2.620,
        'default': -10.0 # Penalidade para Trigramas não listados
    }

def normalizar_texto(texto_decifrado: List[str]) -> str:
    """Decifra o texto usando a chave e o retorna em minúsculas e sem caracteres especiais."""
   
    texto_decifrado_minusculo = [palavra.lower() for palavra in texto_decifrado]
    # Limpa e normaliza o texto para contagem de n-gramas (apenas letras de a-z)
    texto_limpo = ''.join(c for c in "".join(texto_decifrado_minusculo) if 'a' <= c <= 'z')
    return texto_limpo


def contar_n_gramas(texto_decifrado_limpo: str, n: int) -> Dict[str, int]:
    """Conta a ocorrência de N-gramas (pares ou trios) em um texto limpo."""
    contagem: Dict[str, int] = {}
    
    if len(texto_decifrado_limpo) < n:
        return contagem

    for i in range(len(texto_decifrado_limpo) - n + 1):
        n_grama = texto_decifrado_limpo[i:i+n]
        contagem[n_grama] = contagem.get(n_grama, 0) + 1
        
    return contagem

def calcularScoreIntegrado(
    texto_decifrado_str: str,            # Texto corrido (somente letras, maiúsculas) para N-gramas
    palavras_decifradas_list: List[str], # Lista de palavras limpas (minúsculas) para dicionário
    dicionario_validas: Set[str]         
) -> float:
    
    # ----------------------------------------------------
    # 1. DEFINIÇÃO DE PESOS (Ajustados para quebrar a estagnação)
    # ----------------------------------------------------
    
    # Pesos do LL Score (N-gramas)
    peso_bigrama_ll = 0.20 
    peso_trigrama_ll = 0.80
    
    # Pesos da Ponderação Final (Híbrida)
    peso_ll_score = 0.95        # Fator base, mantendo o LL Score como guia estrutural
    peso_word_score = 2000.0    # Fator amplificador e de desempate CRUCIAL

    # ----------------------------------------------------
    # 2. CÁLCULO DO LL SCORE TOTAL (Estrutura Estatística)
    # ----------------------------------------------------
    
    # Contagem de Bigramas e Trigramas no texto corrido
    contagem_bigramas = contar_n_gramas(palavras_decifradas_list, 2)
    contagem_trigramas = contar_n_gramas(palavras_decifradas_list, 3)
    
    BIGRAM_LL_SCORES = getBigramas()
    TRIGRAM_LL_SCORES = getTrigramas()
    
    # Cálculo do Score de Bigramas
    score_bigrama = 0.0
    ll_default_bigrama = BIGRAM_LL_SCORES.get('default', -10.0)
    for bigrama, contagem in contagem_bigramas.items():
        ll_score = BIGRAM_LL_SCORES.get(bigrama, ll_default_bigrama)
        score_bigrama += contagem * ll_score
        
    # Cálculo do Score de Trigramas
    score_trigrama = 0.0
    ll_default_trigrama = TRIGRAM_LL_SCORES.get('default', -10.0)
    for trigrama, contagem in contagem_trigramas.items():
        ll_score = TRIGRAM_LL_SCORES.get(trigrama, ll_default_trigrama)
        score_trigrama += contagem * ll_score
        
    # LL_Score Total (Valor negativo, representa a aptidão estatística)
    ll_score_total = (peso_bigrama_ll * score_bigrama) + (peso_trigrama_ll * score_trigrama)
    
    # ----------------------------------------------------
    # 3. CÁLCULO DO WORD SCORE (Validade Semântica)
    # ----------------------------------------------------
    
    # Contagem de palavras válidas (contagem_acertos) é o fator que nos interessa
    numero_de_palavras_certas, porcentagem_acerto, palavras_certas, palavras_erradas, palavras_certas = calcular_score_palavras(
        texto_decifrado_str, 
        dicionario_validas
    )
  
    # ----------------------------------------------------
    # 4. PONDERAÇÃO FINAL (MAXIMIZAÇÃO DE FITNESS)
    # ----------------------------------------------------
    
    # Componente LL Score: Fator base (negativo)
    score_ll_ponderado = peso_ll_score * ll_score_total
    
    # Componente Word Score: Fator de desempate (positivo e amplificado)
    
    score_word_ponderado = peso_word_score * numero_de_palavras_certas
    
    # O Fitness Final é MAXIMIZADO (o AG buscará o valor menos negativo)
    fitness_final = score_ll_ponderado + score_word_ponderado
    numero_palavra_erradas = len(palavras_erradas)
    return fitness_final, numero_de_palavras_certas, numero_palavra_erradas, palavras_certas 


