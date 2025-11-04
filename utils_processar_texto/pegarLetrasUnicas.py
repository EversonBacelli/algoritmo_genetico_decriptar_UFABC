

from typing import List

def pegarLetrasUnicas(texto_cifrado: str) -> List[str]:
   
    texto_sem_espacos = texto_cifrado.replace(' ', '')
    
    # 2. Obter as letras únicas usando um conjunto (set)
    letras_unicas = set(texto_sem_espacos)
    
    # 3. Converter para lista e ordenar alfabeticamente
    letras_unicas_list = sorted(list(letras_unicas))
    lista_minuscula = [letra.lower() for letra in letras_unicas_list]

    lista_minuscula_limpa = []
    for letra in lista_minuscula:
        if letra.isalnum():
            lista_minuscula_limpa.append(letra)
    return lista_minuscula_limpa