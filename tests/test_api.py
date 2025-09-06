import pytest
import json
import os
import sys
from dotenv import load_dotenv

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database_mysql import init_db, clear_db

# Carregar variáveis de ambiente
load_dotenv()

@pytest.fixture
def client():
    """Configura o cliente de teste do Flask"""
    app.config['TESTING'] = True
    
    # Limpar dados antes de cada teste
    clear_db()
    
    with app.test_client() as client:
        yield client
    
    # Limpar dados após cada teste para manter isolamento
    clear_db()

@pytest.fixture
def imovel_exemplo():
    """Retorna dados de exemplo para um imóvel"""
    return {
        'logradouro': 'Rua Teste, 123',
        'tipo_logradouro': 'Rua',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'cep': '01234-567',
        'tipo': 'apartamento',
        'valor': 300000.50,
        'data_aquisicao': '2023-01-15'
    }

def test_health_check(client):
    """Testa endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'OK'
    assert 'MySQL' in data['database']

def test_listar_imoveis_vazio(client):
    """Testa listagem quando não há imóveis"""
    response = client.get('/imoveis')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == []

def test_criar_imovel(client, imovel_exemplo):
    """Testa criação de um novo imóvel"""
    response = client.post('/imoveis', 
                          data=json.dumps(imovel_exemplo),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data
    assert data['mensagem'] == 'Imóvel criado com sucesso'

def test_criar_imovel_campos_obrigatorios(client):
    """Testa criação com campos obrigatórios faltando"""
    imovel_incompleto = {'logradouro': 'Rua Teste'}
    
    response = client.post('/imoveis',
                          data=json.dumps(imovel_incompleto),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'erro' in data

def test_obter_imovel(client, imovel_exemplo):
    """Testa obtenção de um imóvel específico"""
    # Primeiro, criar um imóvel
    response = client.post('/imoveis',
                          data=json.dumps(imovel_exemplo),
                          content_type='application/json')
    assert response.status_code == 201
    imovel_id = json.loads(response.data)['id']
    
    # Depois, obter o imóvel
    response = client.get(f'/imoveis/{imovel_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['logradouro'] == imovel_exemplo['logradouro']
    assert data['cidade'] == imovel_exemplo['cidade']

def test_obter_imovel_inexistente(client):
    """Testa obtenção de imóvel que não existe"""
    response = client.get('/imoveis/999999')  # ID muito alto para não existir
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['erro'] == 'Imóvel não encontrado'

def test_atualizar_imovel(client, imovel_exemplo):
    """Testa atualização de um imóvel"""
    # Criar imóvel
    response = client.post('/imoveis',
                          data=json.dumps(imovel_exemplo),
                          content_type='application/json')
    assert response.status_code == 201
    imovel_id = json.loads(response.data)['id']
    
    # Atualizar imóvel
    dados_atualizacao = {'valor': 350000.00, 'bairro': 'Vila Nova'}
    response = client.put(f'/imoveis/{imovel_id}',
                         data=json.dumps(dados_atualizacao),
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['mensagem'] == 'Imóvel atualizado com sucesso'
    
    # Verificar se a atualização foi aplicada
    response = client.get(f'/imoveis/{imovel_id}')
    data = json.loads(response.data)
    assert data['valor'] == 350000.00
    assert data['bairro'] == 'Vila Nova'

def test_atualizar_imovel_inexistente(client):
    """Testa atualização de imóvel que não existe"""
    dados_atualizacao = {'valor': 350000.00}
    response = client.put('/imoveis/999999',  # ID muito alto para não existir
                         data=json.dumps(dados_atualizacao),
                         content_type='application/json')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['erro'] == 'Imóvel não encontrado'

def test_deletar_imovel(client, imovel_exemplo):
    """Testa remoção de um imóvel"""
    # Criar imóvel
    response = client.post('/imoveis',
                          data=json.dumps(imovel_exemplo),
                          content_type='application/json')
    assert response.status_code == 201
    imovel_id = json.loads(response.data)['id']
    
    # Deletar imóvel
    response = client.delete(f'/imoveis/{imovel_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['mensagem'] == 'Imóvel removido com sucesso'
    
    # Verificar se foi realmente removido
    response = client.get(f'/imoveis/{imovel_id}')
    assert response.status_code == 404

def test_deletar_imovel_inexistente(client):
    """Testa remoção de imóvel que não existe"""
    response = client.delete('/imoveis/999999')  # ID muito alto para não existir
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['erro'] == 'Imóvel não encontrado'

def test_listar_por_tipo(client, imovel_exemplo):
    """Testa listagem de imóveis por tipo"""
    # Criar alguns imóveis
    response1 = client.post('/imoveis', data=json.dumps(imovel_exemplo), content_type='application/json')
    assert response1.status_code == 201
    
    imovel_casa = imovel_exemplo.copy()
    imovel_casa['tipo'] = 'casa'
    imovel_casa['logradouro'] = 'Rua das Casas, 456'
    response2 = client.post('/imoveis', data=json.dumps(imovel_casa), content_type='application/json')
    assert response2.status_code == 201
    
    # Listar por tipo
    response = client.get('/imoveis/tipo/apartamento')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['tipo'] == 'apartamento'

def test_listar_por_cidade(client, imovel_exemplo):
    """Testa listagem de imóveis por cidade"""
    # Criar alguns imóveis
    response1 = client.post('/imoveis', data=json.dumps(imovel_exemplo), content_type='application/json')
    assert response1.status_code == 201
    
    imovel_rj = imovel_exemplo.copy()
    imovel_rj['cidade'] = 'Rio de Janeiro'
    imovel_rj['logradouro'] = 'Rua Carioca, 789'
    response2 = client.post('/imoveis', data=json.dumps(imovel_rj), content_type='application/json')
    assert response2.status_code == 201
    
    # Listar por cidade
    response = client.get('/imoveis/cidade/São Paulo')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['cidade'] == 'São Paulo'

def test_listar_todos_imoveis(client, imovel_exemplo):
    """Testa listagem de todos os imóveis"""
    # Criar vários imóveis
    for i in range(3):
        imovel = imovel_exemplo.copy()
        imovel['logradouro'] = f'Rua {i}, {i*100}'
        response = client.post('/imoveis', data=json.dumps(imovel), content_type='application/json')
        assert response.status_code == 201
    
    # Listar todos
    response = client.get('/imoveis')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3