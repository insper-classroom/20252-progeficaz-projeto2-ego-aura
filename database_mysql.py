import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def get_db_connection(test_db=False):
    """Cria uma conexão com o banco de dados MySQL"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            port=int(os.getenv('MYSQL_PORT', 3306)),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_TEST_DATABASE' if test_db else 'MYSQL_DATABASE'),
            charset=os.getenv('MYSQL_CHARSET', 'utf8mb4'),
            autocommit=True
        )
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def init_db(test_db=False):
    """Inicializa o banco de dados criando a tabela de imóveis"""
    connection = get_db_connection(test_db)
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS imoveis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                logradouro TEXT NOT NULL,
                tipo_logradouro TEXT,
                bairro TEXT,
                cidade TEXT NOT NULL,
                cep VARCHAR(10),
                tipo VARCHAR(50),
                valor DECIMAL(15,2),
                data_aquisicao DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        ''')
        
        print("Tabela 'imoveis' criada com sucesso!")
        return True
        
    except Error as e:
        print(f"Erro ao criar tabela: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def clear_db(test_db=False):
    """Limpa todos os dados da tabela (útil para testes)"""
    connection = get_db_connection(test_db)
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM imoveis')
        cursor.execute('ALTER TABLE imoveis AUTO_INCREMENT = 1')  # Reset auto increment
        return True
        
    except Error as e:
        print(f"Erro ao limpar tabela: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def execute_query(query, params=None, test_db=False):
    """Executa uma query no banco de dados"""
    connection = get_db_connection(test_db)
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
            # Converter Decimal para float para consistência com JSON
            for row in result:
                for key, value in row.items():
                    if hasattr(value, '__float__'):  # Se é um tipo numérico (como Decimal)
                        try:
                            row[key] = float(value)
                        except (ValueError, TypeError):
                            pass  # Manter o valor original se não conseguir converter
        else:
            result = cursor.lastrowid if cursor.lastrowid else cursor.rowcount
            
        return result
        
    except Error as e:
        print(f"Erro ao executar query: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def test_connection():
    """Testa a conexão com o banco de dados"""
    connection = get_db_connection()
    if connection and connection.is_connected():
        print("✅ Conexão com MySQL estabelecida com sucesso!")
        db_info = connection.server_info  # Usando a propriedade em vez do método
        print(f"Versão do MySQL Server: {db_info}")
        connection.close()
        return True
    else:
        print("❌ Falha na conexão com MySQL!")
        return False