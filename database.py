
"""
Módulo de gerenciamento do banco de dados
Responsável pela criação e conexão com o banco de dados SQLite
"""

import sqlite3
from typing import Optional

class Database:
    """Classe para gerenciar a conexão e operações do banco de dados"""
    
    def __init__(self, db_name: str = "cadastro.db"):
        """Inicializa a conexão com o banco de dados"""
        self.db_name = db_name
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
    
    def conectar(self):
        """Estabelece conexão com o banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ Conectado ao banco de dados '{self.db_name}'")
        except sqlite3.Error as e:
            print(f"✗ Erro ao conectar ao banco de dados: {e}")
    
    def desconectar(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            print("✓ Conexão com banco de dados fechada")
    
    def criar_tabelas(self):
        """Cria as tabelas 'clientes' e 'pedidos' no banco de dados"""
        try:
            # Criar tabela de clientes
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    telefone TEXT NOT NULL
                )
            """)
            
            # Criar tabela de pedidos (relacionada a clientes)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    produto TEXT NOT NULL,
                    valor REAL NOT NULL,
                    data TEXT NOT NULL,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                        ON DELETE CASCADE
                )
            """)
            
            self.conn.commit()
            print("✓ Tabelas criadas com sucesso")
        except sqlite3.Error as e:
            print(f"✗ Erro ao criar tabelas: {e}")
    
    def executar_query(self, query: str, params: tuple = ()):
        """Executa uma query SQL no banco de dados"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"✗ Erro ao executar query: {e}")
            return None
    
    def buscar_todos(self, query: str, params: tuple = ()):
        """Executa uma query SELECT e retorna todos os resultados"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"✗ Erro ao buscar dados: {e}")
            return []
    
    def buscar_um(self, query: str, params: tuple = ()):
        """Executa uma query SELECT e retorna apenas um resultado"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"✗ Erro ao buscar dado: {e}")
            return None
