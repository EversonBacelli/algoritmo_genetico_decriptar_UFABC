import random
from enum import Enum

from ..utils_processar_texto.updateText import updateTexto
from .calcularScore import normalizar_texto, calcularScoreIntegrado, calcular_score_palavras
import copy
from .estrategiasAG import criar_crossover_chaves, mutar_chave_segura, selecao_por_torneio
from .gerarChaves import gerarChaves

class Alternativa:
    DICIONARIO = []
    GERACOES = []
    ABANDONADOS = []
    MINIMO_LOCAL = [[0],[0]]
    CASTIGO_OPRESSORES = []
    CARACTERES_UNICOS = []
    PALAVRAS = []

    def __init__(self, chave, TEXTO):
        self.chave = chave
        self.novasPalavras = updateTexto(copy.deepcopy(TEXTO), chave)
        texto_normalizado = normalizar_texto(copy.deepcopy(self.novasPalavras))
        self.scoreFitness = calcularScoreIntegrado(self.novasPalavras, texto_normalizado, Alternativa.DICIONARIO)
        self.acertos = 0
        
    def criarNovaGeracao( NUMERO_DE_TUTANTES, TAXA_MUTACAO, TEXTO, QTD_SOBREVIVENTES):           
        ##
        
        ## Pegar a última geração
        alternativas = copy.deepcopy(Alternativa.GERACOES[-1])
        
        ## Amplificar taxa de mutação em caso de minimo local
        TAXA_MUTACAO, qtd, alternativas, remove = Alternativa.verificarMaximoLocal(alternativas[-1], TAXA_MUTACAO, alternativas)
        
        piores = []
        ## Criar novaGeração
        for ciclo in range(NUMERO_DE_TUTANTES):
            alternativas, piores = Alternativa.criarHerdeiro(alternativas, TEXTO, TAXA_MUTACAO, piores)
        
        ## elitismo
        principais_alternativas = alternativas[:QTD_SOBREVIVENTES]

        # diversidade
        if len(piores) > 0:
            piores.sort(key=lambda alt: alt.scoreFitness, reverse=True)
            melhor_dos_piores = piores[:qtd]
            pior_dos_piores = piores[qtd:]
            Alternativa.ABANDONADOS.extend(melhor_dos_piores)
            Alternativa.ABANDONADOS.extend(pior_dos_piores)

            ancestrais = []
            for i in range(qtd):
                posicao1 = len(Alternativa.ABANDONADOS ) - 1
                ancestral = Alternativa.ABANDONADOS[random.randint(0, posicao1)]
                ancestrais.append(ancestral)
            
            principais_alternativas.extend(melhor_dos_piores)
            principais_alternativas.extend(pior_dos_piores)
            principais_alternativas.extend(ancestrais)
            
        # ## Tira do gancho
        if remove:
            principais_alternativas.extend(Alternativa.CASTIGO_OPRESSORES)
            Alternativa.CASTIGO_OPRESSORES.clear()
            
        ## inserir novaGeração
        Alternativa.GERACOES.clear()
        Alternativa.GERACOES.append(principais_alternativas)    
    
    def criarHerdeiro(alternativas, TEXTO, TAXA_MUTACAO, piores):
        piores = []

        # 1. Seleção dos Pais (Seleção Aleatória Simples)
        melhor_pai1, idx1_melhor = selecao_por_torneio(alternativas, 3)
        melhor_pai2, idx2_melhor = selecao_por_torneio(alternativas, 3)
                
        # Garante que os pais são diferentes para um crossover mais eficaz
        while idx1_melhor == idx2_melhor:
            melhor_pai2, idx2_melhor = selecao_por_torneio(alternativas, 3)

        pai1 = melhor_pai1
        pai2 = melhor_pai2
            
        # 2. Reprodução (Crossover) - Combinar o material genético
        chave_hibrida = criar_crossover_chaves(copy.deepcopy(pai1.chave), copy.deepcopy(pai2.chave))
                
        # 3. Introduzir mutações no novo individuo  
        chave_mutada = mutar_chave_segura(chave_hibrida, TAXA_MUTACAO)
                
        # 4. Criar uma nova chave, já avaliada
        novaAlternativa = Alternativa(chave_mutada, TEXTO) 
        
        # 5. Sobrevivência (Torneio Simples: Filho vs. Pior Pai)        
        # Encontra o índice do pai com o PIOR fitness (maior score negativo)
        id_pior = 0
        pai_pior = None
        if pai1.scoreFitness < pai2.scoreFitness:
            pai_pior = pai1
            id_pior = idx1_melhor
        else:
            pai_pior = pai2
            id_pior = idx2_melhor
                    
        # Se o Filho for estritamente melhor que o pior pai, substitui
        if novaAlternativa.scoreFitness > pai_pior.scoreFitness:
            piores.append(pai_pior)
            alternativas[id_pior] = novaAlternativa

        # Ordena o vetor final (É fundamental ordenar o vetor para o AG)
        alternativas.sort(key=lambda alt: alt.scoreFitness, reverse=True)    
        
        ## Se o novo individuo for melhor, é incluso 
        return alternativas, piores
    
    def verificarMaximoLocal(topo, TAXA_MUTACAO, alternativas):
        qtd = 2
        if Alternativa.MINIMO_LOCAL[0][0] == 0:
            Alternativa.MINIMO_LOCAL[0][0] = topo.scoreFitness
            Alternativa.MINIMO_LOCAL[1][0] += 1
            return TAXA_MUTACAO, qtd, alternativas, False
        elif Alternativa.MINIMO_LOCAL[0][0] == topo.scoreFitness:   
                if Alternativa.MINIMO_LOCAL[1][0] > 5:
                    Alternativa.MINIMO_LOCAL[1][0] = 0
                    
                    # print('Ampliada Taxa de Mutacao')
                    NOVA_TAXA = TAXA_MUTACAO * 1.5
                    
                    
                    top2 = alternativas.pop(0)
                    top3 = alternativas.pop(0)


                    for i in range(3):
                        top = alternativas.pop(0)
                        Alternativa.CASTIGO_OPRESSORES.append(top)
                 
                    for i in range(5):
                        # del alternativas[0]
                        
                        c1 = gerarChaves(Alternativa.CARACTERES_UNICOS)
                        alternativas.append(Alternativa(c1, copy.deepcopy(Alternativa.PALAVRAS)))
                        

                    qtd = qtd + 8
                    return NOVA_TAXA, qtd, alternativas, True
                else:
                    Alternativa.MINIMO_LOCAL[1][0] += 1
                    return TAXA_MUTACAO, qtd, alternativas, False
        else: 
            Alternativa.MINIMO_LOCAL[0][0] = topo.scoreFitness
            Alternativa.MINIMO_LOCAL[1][0] = 0
            return TAXA_MUTACAO, qtd, alternativas, False


