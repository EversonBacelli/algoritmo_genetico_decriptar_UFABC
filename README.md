# 🧬 Algoritmo Genético para Decriptação (UFABC)

Repositório: **`algoritmo_genetico_decriptar_UFABC`**  
Autor: *Everson Bacelli*  
Licença sugerida: **MIT**

> Projeto acadêmico que implementa um **algoritmo genético (AG)** para a **decriptação de cifras por substituição**, utilizando técnicas heurísticas e análise estatística de linguagem.  
> Desenvolvido no contexto da **Universidade Federal do ABC (UFABC)**.

---

## 📚 Sumário

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Executar](#-como-executar)
- [Parâmetros do Algoritmo](#-parâmetros-do-algoritmo)
- [Como o Algoritmo Funciona](#-como-o-algoritmo-funciona)
- [Resultados e Logs](#-resultados-e-logs)
- [Testes e Validação](#-testes-e-validação)
- [Melhorias Futuras](#-melhorias-futuras)
- [Contribuições](#-contribuições)
- [Licença](#-licença)
- [Contato](#-contato)

---

## 💡 Visão Geral

O objetivo do projeto é aplicar um **algoritmo genético (AG)** para **quebrar cifras simples**, como a cifra de substituição monoalfabética.  
O AG tenta encontrar uma **chave de substituição** que maximize a semelhança entre o texto decifrado e o idioma natural (ex.: português), utilizando **frequência de letras** e **modelos de n-gramas** como métrica de aptidão (*fitness*).

---

## ⚙️ Funcionalidades

✅ Implementação completa de um Algoritmo Genético  
✅ Suporte a fitness baseado em **n-gramas** e **frequência de letras/palavras**  
✅ Parâmetros configuráveis via **linha de comando** ou arquivo **JSON**  
✅ Salvamento do **melhor indivíduo** e **logs por geração**  
✅ Estrutura modular e expansível (crossover, mutação, seleção etc.)  
✅ Execução reproduzível via *random seed*  

---

## 🧩 Pré-requisitos

- **Python** ≥ 3.8  
- Pacotes necessários:
  ```bash
  pip install numpy tqdm pandas
🚀 Instalação
Clone o repositório e acesse o diretório:

bash
Copiar código
git clone https://github.com/EversonBacelli/algoritmo_genetico_decriptar_UFABC.git
cd algoritmo_genetico_decriptar_UFABC
🗂️ Estrutura do Projeto
bash
Copiar código
algoritmo_genetico_decriptar_UFABC/
├── README.md
├── requirements.txt
├── src/
│   ├── main.py              # Script principal (entrada do programa)
│   ├── ga.py                # Núcleo do algoritmo genético
│   ├── fitness.py           # Funções de avaliação (n-gramas)
│   ├── operators.py         # Crossover, mutação, seleção
│   ├── util.py              # Funções auxiliares (IO, manipulação de texto)
│   └── data/
│       ├── ciphertext.txt   # Texto cifrado de exemplo
│       └── corpus.txt       # Corpus de referência para scoring
├── experiments/
│   └── example_config.json
└── results/
    └── best.txt
🧠 Como Executar
🔹 Opção 1 — Linha de comando
bash
Copiar código
python src/main.py --cipher src/data/ciphertext.txt \
                   --population 500 \
                   --generations 1000 \
                   --mutation 0.02 \
                   --crossover 0.9 \
                   --seed 42 \
                   --output results/best.txt
🔹 Opção 2 — Arquivo de configuração
Arquivo experiments/example_config.json:

json
Copiar código
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
Execução:

bash
Copiar código
python src/main.py --config experiments/example_config.json
⚙️ Parâmetros do Algoritmo
Parâmetro	Descrição	Valor padrão
--population	Tamanho da população	300
--generations	Nº de gerações	1000
--mutation	Taxa de mutação	0.02
--crossover	Taxa de crossover	0.8
--selection	Método de seleção (tournament, roulette, rank)	tournament
--elitism	Nº de indivíduos mantidos	1
--seed	Valor fixo para reprodutibilidade	None

🔍 Como o Algoritmo Funciona
Inicialização: cria uma população aleatória de chaves (permutações do alfabeto).

Avaliação (fitness): decifra o texto e mede a "naturalidade" do resultado.

Seleção: escolhe os indivíduos mais promissores.

Crossover: combina partes das chaves dos pais.

Mutação: faz pequenas alterações aleatórias.

Elitismo: mantém os melhores indivíduos.

Iteração: repete até convergir ou atingir o limite de gerações.

Exemplo de cálculo de fitness:

python
Copiar código
score = 0.0
for trigram in text:
    score += math.log(prob_trigram.get(trigram, 1e-12))
📊 Resultados e Logs
Durante a execução, são gerados:

results/best.txt → texto decifrado com o melhor indivíduo

results/log.csv → log por geração (fitness médio, melhor fitness etc.)

Exemplo de saída no terminal:

yaml
Copiar código
Geração  250 / 1000 | Melhor fitness: -1234.56 | Texto parcial: "o segredo está revelado..."
🧪 Testes e Validação
Gere um texto cifrado conhecido e verifique se o AG consegue recuperar o plaintext.

Varie parâmetros (população, taxa de mutação) e observe a convergência.

Compare diferentes métricas de fitness (frequência simples vs. n-gramas).

🚧 Melhorias Futuras
 Suporte a outras cifras (Vigenère, Hill, Afim)

 Paralelização de fitness com multiprocessing

 Interface visual (Streamlit / Tkinter)

 Otimização híbrida (AG + Hill Climbing)

 Visualização de convergência em tempo real

🤝 Contribuições
Contribuições são bem-vindas!
Para colaborar:

Faça um fork do repositório

Crie uma branch: git checkout -b feature/nome-da-feature

Commit: git commit -m "Adiciona nova feature"

Push: git push origin feature/nome-da-feature

Abra um Pull Request

📄 Licença
Distribuído sob a licença MIT.
Consulte o arquivo LICENSE para mais informações.

text
Copiar código
MIT License
Copyright (c) 2025 Everson Bacelli
