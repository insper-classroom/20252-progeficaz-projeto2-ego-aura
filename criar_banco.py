#!/usr/bin/env python3
"""
Script para criar e popular o banco de dados de imóveis
Baseado no arquivo imoveis.sql

Este script:
1. Cria a tabela imoveis com a estrutura correta para SQLite
2. Popula o banco com todos os dados do arquivo imoveis.sql
3. Exibe estatísticas dos dados inseridos
"""

import sqlite3
import os
from pathlib import Path

def criar_banco():
    """Cria o banco de dados e a tabela imoveis"""
    
    # Nome do banco de dados
    db_name = 'imoveis.db'
    
    # Remove o banco existente se existir
    if os.path.exists(db_name):
        print(f"Removendo banco existente: {db_name}")
        os.remove(db_name)
    
    # Conecta ao banco (cria se não existir)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    print("Criando tabela 'imoveis'...")
    
    # Cria a tabela imoveis
    cursor.execute('''
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
    print("✅ Tabela criada com sucesso!")
    
    return conn

def ler_dados_sql():
    """Lê e processa os dados do arquivo imoveis.sql"""
    
    sql_file = Path('imoveis.sql')
    
    if not sql_file.exists():
        print("❌ Arquivo imoveis.sql não encontrado!")
        return []
    
    print("📖 Lendo dados do arquivo imoveis.sql...")
    
    dados = []
    
    with open(sql_file, 'r', encoding='utf-8') as file:
        content = file.read()
        
        # Procura por linhas INSERT
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('INSERT INTO imoveis'):
                # Extrai os valores entre parênteses após VALUES
                try:
                    start = line.find('VALUES (') + 8
                    end = line.rfind(');')
                    values_str = line[start:end]
                    
                    # Parse manual dos valores (considerando aspas simples e vírgulas)
                    values = []
                    current_value = ""
                    in_quotes = False
                    
                    i = 0
                    while i < len(values_str):
                        char = values_str[i]
                        
                        if char == "'" and (i == 0 or values_str[i-1] != '\\'):
                            in_quotes = not in_quotes
                        elif char == ',' and not in_quotes:
                            values.append(current_value.strip().strip("'"))
                            current_value = ""
                            i += 1
                            continue
                        
                        if not (char == "'" and not in_quotes):
                            current_value += char
                        
                        i += 1
                    
                    # Adiciona o último valor
                    if current_value:
                        values.append(current_value.strip().strip("'"))
                    
                    # Converte tipos apropriados
                    if len(values) == 8:  # logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao
                        logradouro = values[0]
                        tipo_logradouro = values[1]
                        bairro = values[2]
                        cidade = values[3]
                        cep = values[4]
                        tipo = values[5]
                        
                        # Converte valor para float
                        try:
                            valor = float(values[6]) if values[6] else None
                        except:
                            valor = None
                            
                        data_aquisicao = values[7]
                        
                        dados.append((logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao))
                
                except Exception as e:
                    print(f"⚠️  Erro ao processar linha: {line[:50]}... - {e}")
                    continue
    
    print(f"✅ {len(dados)} registros encontrados no arquivo SQL")
    return dados

def inserir_dados(conn, dados):
    """Insere os dados na tabela imoveis"""
    
    if not dados:
        print("❌ Nenhum dado para inserir!")
        return
    
    cursor = conn.cursor()
    
    print(f"📝 Inserindo {len(dados)} registros...")
    
    # SQL para inserção
    insert_sql = '''
        INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    # Inserção em lote
    try:
        cursor.executemany(insert_sql, dados)
        conn.commit()
        print(f"✅ {len(dados)} registros inseridos com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao inserir dados: {e}")
        conn.rollback()

def exibir_estatisticas(conn):
    """Exibe estatísticas dos dados inseridos"""
    
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print("📊 ESTATÍSTICAS DO BANCO DE DADOS")
    print("="*50)
    
    # Total de registros
    cursor.execute("SELECT COUNT(*) FROM imoveis")
    total = cursor.fetchone()[0]
    print(f"Total de imóveis: {total}")
    
    # Imóveis por tipo
    print("\n🏠 Imóveis por tipo:")
    cursor.execute("SELECT tipo, COUNT(*) FROM imoveis WHERE tipo IS NOT NULL GROUP BY tipo ORDER BY COUNT(*) DESC")
    for tipo, count in cursor.fetchall():
        print(f"  {tipo}: {count}")
    
    # Imóveis por cidade (top 10)
    print("\n🏙️  Top 10 cidades com mais imóveis:")
    cursor.execute("SELECT cidade, COUNT(*) FROM imoveis GROUP BY cidade ORDER BY COUNT(*) DESC LIMIT 10")
    for cidade, count in cursor.fetchall():
        print(f"  {cidade}: {count}")
    
    # Estatísticas de valor
    print("\n💰 Estatísticas de valor:")
    cursor.execute("SELECT COUNT(*), MIN(valor), MAX(valor), AVG(valor) FROM imoveis WHERE valor IS NOT NULL")
    count, min_val, max_val, avg_val = cursor.fetchone()
    if count > 0:
        print(f"  Imóveis com valor: {count}")
        print(f"  Valor mínimo: R$ {min_val:,.2f}")
        print(f"  Valor máximo: R$ {max_val:,.2f}")
        print(f"  Valor médio: R$ {avg_val:,.2f}")
    
    # Anos de aquisição
    print("\n📅 Imóveis por ano de aquisição:")
    cursor.execute("""
        SELECT substr(data_aquisicao, 1, 4) as ano, COUNT(*) 
        FROM imoveis 
        WHERE data_aquisicao IS NOT NULL 
        GROUP BY substr(data_aquisicao, 1, 4) 
        ORDER BY ano
    """)
    for ano, count in cursor.fetchall():
        print(f"  {ano}: {count}")

def verificar_dados(conn):
    """Exibe alguns exemplos de dados para verificação"""
    
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print("🔍 EXEMPLOS DE DADOS INSERIDOS")
    print("="*50)
    
    cursor.execute("SELECT * FROM imoveis LIMIT 5")
    registros = cursor.fetchall()
    
    for i, registro in enumerate(registros, 1):
        print(f"\n📋 Registro {i}:")
        print(f"  ID: {registro[0]}")
        print(f"  Logradouro: {registro[1]}")
        print(f"  Tipo Logradouro: {registro[2]}")
        print(f"  Bairro: {registro[3]}")
        print(f"  Cidade: {registro[4]}")
        print(f"  CEP: {registro[5]}")
        print(f"  Tipo: {registro[6]}")
        print(f"  Valor: R$ {registro[7]:,.2f}" if registro[7] else "  Valor: Não informado")
        print(f"  Data Aquisição: {registro[8]}")

def main():
    """Função principal"""
    
    print("🏠 CRIADOR DE BANCO DE DADOS DE IMÓVEIS")
    print("="*50)
    
    try:
        # 1. Criar banco e tabela
        conn = criar_banco()
        
        # 2. Ler dados do arquivo SQL
        dados = ler_dados_sql()
        
        # 3. Inserir dados
        if dados:
            inserir_dados(conn, dados)
            
            # 4. Exibir estatísticas
            exibir_estatisticas(conn)
            
            # 5. Verificar alguns dados
            verificar_dados(conn)
            
        else:
            print("❌ Nenhum dado foi encontrado para inserir!")
        
        # Fechar conexão
        conn.close()
        
        print(f"\n✅ Processo concluído! Banco 'imoveis.db' criado com sucesso!")
        print(f"💡 Você pode usar este banco com a API Flask que criamos.")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")

if __name__ == '__main__':
    main()
