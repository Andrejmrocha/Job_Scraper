# 🚀 Job Scraper & AI Refiner

Uma esteira automatizada de dados (RPA) desenvolvida em Python que navega em uma plataforma de vagas de emprego, extrai vagas de tecnologia, previne duplicatas e utiliza Inteligência Artificial (OpenAI) para higienizar e estruturar os requisitos em formato JSON.

## 🎯 O Problema
Plataformas de vagas costumam ter descrições formatadas de maneira inconsistente pelo RH (texto livre, listas quebradas, seções misturadas). Extrair esses dados de forma bruta gera um banco de dados sujo e difícil de analisar.

## 💡 A Solução
Este projeto implementa uma arquitetura modular de Extração, Transformação e Carga (ETL):
1. **Extract (Scraping):** Utiliza o Playwright para contornar renderizações dinâmicas, preencher formulários de busca e extrair o HTML da página.
2. **Transform (LLM):** Envia os dados não estruturados para a API da OpenAI (`gpt-4o-mini`), garantindo via engenharia de prompt que os dados retornem limpos e no formato JSON estrito, sem perda ou alucinação de informações.
3. **Load (Persistência):** Salva os dados processados localmente em um arquivo JSON com timestamp, pronto para consumo em dashboards de BI ou bancos de dados relacionais.

## 🏗️ Arquitetura do Projeto

O projeto segue os princípios de *Clean Code* e *Separation of Concerns* (SoC), dividido nos seguintes módulos:

* `main.py`: O Maestro. Orquestra a ordem de execução do script e gerencia a lógica de negócio (como o filtro de chave composta para evitar vagas duplicadas).
* `scraper.py`: O Operário. Focado exclusivamente na interação com o DOM usando Playwright e localização de elementos CSS/XPath.
* `ia.py`: O Cérebro. Isola a comunicação com a API da OpenAI e gerencia o prompt do sistema.
* `utils.py`: O Auxiliar. Responsável pelo I/O e persistência dos dados no disco.

## 🛠️ Tecnologias Utilizadas

* **Python 3+**
* **Playwright:** Para automação e navegação headless/browser.
* **OpenAI API (GPT-4o-mini):** Para Processamento de Linguagem Natural e estruturação de dados.
* **python-dotenv:** Para gerenciamento seguro de credenciais e chaves de API.

## 🚀 Como Executar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/Andrejmrocha/Job_Scraper.git
cd Job_Scraper
```

### 2. Instale as dependências
```bash
pip install playwright openai python-dotenv
playwright install chromium
```
### 3. Configure as Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto e adicione sua chave de API da OpenAI:
````bash
OPENAI_API_KEY=sk-sua-chave-aqui
````
### 4. Execute o robô
```bash
python main.py
```
