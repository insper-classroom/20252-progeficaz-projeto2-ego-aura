from flask import Flask, request, jsonify
from database import init_db, get_db_connection
from models import Imovel

app = Flask(__name__)

# Inicializar banco ao iniciar a aplicação
init_db()

def get_db():
    """Obtém conexão com o banco, usando configuração de teste se disponível"""
    database_name = app.config.get('DATABASE')
    return get_db_connection(database_name)

@app.route('/imoveis', methods=['GET'])
def listar_imoveis():
    """Lista todos os imóveis"""
    conn = get_db()
    imoveis = conn.execute('SELECT * FROM imoveis').fetchall()
    conn.close()
    
    return jsonify([dict(imovel) for imovel in imoveis])

@app.route('/imoveis/<int:id>', methods=['GET'])
def obter_imovel(id):
    """Obtém um imóvel específico pelo ID"""
    conn = get_db()
    imovel = conn.execute('SELECT * FROM imoveis WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if imovel is None:
        return jsonify({'erro': 'Imóvel não encontrado'}), 404
    
    return jsonify(dict(imovel))

@app.route('/imoveis', methods=['POST'])
def criar_imovel():
    """Adiciona um novo imóvel"""
    data = request.get_json()
    
    # Validação básica - apenas campos obrigatórios
    campos_obrigatorios = ['logradouro', 'cidade']
    for campo in campos_obrigatorios:
        if campo not in data:
            return jsonify({'erro': f'Campo {campo} é obrigatório'}), 400
    
    try:
        conn = get_db()
        cursor = conn.execute('''
            INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['logradouro'], data.get('tipo_logradouro'), data.get('bairro'), 
              data['cidade'], data.get('cep'), data.get('tipo'), 
              data.get('valor'), data.get('data_aquisicao')))
        
        conn.commit()
        imovel_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': imovel_id, 'mensagem': 'Imóvel criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'erro': 'Erro ao criar imóvel'}), 500

@app.route('/imoveis/<int:id>', methods=['PUT'])
def atualizar_imovel(id):
    """Atualiza um imóvel existente"""
    data = request.get_json()
    
    conn = get_db()
    # Verificar se imóvel existe
    imovel_existente = conn.execute('SELECT * FROM imoveis WHERE id = ?', (id,)).fetchone()
    
    if imovel_existente is None:
        conn.close()
        return jsonify({'erro': 'Imóvel não encontrado'}), 404
    
    # Atualizar campos fornecidos
    campos_update = []
    valores = []
    
    for campo in ['logradouro', 'tipo_logradouro', 'bairro', 'cidade', 'cep', 'tipo', 'valor', 'data_aquisicao']:
        if campo in data:
            campos_update.append(f'{campo} = ?')
            valores.append(data[campo])
    
    if campos_update:
        query = f'UPDATE imoveis SET {", ".join(campos_update)} WHERE id = ?'
        valores.append(id)
        conn.execute(query, valores)
        conn.commit()
    
    conn.close()
    return jsonify({'mensagem': 'Imóvel atualizado com sucesso'})

@app.route('/imoveis/<int:id>', methods=['DELETE'])
def deletar_imovel(id):
    """Remove um imóvel"""
    conn = get_db()
    cursor = conn.execute('DELETE FROM imoveis WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    if cursor.rowcount == 0:
        return jsonify({'erro': 'Imóvel não encontrado'}), 404
    
    return jsonify({'mensagem': 'Imóvel removido com sucesso'})

@app.route('/imoveis/tipo/<tipo>', methods=['GET'])
def listar_por_tipo(tipo):
    """Lista imóveis por tipo"""
    conn = get_db()
    imoveis = conn.execute('SELECT * FROM imoveis WHERE tipo = ?', (tipo,)).fetchall()
    conn.close()
    
    return jsonify([dict(imovel) for imovel in imoveis])

@app.route('/imoveis/cidade/<cidade>', methods=['GET'])
def listar_por_cidade(cidade):
    """Lista imóveis por cidade"""
    conn = get_db()
    imoveis = conn.execute('SELECT * FROM imoveis WHERE cidade = ?', (cidade,)).fetchall()
    conn.close()
    
    return jsonify([dict(imovel) for imovel in imoveis])

@app.errorhandler(404)
def not_found(error):
    return jsonify({'erro': 'Rota não encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'erro': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True)
