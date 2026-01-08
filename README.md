# DP-Data-Pipeline
Camada de Engenharia de Dados para Privacidade Diferencial
## 📌 Visão Geral

Este repositório contém um pipeline de engenharia de dados responsável pela extração, preparação e aplicação de Privacidade Diferencial sobre dados provenientes de um Sistema de Recursos Humanos (RH), acessados via API.

Repositório do sistema base : https://github.com/L-Repinaldo/Projeto-Sistema-de-RH

O objetivo do pipeline é gerar datasets versionados, contendo uma versão original (baseline) e múltiplas versões privatizadas, aplicando mecanismos de Privacidade Diferencial de forma controlada, reproduzível e rastreável.

Este repositório concentra-se exclusivamente na etapa de preparação e privatização dos dados, sem assumir qualquer responsabilidade sobre o uso posterior desses datasets.

## 🏗️ Arquitetura do Projeto

O pipeline atua como uma camada intermediária de engenharia de dados, com as seguintes características:

  - Consome dados estruturados de um Sistema de RH (OLTP);

  - Não modifica nem interfere no banco de dados de origem;

  - Executa transformações e mecanismos de privacidade de forma batch;

  - Gera conjuntos de dados versionados como saída.

Este repositório representa somente a camada de Engenharia de Dados, com foco na aplicação da Privacidade Diferencial.

## 🎯 Objetivo

Fornecer conjuntos de dados privatizados que permitam:

  - Analisar o impacto da aplicação de Privacidade Diferencial sobre dados tabulares;

  - Comparar versões do mesmo dataset sob diferentes níveis de privacidade (ε);

  - Garantir reprodutibilidade e rastreabilidade do processo de privatização.

O pipeline foi projetado para tornar explícitos os parâmetros, decisões e limites da aplicação de Privacidade Diferencial.

## ⚙️ Responsabilidades do Pipeline

Este sistema é responsável por:

  - Extrair dados estruturados do banco de dados do sistema de RH;

  - Realizar limpeza e seleção de atributos relevantes;

  - Identificar atributos sensíveis e não sensíveis;

  - Aplicar mecanismos de Privacidade Diferencial com parâmetros configuráveis;

  - Gerar múltiplas versões do mesmo dataset (baseline e versões privatizadas);

  - Registrar metadados completos do processo de privatização;

  - Garantir execução determinística e reprodutível.

❌ O pipeline não:

  - Altera o banco de dados de origem;

  - Executa processamento em tempo real;

  - Realiza análises estatísticas ou modelagem sobre os dados.

## 🔐 Privacidade Diferencial

A Privacidade Diferencial é aplicada como uma etapa explícita do pipeline de preparação de dados.

Atualmente, o pipeline suporta:

  - Laplace Mechanism aplicado a atributos numéricos;

  - Clipping obrigatório baseado em limites definidos em configuração;

  - Sensibilidade controlada por atributo;

  - Execução determinística via uso de seed fixa.

Cada execução registra de forma explícita:

  - O mecanismo de privacidade utilizado;

  - Os valores de ε aplicados;

  - Os limites e sensibilidades por atributo.

## 🗂️ Versionamento de Dados

Os datasets gerados são versionados por execução do pipeline.

Exemplo de estrutura:

      datasets/
      └── v-YYYY-MM-DD_HH-MM-SS/
            ├── baseline.csv
            ├── dp_eps_0.1.csv
            ├── dp_eps_1.0.csv
            └── metadata.json


Cada versão representa:

  - Um estado específico dos dados extraídos do sistema de RH;

  - Um conjunto fechado e comparável de datasets;

  - Um registro completo dos parâmetros utilizados.

## 📥 Entrada e 📤 Saída de Dados

Entrada

Dados estruturados provenientes do Sistema de RH, incluindo, por exemplo:

  - Funcionários;

  - Setores;

  - Cargos;

  - Benefícios_Funcionários;

  - Avaliações;

  - Benefícios.

Saída

  - Dataset original (baseline);

  - Datasets privatizados por nível de ε;

Metadados da execução (parâmetros, mecanismo, versão).
## ▶️ Execução

O pipeline é executado de forma batch e sob demanda.

  - Não há execução automática ou contínua;

  - Uma nova versão de dataset só é criada quando o pipeline é explicitamente executado;

  - Mudanças no sistema de RH não afetam versões já geradas.

## 🎓 Motivação Acadêmica

A separação da aplicação de Privacidade Diferencial em um pipeline independente permite:

  - Isolamento claro da etapa de privatização;

  - Rigor metodológico;

  - Transparência no processo de geração dos dados;

  - Alinhamento com boas práticas de engenharia de dados e pesquisa acadêmica.

## ℹ️ Observações

  - Os dados utilizados são simulados e não representam indivíduos reais;

  - Este projeto possui finalidade acadêmica e experimental;

  - O foco está em clareza, reprodutibilidade e controle do processo.

## 📜 Licença

Uso acadêmico e educacional.

## Nota Final

Este repositório existe para tornar explícita, controlável e defensável a aplicação de Privacidade Diferencial sobre dados de RH.

Nada mais. Nada a menos.