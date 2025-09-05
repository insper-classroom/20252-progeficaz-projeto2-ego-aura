import sqlite3
import os

DATABASE = 'imoveis.db'

def get_db_connection(database_name=None):
    """Cria uma conexão com o banco de dados SQLite"""
    db_name = database_name or DATABASE
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(database_name=None):
    """Inicializa o banco de dados criando a tabela de imóveis"""
    conn = get_db_connection(database_name)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS imoveis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            logradouro TEXT NOT NULL,
            tipo_logradouro TEXT,
            bairro TEXT,
            cidade TEXT NOT NULL,
            cep TEXT,
            tipo TEXT,
            valor REAL,
            data_aquisicao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def clear_db(database_name=None):
    """Limpa todos os dados da tabela (útil para testes)"""
    conn = get_db_connection(database_name)
    conn.execute('DELETE FROM imoveis')
    conn.commit()
    conn.close()
