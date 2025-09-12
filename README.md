# API REST Imobiliária

Uma API REST completa para gerenciar imóveis de uma empresa imobiliária, desenvolvida com Flask e MySQL.

A API estará disponível em `http://3.82.36.224:5000`

## Funcionalidades

- Listar todos os imóveis
- Obter um imóvel específico por ID
- Criar novo imóvel
- Atualizar imóvel existente
- Remover imóvel
- Listar imóveis por tipo
- Listar imóveis por cidade
- Testes automatizados completos

## Estrutura do Projeto

```
projeto2/
├── app.py                              # Aplicação Flask principal com todas as rotas da API
├── database.py                         # Configuração e funções do banco de dados SQLite
├── database_mysql.py                   # Configuração e funções do banco de dados MySQL
├── models.py                           # Modelo de dados do imóvel
├── criar_banco.py                      # Script para criar e popular o banco
├── requirements.txt                    # Dependências do projeto
├── .env.example                        # Exemplo de arquivo de configuração de ambiente
├── .gitignore                          # Arquivos ignorados pelo Git
├── imoveis.sql                         # Arquivo original com estrutura e dados
├── Imoveis_API.postman_collection.json # Coleção do Postman para testes da API
├── POSTMAN_COLLECTION.md               # Documentação da coleção do Postman
└── tests/
    ├── __init__.py                     # Torna o diretório um pacote Python
    └── test_api.py                     # Testes automatizados da API
```

## Instalação e Execução

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```
2. **Execute a aplicação:**
```bash
python app.py
```

## Executar Testes

```bash
pytest tests/ -v
```

## Endpoints da API

### Listar todos os imóveis
- **GET** `/imoveis`
- Retorna: Lista de todos os imóveis

### Obter imóvel específico
- **GET** `/imoveis/<id>`
- Retorna: Dados do imóvel com o ID especificado

### Criar novo imóvel
- **POST** `/imoveis`
- Body (JSON):
```json
{
    "logradouro": "Rua das Flores, 123",
    "tipo_logradouro": "Rua",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "cep": "01234-567",
    "tipo": "apartamento",
    "valor": 350000.0,
    "data_aquisicao": "2024-01-15"
}
```

### Atualizar imóvel
- **PUT** `/imoveis/<id>`
- Body (JSON): Campos a serem atualizados

### Remover imóvel
- **DELETE** `/imoveis/<id>`

### Listar por tipo
- **GET** `/imoveis/tipo/<tipo>`
- Exemplo: `/imoveis/tipo/apartamento`

### Listar por cidade
- **GET** `/imoveis/cidade/<cidade>`
- Exemplo: `/imoveis/cidade/São Paulo`

## Estrutura do Banco de Dados

A tabela `imoveis` possui os seguintes campos:
- `id` (INTEGER, PRIMARY KEY)
- `logradouro` (TEXT, NOT NULL)
- `tipo_logradouro` (TEXT, opcional)
- `bairro` (TEXT, opcional)
- `cidade` (TEXT, NOT NULL)
- `cep` (TEXT, opcional)
- `tipo` (TEXT, opcional)
- `valor` (REAL, opcional)
- `data_aquisicao` (TEXT, opcional)

## Testes Automatizados

Todos os 12 testes passam com sucesso:
- Teste de listagem vazia
- Teste de criação de imóvel
- Teste de validação de campos obrigatórios
- Teste de obtenção de imóvel existente/inexistente
- Teste de atualização de imóvel existente/inexistente
- Teste de remoção de imóvel existente/inexistente
- Teste de listagem por tipo
- Teste de listagem por cidade
- Teste de listagem geral

## Tecnologias Utilizadas

- **Framework:** Flask 2.3.3
- **Banco de Dados:** MySQL
- **Testes:** pytest 7.4.2
- **HTTP Client:** requests (para demonstrações)

## Características

- Framework Flask
- Banco MySQL com dados reais
- Estrutura simples e funcional
- Testes automatizados completos
- Documentação clara
- Adaptado ao arquivo imoveis.sql fornecido
- Validação de dados
- Tratamento de erros
- API RESTful completa
- Script de criação do banco
- Coleção do Postman para testes

## Notas de Implementação

Este projeto foi desenvolvido seguindo os requisitos do segundo projeto de Programação Eficaz, implementando uma API REST completa para gerenciamento de imóveis com todas as operações CRUD e funcionalidades de filtro por tipo e cidade.
