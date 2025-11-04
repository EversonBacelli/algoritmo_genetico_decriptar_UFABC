import enchant
import random
import copy
import time


# MODULOS INTERNOS
from .stage1_ler_converter.processarBinarios import converterParaAscii, limparCaracteresEspeciais
from .utils_processar_texto.utils import limparDicionario, testModelo
from .utils_processar_texto.pegarLetrasUnicas import pegarLetrasUnicas
from .stage2_AG.calcularScore import calcular_score_palavras
from .stage2_AG.gerarChaves import gerarChaves
from .utils_processar_texto.dicionario import getNovoDicionario

# MODELO
from .stage2_AG.Alternativas import Alternativa

######## Inicio da Execução ########
start_time = time.perf_counter()

# stage 1 - converter binário em caracteres
caracteres_ascii = converterParaAscii()
palavras = caracteres_ascii.split()
palavras = limparCaracteresEspeciais(palavras)

palavras = [p.lower() for p in palavras]


# stage 2 -Gerar ancestrais
## Habilitar o dicionário
d = enchant.Dict("en_US")
word_list = getNovoDicionario()
Alternativa.DICIONARIO = word_list

## Gerar - Os patriarcas
letras_unicas_texto = pegarLetrasUnicas(caracteres_ascii)
Alternativa.CARACTERES_UNICOS = letras_unicas_texto
Alternativa.PALAVRAS = palavras

chaves_iniciais = []
for i in range(50):
    nova_chave = gerarChaves(letras_unicas_texto)
    chaves_iniciais.append(nova_chave)


alternativas = []
for chave in chaves_iniciais:
    alt = Alternativa(chave, copy.deepcopy(palavras))
    alternativas.append(alt)

Alternativa.GERACOES.append(alternativas)

##
QTD_GERACOES = 5000
TAXA_MUTACAO = 0.4
QTD_MUTANTES = 150
QTD_SOBREVIVENTES = 5


# numero_de_ciclos, tempo_processamento, consumo_memoria, scoreFitness


tempo_processamento = 0
qtd_memoria = 0


cont = 0


    
SCORE_FITNESS_FINAL = 0
NUMERO_FINAL_CICLOS = 0

for i in range(QTD_GERACOES):
    Alternativa.criarNovaGeracao(QTD_MUTANTES, TAXA_MUTACAO, copy.deepcopy(palavras), QTD_SOBREVIVENTES)
    ultimarGeracao = Alternativa.GERACOES[-1]
    
    maisAdaptado = ultimarGeracao[:1]
    fitness_final, numero_de_palavras_certas, numero_palavra_erradas, palavras_certas = maisAdaptado[0].scoreFitness
    
    if fitness_final > 223000.00:  ## caso seja o texto 1 o valor é 84.000
        # testModelo(ultimarGeracao)
        break
    # else:
        # testModelo(ultimarGeracao)
    NUMERO_FINAL_CICLOS = i
    print("N° do ciclo atual :" , '  ', NUMERO_FINAL_CICLOS)
    SCORE_FITNESS_FINAL = fitness_final
    print(f"N° do ciclo atual : {NUMERO_FINAL_CICLOS} |  SCORE_FINAL: {SCORE_FITNESS_FINAL}")


end_time = time.perf_counter()
tempo_total = (end_time - start_time) / 60

print('SCORE FITNESS FINAL: ' , round(SCORE_FITNESS_FINAL,2))
print('Numero de Ciclos: ', NUMERO_FINAL_CICLOS)
print("TEMPO TOTAL: " , round( tempo_total, 2))
