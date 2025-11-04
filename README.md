Algoritmo Genético — Decriptar (UFABC)

Repositório: algoritmo_genetico_decriptar_UFABC
Autor: Everson Bacelli (presumivelmente)
Descrição curta: Implementação de um algoritmo genético para quebrar / decriptar (ataque de força heurística) cifras simples (p.ex. cifra por substituição) — desenvolvido no contexto UFABC.

Observação: como não tenho acesso direto ao conteúdo do repositório neste momento, este README foi escrito para ser aplicável ao repositório com esse nome. Ajuste nomes de ficheiros/paths conforme o seu projeto real.

Índice

Visão geral

Funcionalidades

Pré-requisitos

Instalação

Estrutura sugerida do repositório

Uso / Exemplos de execução

Configuração de parâmetros

Como funciona (resumo do algoritmo)

Resultados esperados / output

Testes

Contribuição

Licença

Contato

Visão geral

Este projeto implementa um algoritmo genético (AG) para encontrar chaves/sistemas de substituição que transformem um texto cifrado em texto plausível em português (ou outro idioma), usando medidas de aptidão como modelos de n-gramas, scoring por frequência de letras/palavras ou comparação com corpus de referência.

O objetivo principal é apresentar:

representação de indivíduos (chaves/permutações),

operadores genéticos (crossover, mutação),

seleção (torneio, roleta, rank),

função de aptidão baseada em modelos linguísticos.

Funcionalidades

Implementação de AG para quebra de cifras por substituição (ex.: cifra monoalfabética).

Fitness baseado em n-gramas (monogramas, bigramas, trigramas) ou frequência de palavras.

Variação de parâmetros: tamanho da população, prob. de mutação, prob. de crossover, número de gerações.

Salvamento do melhor indivíduo a cada geração / logs de execução.

(Opcional) Interface CLI simples para executar e configurar experimentos.

Pré-requisitos

Python 3.8+

Bibliotecas (instale via pip):

numpy

tqdm (opcional, para progress bars)

pandas (opcional, para análise de resultados)

Exemplo:

python -m venv venv
source venv/bin/activate   # linux/mac
venv\Scripts\activate      # windows
pip install numpy tqdm pandas

Instalação

Clone o repositório:

git clone https://github.com/EversonBacelli/algoritmo_genetico_decriptar_UFABC.git
cd algoritmo_genetico_decriptar_UFABC


Crie e ative um ambiente virtual (opcional, recomendado) e instale dependências como mostrado acima.

Estrutura sugerida do repositório

A estrutura abaixo é sugerida e provavelmente corresponde ao layout do projeto — ajuste conforme os ficheiros reais:

algoritmo_genetico_decriptar_UFABC/
├── README.md
├── requirements.txt
├── src/
│   ├── main.py                # script principal / CLI
│   ├── ga.py                  # lógica do algoritmo genético
│   ├── operators.py           # crossover / mutação / seleção
│   ├── fitness.py             # funções de avaliação (n-gram scoring)
│   ├── util.py                # utilitários (decodificação, IO)
│   └── data/
│       ├── corpus.txt         # corpus de referência (opcional)
│       └── ciphertext.txt     # texto cifrado de exemplo
├── experiments/
│   └── example_config.json
└── results/
    └── best_individuals.csv

Uso / Exemplos de execução
Executando o script principal (exemplo)

Se existir um main.py:

python src/main.py --cipher src/data/ciphertext.txt \
                   --population 500 \
                   --generations 1000 \
                   --mutation 0.02 \
                   --crossover 0.9 \
                   --seed 42 \
                   --output results/best.txt


Parâmetros possíveis (exemplo):

--cipher : caminho para o texto cifrado.

--population : tamanho da população.

--generations : número máximo de gerações.

--mutation : probabilidade de mutação (ex.: 0.01 = 1%).

--crossover : probabilidade de crossover (ex.: 0.8).

--selection : método de seleção (tournament, roulette, rank).

--elitism : número de indivíduos elitistas a preservar por geração.

--output : arquivo para salvar o melhor deciframento.

Executando com um arquivo de configuração (JSON)

Exemplo experiments/example_config.json:

{
  "cipher": "src/data/ciphertext.txt",
  "population": 400,
  "generations": 800,
  "mutation": 0.03,
  "crossover": 0.85,
  "selection": "tournament",
  "elitism": 1,
  "seed": 1234
}


E execução:

python src/main.py --config experiments/example_config.json

Configuração de parâmetros (exemplo de defaults recomendados)
Parâmetro	Valor padrão sugerido
population	300
generations	1000
mutation_rate	0.02
crossover_rate	0.8
selection	tournament (size=3)
elitism	1
seed	None
Como funciona (resumo do algoritmo)

Representação: cada indivíduo representa uma permutação do alfabeto (chave de substituição).

Inicialização: população inicial composta por permutações aleatórias.

Avaliação (fitness): decodifica-se o texto cifrado com a chave do indivíduo e calcula-se um score por similaridade com o idioma (n-gram scoring / log prob).

Seleção: escolhe pais via torneio/roleta/rank.

Crossover: combinações de permutações (p.ex. PMX — Partially Mapped Crossover, ou outro método específico para permutações).

Mutação: swap aleatório entre duas posições da permutação com probabilidade mutation_rate.

Elitismo: preserva os melhores indivíduos para a próxima geração.

Parada: por número de gerações ou por atingir fitness alvo.

Fitness (detalhes práticos)

Utilize log-probabilidade de n-gramas (bigrams/trigrams) para evitar underflow.

Treine um modelo simples no corpus (por ex., contar frequências e converter para probabilidades).

Score do texto decodificado = soma dos logs das probabilidades de cada n-grama encontrado.

Exemplo (pseudocódigo):

score = 0.0
for each trigram in text:
    score += log(prob_trigram.get(trigram, small_value))

Resultados esperados / Output

results/best.txt — texto decodificado com a melhor chave encontrada.

results/log.csv — log por geração com: geração, melhor fitness, média fitness, melhor indivíduo (chave).

Impressões no console com progresso (opcional: tqdm).

Exemplo de saída no console:

Geração  100 / 1000 | Melhor fitness: -1234.56 | Texto: "aqui vai um trecho legível..."

Testes

Tenha um texto claro (plaintext) e aplique uma chave conhecida (substituição) para gerar ciphertext.txt. Rode o AG e verifique se a chave encontrada é igual (ou próxima) da chave original ou se o plaintext é recuperado.

Teste variações de parâmetros para ver robustez (pop size, mutation_rate).

Compare fitness com função de n-gramas vs. frequência de palavras para ver qual converge melhor.

Dicas para melhorar performance

Use mais população ou mais gerações quando o espaço de busca for grande.

Combine AG com heurísticas locais (ex.: hill climbing) para polir soluções (memetic algorithm).

Use avaliação em log para estabilidade numérica.

Faça múltiplas execuções com diferentes seeds e escolha o melhor resultado.

Contribuição

Abra uma issue descrevendo a proposta.

Crie um branch com uma feature/bugfix.

Faça um pull request com descrição e testes básicos.

Sugestões de melhorias:

adicionar GUI simples (tkinter/streamlit) para testar rapidamente.

adicionar paralelização (multiprocessing) para avaliação de populações grandes.

suporte a outros tipos de cifra (Vigenère, Hill, etc).

Licença

Coloque aqui a licença desejada (ex.: MIT, GPL-3.0). Se ainda não existir, recomendo MIT para projetos académicos que você queira compartilhar livremente:

MIT License
Copyright (c) 2025 Everson Bacelli
...
