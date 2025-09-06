from flask import Flask, request, jsonify
from database_mysql import init_db, execute_query, test_connection
from models import Imovel
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Testar conexão e inicializar banco ao iniciar a aplicação
# Pula a verificação se estiver em modo de teste (TESTING=True será definido pelos testes)
if not os.getenv('TESTING') and not app.config.get('TESTING'):
    if not test_connection():
        print("❌ Erro: Não foi possível conectar ao banco de dados MySQL!")
        print("💡 Configure o arquivo .env com as credenciais MySQL")
        exit(1)
    
    if not init_db():
        print("❌ Erro: Não foi possível inicializar o banco de dados!")
        exit(1)

def get_test_db_flag():
    """Verifica se deve usar banco de teste"""
    return app.config.get('TESTING', False)

@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    """Lista todos os imóveis"""
    imoveis = execute_query('SELECT * FROM imoveis ORDER BY id')
    
    if imoveis is None:
        return jsonify({'erro': 'Erro interno do servidor'}), 500
    
    return jsonify(imoveis)

@app.route('/imoveis/<int:id>', methods=['GET'])
def obter_imovel(id):
    """Obtém um imóvel específico pelo ID"""
    imoveis = execute_query('SELECT * FROM imoveis WHERE id = %s', (id,))
    
    if imoveis is None:
        return jsonify({'erro': 'Erro interno do servidor'}), 500
    
    if not imoveis:
        return jsonify({'erro': 'Imóvel não encontrado'}), 404
    
    return jsonify(imoveis[0])

@app.route('/imoveis', methods=['POST'])
def criar_imovel():
    """Adiciona um novo imóvel"""
    data = request.get_json()
    
    # Validação básica - apenas campos obrigatórios
    campos_obrigatorios = ['logradouro', 'cidade']
    for campo in campos_obrigatorios:
        if campo not in data or not data[campo]:
            return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
    
    try:
        query = '''
            INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        
        params = (
            data['logradouro'],
            data.get('tipo_logradouro'),
            data.get('bairro'),
            data['cidade'],
            data.get('cep'),
            data.get('tipo'),
            data.get('valor'),
            data.get('data_aquisicao')
        )
        
        imovel_id = execute_query(query, params)
        
        if imovel_id is None:
            return jsonify({'erro': 'Erro ao criar imóvel'}), 500
        
        return jsonify({'id': imovel_id, 'mensagem': 'Imóvel criado com sucesso'}), 201
        
    except Exception as e:
        print(f"Erro ao criar imóvel: {e}")
        return jsonify({'erro': 'Erro ao criar imóvel'}), 500

@app.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    """Atualiza um imóvel existente"""
    data = request.get_json()
    
    # Verificar se imóvel existe
    imovel_existente = execute_query('SELECT id FROM imoveis WHERE id = %s', (id,))
    
    if imovel_existente is None:
        return jsonify({'erro': 'Erro interno do servidor'}), 500
    
    if not imovel_existente:
        return jsonify({'erro': 'Imóvel não encontrado'}), 404
    
    # Construir query de atualização dinamicamente
    campos_update = []
    valores = []
    
    campos_permitidos = ['logradouro', 'tipo_logradouro', 'bairro', 'cidade', 'cep', 'tipo', 'valor', 'data_aquisicao']
    
    for campo in campos_permitidos:
        if campo in data:
            campos_update.append(f'{campo} = %s')
            valores.append(data[campo])
    
    if not campos_update:
        return jsonify({'erro': 'Nenhum campo para atualizar'}), 400
    
    valores.append(id)
    query = f'UPDATE imoveis SET {", ".join(campos_update)} WHERE id = %s'
    
    result = execute_query(query, valores)
    
    if result is None:
        return jsonify({'erro': 'Erro ao atualizar imóvel'}), 500
    
    return jsonify({'mensagem': 'Imóvel atualizado com sucesso'})

@app.route('/imoveis/<int:id>', methods=['DELETE'])
def deletar_imovel(id):
    """Remove um imóvel"""
    result = execute_query('DELETE FROM imoveis WHERE id = %s', (id,))
    
    if result is None:
        return jsonify({'erro': 'Erro interno do servidor'}), 500
    
    if result == 0:
        return jsonify({'erro': 'Imóvel não encontrado'}), 404
    
    return jsonify({'mensagem': 'Imóvel removido com sucesso'})

@app.route('/imoveis/tipo/<tipo>', methods=['GET'])
def listar_por_tipo(tipo):
    """Lista imóveis por tipo"""
    imoveis = execute_query('SELECT * FROM imoveis WHERE tipo = %s ORDER BY id', (tipo,))
    
    if imoveis is None:
        return jsonify({'erro': 'Erro interno do servidor'}), 500
    
    return jsonify(imoveis)

@app.route('/imoveis/cidade/<cidade>', methods=['GET'])
def listar_por_cidade(cidade):
    """Lista imóveis por cidade"""
    imoveis = execute_query('SELECT * FROM imoveis WHERE cidade = %s ORDER BY id', (cidade,))
    
    if imoveis is None:
        return jsonify({'erro': 'Erro interno do servidor'}), 500
    
    return jsonify(imoveis)

@app.route('/health', methods=['GET'])
def health_check():
    """Verifica status da API e banco"""
    if test_connection():
        return jsonify({
            'status': 'OK',
            'database': 'MySQL Connected',
            'message': 'API funcionando corretamente'
        })
    else:
        return jsonify({
            'status': 'ERROR',
            'database': 'MySQL Disconnected',
            'message': 'Problema na conexão com o banco'
        }), 500

@app.route('/debug', methods=['GET'])
def debug_database():
    """Endpoint de debug para verificar o banco"""
    try:
        # Verificar se a tabela existe
        tables = execute_query("SHOW TABLES")
        
        # Contar registros na tabela imoveis
        count = execute_query("SELECT COUNT(*) as total FROM imoveis")
        
        # Mostrar estrutura da tabela
        structure = execute_query("DESCRIBE imoveis")
        
        return jsonify({
            'tabelas': tables,
            'total_imoveis': count,
            'estrutura_tabela': structure,
            'status': 'OK'
        })
    except Exception as e:
        return jsonify({
            'erro': str(e),
            'status': 'ERROR'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'erro': 'Rota não encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'erro': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True)