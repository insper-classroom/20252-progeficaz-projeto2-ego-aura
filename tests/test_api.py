import pytest
import json
import os
import tempfile
from app import app
from database import init_db, clear_db

@pytest.fixture
def client():
    """Configura um cliente de teste Flask"""
    # Usar um banco de dados temporário para testes
    db_fd, db_path = tempfile.mkstemp()
    app.config['DATABASE'] = db_path
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            init_db(db_path)
        yield client
    
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def sample_imovel():
    """Dados de exemplo para um imóvel"""
    return {
        'logradouro': 'Rua das Flores, 123',
        'tipo_logradouro': 'Rua',
        'bairro': 'Centro',
        'cidade': 'São Paulo',
        'cep': '01234-567',
        'tipo': 'apartamento',
        'valor': 350000.0,
        'data_aquisicao': '2024-01-15'
    }

class TestImoveis:
    
    def test_listar_imoveis_vazio(self, client):
        """Testa listagem quando não há imóveis"""
        response = client.get('/imoveis')
        assert response.status_code == 200
        assert json.loads(response.data) == []
    
    def test_criar_imovel(self, client, sample_imovel):
        """Testa criação de um novo imóvel"""
        response = client.post('/imoveis', 
                              data=json.dumps(sample_imovel),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'id' in data
        assert data['mensagem'] == 'Imóvel criado com sucesso'
    
    def test_criar_imovel_sem_campos_obrigatorios(self, client):
        """Testa criação de imóvel sem campos obrigatórios"""
        imovel_incompleto = {'tipo': 'casa'}
        
        response = client.post('/imoveis',
                              data=json.dumps(imovel_incompleto),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'erro' in data
    
    def test_obter_imovel_existente(self, client, sample_imovel):
        """Testa obtenção de um imóvel específico"""
        # Primeiro, criar um imóvel
        response = client.post('/imoveis',
                              data=json.dumps(sample_imovel),
                              content_type='application/json')
        imovel_id = json.loads(response.data)['id']
        
        # Agora, obter o imóvel
        response = client.get(f'/imoveis/{imovel_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['tipo'] == sample_imovel['tipo']
        assert data['cidade'] == sample_imovel['cidade']
        assert data['valor'] == sample_imovel['valor']
    
    def test_obter_imovel_inexistente(self, client):
        """Testa obtenção de um imóvel que não existe"""
        response = client.get('/imoveis/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['erro'] == 'Imóvel não encontrado'
    
    def test_atualizar_imovel(self, client, sample_imovel):
        """Testa atualização de um imóvel"""
        # Criar um imóvel
        response = client.post('/imoveis',
                              data=json.dumps(sample_imovel),
                              content_type='application/json')
        imovel_id = json.loads(response.data)['id']
        
        # Atualizar o imóvel
        atualizacao = {'valor': 400000.0, 'bairro': 'Vila Madalena'}
        response = client.put(f'/imoveis/{imovel_id}',
                             data=json.dumps(atualizacao),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['mensagem'] == 'Imóvel atualizado com sucesso'
        
        # Verificar se a atualização foi aplicada
        response = client.get(f'/imoveis/{imovel_id}')
        data = json.loads(response.data)
        assert data['valor'] == 400000.0
        assert data['bairro'] == 'Vila Madalena'
    
    def test_atualizar_imovel_inexistente(self, client):
        """Testa atualização de um imóvel que não existe"""
        atualizacao = {'valor': 400000.0}
        response = client.put('/imoveis/999',
                             data=json.dumps(atualizacao),
                             content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['erro'] == 'Imóvel não encontrado'
    
    def test_deletar_imovel(self, client, sample_imovel):
        """Testa remoção de um imóvel"""
        # Criar um imóvel
        response = client.post('/imoveis',
                              data=json.dumps(sample_imovel),
                              content_type='application/json')
        imovel_id = json.loads(response.data)['id']
        
        # Deletar o imóvel
        response = client.delete(f'/imoveis/{imovel_id}')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['mensagem'] == 'Imóvel removido com sucesso'
        
        # Verificar se foi realmente removido
        response = client.get(f'/imoveis/{imovel_id}')
        assert response.status_code == 404
    
    def test_deletar_imovel_inexistente(self, client):
        """Testa remoção de um imóvel que não existe"""
        response = client.delete('/imoveis/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert data['erro'] == 'Imóvel não encontrado'
    
    def test_listar_por_tipo(self, client, sample_imovel):
        """Testa listagem de imóveis por tipo"""
        # Criar alguns imóveis de tipos diferentes
        apartamento = sample_imovel.copy()
        apartamento['tipo'] = 'apartamento'
        
        casa = sample_imovel.copy()
        casa['tipo'] = 'casa'
        casa['logradouro'] = 'Rua das Casas, 456'
        
        client.post('/imoveis', data=json.dumps(apartamento), content_type='application/json')
        client.post('/imoveis', data=json.dumps(casa), content_type='application/json')
        
        # Listar apenas apartamentos
        response = client.get('/imoveis/tipo/apartamento')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['tipo'] == 'apartamento'
    
    def test_listar_por_cidade(self, client, sample_imovel):
        """Testa listagem de imóveis por cidade"""
        # Criar imóveis em cidades diferentes
        sp_imovel = sample_imovel.copy()
        sp_imovel['cidade'] = 'São Paulo'
        
        rj_imovel = sample_imovel.copy()
        rj_imovel['cidade'] = 'Rio de Janeiro'
        rj_imovel['logradouro'] = 'Avenida Copacabana, 789'
        
        client.post('/imoveis', data=json.dumps(sp_imovel), content_type='application/json')
        client.post('/imoveis', data=json.dumps(rj_imovel), content_type='application/json')
        
        # Listar apenas imóveis de São Paulo
        response = client.get('/imoveis/cidade/São Paulo')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['cidade'] == 'São Paulo'
    
    def test_listar_todos_imoveis(self, client, sample_imovel):
        """Testa listagem de todos os imóveis"""
        # Criar vários imóveis
        for i in range(3):
            imovel = sample_imovel.copy()
            imovel['logradouro'] = f'Rua {i}, {i*100}'
            client.post('/imoveis', data=json.dumps(imovel), content_type='application/json')
        
        # Listar todos
        response = client.get('/imoveis')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert len(data) == 3
