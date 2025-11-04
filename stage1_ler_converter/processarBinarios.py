import os

#arquitetura_e_organizacao_de_computadores_UFABC_decriptografia/stage1_converter
def lerArquivo():
    base_dir = os.path.dirname(__file__)
    caminho_arquivo = os.path.join(base_dir, "textoAtividade.txt")
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo_completo = arquivo.read()
        lista_de_caracteres = conteudo_completo.split()
    return lista_de_caracteres


def converterParaAscii():
    lista_de_caracteres = lerArquivo()
    caracteres_hex = []

    for caractere in lista_de_caracteres:
        caracteres_hex.append(hex(int(caractere, 2)))

    caracteres_ascii = "".join([
        chr(int(h, 16)) for h in caracteres_hex 
    ])

    return caracteres_ascii

def limparCaracteresEspeciais(lista_de_strings):
    # Lista para armazenar palavras limpas
    palavras_limpas = []
    
    # Processar cada string da lista
    for palavra in lista_de_strings:
        # Manter apenas caracteres alfanuméricos
        # palavra_limpa = ''.join(char for char in palavra if char.isalnum())
        palavra_limpa = []
        for p in palavra:
            if p.isalnum():
                palavra_limpa.append(p)
        np = "".join(palavra_limpa)
        palavras_limpas.append(np)
    
    return palavras_limpas