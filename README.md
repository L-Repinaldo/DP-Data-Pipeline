# DP-Data-Pipeline
Camada de Engenharia de Dados para Privacidade Diferencial
## 📌 Visão Geral

Este repositório contém o sistema intermediário de engenharia de dados do projeto IC Privacidade.
Seu papel é realizar a extração, preparação e privatização de dados provenientes de um sistema transacional de Recursos Humanos, aplicando Privacidade Diferencial (DP) de forma controlada, versionada e reproduzível.

O pipeline foi projetado para isolar a aplicação da privacidade diferencial como variável experimental, garantindo clareza metodológica e separação de responsabilidades entre os sistemas envolvidos.

## 🏗️ Arquitetura do Projeto

O projeto completo é composto por três sistemas independentes:

1. Projeto A — Sistema de RH (OLTP)

    - Geração de dados limpos, consistentes e realistas
    
    - Não aplica Privacidade Diferencial

2. Projeto Intermediário — DP Data Pipeline (este repositório)

    - Extração de dados do RH
    
    - Aplicação de mecanismos de Privacidade Diferencial
    
    - Versionamento de datasets

3. Projeto B — Machine Learning e Ataques de Inferência

    - Consumo dos datasets gerados
    
    - Avaliação de utilidade, vazamento e trade-offs

👉 Este repositório representa exclusivamente a camada de Engenharia de Dados.

## 🎯 Objetivo

Fornecer conjuntos de dados privatizados que permitam avaliar, de forma experimental e reproduzível:

  - o impacto da Privacidade Diferencial na utilidade estatística dos dados;
  
  - o efeito do ruído na performance de modelos de Machine Learning;
  
  - a resistência dos dados a ataques de inferência e reidentificação.

## ⚙️ Responsabilidades do Pipeline

Este sistema é responsável por:

  - Extrair dados estruturados do banco do sistema de RH;
  
  - Selecionar atributos sensíveis e não sensíveis;
  
  - Aplicar mecanismos de Privacidade Diferencial com parâmetros configuráveis (ε);
  
  - Gerar múltiplas versões do mesmo dataset (baseline e datasets privatizados);
  
  - Registrar metadados do processo de privatização;
  
  - Garantir reprodutibilidade dos experimentos.

❌ O pipeline não:

  - treina modelos de Machine Learning;
  
  - executa ataques de inferência;
  
  - altera o banco de dados de origem.

## 🔐 Privacidade Diferencial

A Privacidade Diferencial é aplicada como etapa de preparação de dados, antes do uso em Machine Learning.

Mecanismos avaliados podem incluir:

  - Laplace Mechanism
  
  - Gaussian Mechanism
  
  - Perturbação de atributos e/ou labels

Cada execução registra explicitamente:

  - o mecanismo utilizado;
  
  - os valores de ε;
  
  - a versão do dataset gerado.

## 🗂️ Versionamento de Dados

Os datasets são versionados por execução, permitindo comparações entre diferentes estados do sistema de origem.

Exemplo de estrutura:

    datasets/
     ├── v1/
     │    ├── baseline.csv
     │    ├── dp_eps_0.1.csv
     │    └── dp_eps_1.0.csv
     ├── v2/
     │    ├── baseline.csv
     │    ├── dp_eps_0.1.csv
     │    └── dp_eps_1.0.csv


Cada versão representa:

  - um estado específico do banco do RH;
  
  - um conjunto fechado e comparável de experimentos.

## 📥 Entrada e 📤 Saída de Dados

Entrada

Dados estruturados provenientes do sistema de RH:
  
  - funcionários
  
  - setores
  
  - avaliações
  
  - benefícios

Saída
  
  - Dataset original (baseline);
  
  - Datasets privatizados por nível de ε;
  
  - Metadados da execução (parâmetros, data, versão).

## ▶️ Execução

O pipeline é executado de forma batch e sob demanda.

  - Não há execução contínua;
  
  - Não há dependência em tempo real entre os sistemas.

Mudanças no sistema de RH não afetam automaticamente os experimentos de ML.
Uma nova versão de dataset só é criada quando o pipeline é explicitamente executado.

🤖 Relação com o Projeto de Machine Learning

O Projeto B consome explicitamente uma versão definida dos datasets gerados por este pipeline.

Isso garante que os experimentos sejam:

  - reproduzíveis;
  
  - comparáveis;
  
  - independentes da evolução do sistema de origem.

## 🎓 Motivação Acadêmica

A separação da camada de Privacidade Diferencial em um sistema independente permite:

  - isolamento da variável experimental;
  
  - rigor metodológico;
  
  - alinhamento com boas práticas de engenharia de dados e pesquisa científica.

## ℹ️ Observações

  - Os dados utilizados são simulados e não representam indivíduos reais;
  
  - Este projeto é desenvolvido para fins acadêmicos e de pesquisa;
  
  - O foco está em clareza experimental, não em conveniência de execução imediata.

## 📜 Licença

Uso acadêmico e educacional.

## Nota Final

Este repositório não existe para “facilitar” o Machine Learning,
ele existe para tornar o experimento correto, reproduzível e defensável.

Isso é intencional.
