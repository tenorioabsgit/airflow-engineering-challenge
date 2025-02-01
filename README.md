# Desafio Técnico - Engenharia de Dados com Airflow

## Visão Geral
Este projeto implementa um pipeline de ETL usando Apache Airflow, PostgreSQL e Docker.

## Tecnologias Utilizadas
- Apache Airflow (Orquestração)
- PostgreSQL (Banco de Dados)
- Docker & Docker Compose (Gerenciamento de Containers)
- Python (Extração e Transformação de Dados)

## Estrutura das Camadas
- Raw: Armazena os dados brutos extraídos da API.
- Stage: Estruturação dos dados em tabelas intermediárias no PostgreSQL.
- Trusted: Dados processados e prontos para análise.

## Como Rodar o Projeto
1. Clone o repositório:
   ```bash
   git clone <seu-repositorio>
   cd airflow-engineering-challenge
   ```

2. Inicie os containers:
   ```bash
   docker-compose up --build -d
   ```

3. Acesse o Airflow:
   - URL: [http://localhost:8080](http://localhost:8080)
   - Usuário: airflow
   - Senha: airflow

4. Execute as DAGs na seguinte ordem:
   - extract_products → Extrai os dados da API e salva na camada Raw.
   - load_stage → Carrega os dados para a camada Stage no PostgreSQL.
   - load_trusted → Agrega os dados na camada Trusted.

## Consultas no PostgreSQL
- Verificar a camada Stage:
  ```sql
  SELECT * FROM stage.products;
  ```
- Verificar a camada Trusted:
  ```sql
  SELECT * FROM trusted.product_sales_daily;
  ```

## Observações
- A API utiliza autenticação via JWT, então é necessário renovar o token caso expire.
- A DAG foi configurada para rodar diariamente, mas pode ser acionada manualmente no Airflow.

## Estrutura do Projeto
```
/airflow-engineering-challenge
├── dags/
│   ├── extract_products.py  # DAG para extração
│   ├── load_stage.py        # DAG para carga na camada Stage
│   ├── load_trusted.py      # DAG para carga na camada Trusted
├── local_storage/
│   ├── raw/                 # Armazena dados brutos da API
├── api/
│   ├── main.py              # API Fake de produtos
│   ├── models.py            # Modelos de dados
│   ├── seed_data.py         # Script de população da API
├── docker-compose.yml        # Configuração do ambiente
├── README.md                 # Documentação
```

## Problemas e Soluções
- DAGs não aparecendo no Airflow: Verificar se os arquivos estão no diretório correto (dags/) e reiniciar o Airflow.
- Erro ao conectar ao PostgreSQL: Certifique-se de que os containers estão rodando e de que o PostgreSQL está acessível na rede do Docker.
- Token JWT expirado: Utilize o endpoint /refresh-token para obter um novo token.

## Melhorias Futuras
- Adicionar testes automatizados para DAGs
- Criar um dashboard no Metabase para visualizar os dados Trusted
- Implementar o DBT para transformação de dados

Projeto concluído com sucesso


