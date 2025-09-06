# Collection Postman - Imóveis API

Esta collection contém todos os 2. **Listar Imóveis**: Veja os dados existentes
3. **Criar Imóvel**: Adicione novos dados
4. **Buscar por ID**: Teste busca específica
5. **Atualizar**: Modifique um imóvel existente
6. **Buscar por Tipo/Cidade**: Teste filtros
7. **Deletar**: Remova um imóvel
8. **Testes de Erro**: Verifique tratamento de errosts para testar a API de gerenciamento de imóveis.

## Como Importar no Postman

### 1. Importar a Collection
1. Abra o Postman
2. Clique em "Import" no canto superior esquerdo
3. Selecione o arquivo `Imoveis_API.postman_collection.json`
4. Clique em "Import"

### 2. Importar o Environment (Opcional)
1. No Postman, clique no ícone de engrenagem (Settings) no canto superior direito
2. Selecione "Manage Environments"
3. Clique em "Import"
4. Selecione o arquivo `Imoveis_API_Local.postman_environment.json`
5. Ative o environment "Imóveis API - Local" no dropdown no canto superior direito

## Endpoints Disponíveis

### Health Check
- **GET /health** - Verifica status da API e conexão com banco

### CRUD de Imóveis
- **GET /imoveis** - Lista todos os imóveis
- **GET /imoveis/{id}** - Busca imóvel por ID
- **POST /imoveis** - Cria novo imóvel
- **PUT /imoveis/{id}** - Atualiza imóvel existente
- **DELETE /imoveis/{id}** - Remove imóvel

### Consultas Específicas
- **GET /imoveis/tipo/{tipo}** - Busca imóveis por tipo
- **GET /imoveis/cidade/{cidade}** - Busca imóveis por cidade

### Testes de Erro
- Requests para testar cenários de erro (404, dados inválidos, etc.)

## Estrutura do Imóvel

```json
{
    "logradouro": "Rua das Flores, 123",
    "tipo_logradouro": "Rua",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "cep": "01234-567",
    "tipo": "Apartamento",
    "valor": 350000.00,
    "data_aquisicao": "2024-01-15"
}
```

## Configuração

### URL Base
Por padrão, a collection está configurada para usar `http://127.0.0.1:5000`. 

Se a API estiver rodando em uma porta diferente, você pode:
1. Usar o environment e alterar a variável `base_url`
2. Ou editar diretamente nas requests

### Antes de Testar
1. Certifique-se de que a API está rodando (`python app.py`)
2. Configure o arquivo `.env` com as credenciais do MySQL
3. Verifique se o banco de dados está acessível

## Sequência de Testes Sugerida

1. **Health Check**: Verifique se a API está funcionando
2. **Listar Imóveis**: Veja os dados existentes
4. **Criar Imóvel**: Adicione novos dados
5. **Buscar por ID**: Teste busca específica
6. **Atualizar**: Modifique um imóvel existente
7. **Buscar por Tipo/Cidade**: Teste filtros
8. **Deletar**: Remova um imóvel
9. **Testes de Erro**: Verifique tratamento de erros

## Tipos de Imóveis Sugeridos
- Apartamento
- Casa
- Terreno
- Sobrado
- Kitnet
- Loft
- Cobertura

## Exemplos de Dados para Teste

### Apartamento
```json
{
    "logradouro": "Avenida Paulista, 1000",
    "tipo_logradouro": "Avenida",
    "bairro": "Bela Vista",
    "cidade": "São Paulo",
    "cep": "01310-100",
    "tipo": "Apartamento",
    "valor": 450000.00,
    "data_aquisicao": "2024-03-15"
}
```

### Casa
```json
{
    "logradouro": "Rua das Palmeiras, 456",
    "tipo_logradouro": "Rua",
    "bairro": "Vila Madalena",
    "cidade": "São Paulo",
    "cep": "05435-010",
    "tipo": "Casa",
    "valor": 850000.00,
    "data_aquisicao": "2024-02-20"
}
```

### Terreno
```json
{
    "logradouro": "Estrada do Campo, 789",
    "tipo_logradouro": "Estrada",
    "bairro": "Zona Rural",
    "cidade": "Campinas",
    "cep": "13000-000",
    "tipo": "Terreno",
    "valor": 120000.00,
    "data_aquisicao": "2024-01-10"
}
```
