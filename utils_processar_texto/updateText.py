import copy

from .utils import mudarLetra


def updateTexto(palavras_cifradas, chave):
    CORINGA = '_'
    
    # --- Passo 1: Preparação e Mapeamento para Decifragem/Coringa ---
    
    # 1A. Criar dicionários para consulta rápida
    mapa_decifragem = dict(chave)           # {letra_cifrada: letra_decifrada}
    letras_cifradas_mapeadas = mapa_decifragem.keys()
    
    # 1B. Lista para armazenar o resultado da decifragem com coringa
    texto_intermediario = [] 
    
    for palavra_cifrada in palavras_cifradas:
        palavra_resultante = ""
        
        # Itera sobre CADA letra na palavra cifrada
        for letra in palavra_cifrada:
            # 2. CORREÇÃO: Verifica se a letra cifrada TEM mapeamento
            if letra in letras_cifradas_mapeadas:
                # Se mapeada: Decifra e adiciona
                palavra_resultante += mapa_decifragem[letra].lower()
            else:
                # Se NÃO mapeada: Adiciona o Coringa
                palavra_resultante += CORINGA
                
        texto_intermediario.append(palavra_resultante)

    return texto_intermediario


