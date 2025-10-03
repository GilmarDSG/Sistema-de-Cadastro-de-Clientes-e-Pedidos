from database import Database
from typing import List, Optional

class GerenciadorClientes:
    """Classe responsável pelas operações CRUD de clientes"""
    
    def __init__(self, db: Database):
        """Inicializa o gerenciador de clientes"""
        self.db = db

    def criar_cliente(self, nome: str, email: str, telefone: str) -> bool:
        """Cria um novo cliente no banco de dados (CREATE)"""
        query = "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)"
        resultado = self.db.executar_query(query, (nome, email, telefone))
        
        if resultado:
            print(f"✓ Cliente '{nome}' cadastrado com sucesso!")
            return True
        return False

    def listar_clientes(self) -> List[tuple]:
        """Lista todos os clientes cadastrados (READ)"""
        query = "SELECT * FROM clientes ORDER BY id"
        return self.db.buscar_todos(query)
    
    def buscar_cliente_por_id(self, cliente_id: int) -> Optional[tuple]:
        """Busca um cliente específico pelo ID (READ)"""
        query = "SELECT * FROM clientes WHERE id = ?"
        return self.db.buscar_um(query, (cliente_id,))

    def atualizar_cliente(self, cliente_id: int, nome: str, email: str, telefone: str) -> bool:
        """Atualiza os dados de um cliente existente (UPDATE)"""
        query = """
            UPDATE clientes 
            SET nome = ?, email = ?, telefone = ? 
            WHERE id = ?
        """
        resultado = self.db.executar_query(query, (nome, email, telefone, cliente_id))
        
        if resultado:
            print(f"✓ Cliente ID {cliente_id} atualizado com sucesso!")
            return True
        return False

    def deletar_cliente(self, cliente_id: int) -> bool:
        """Remove um cliente do banco de dados (DELETE)"""
        query = "DELETE FROM clientes WHERE id = ?"
        resultado = self.db.executar_query(query, (cliente_id,))
        
        if resultado:
            print(f"✓ Cliente ID {cliente_id} removido com sucesso!")
            return True
        return False

    def exibir_clientes(self):
        """Exibe todos os clientes de forma formatada no terminal"""
        clientes = self.listar_clientes()
        
        if not clientes:
            print("\n⚠ Nenhum cliente cadastrado.")
            return
        
        print("\n" + "="*80)
        print("LISTA DE CLIENTES".center(80))
        print("="*80)
        print(f"{'ID':<5} {'Nome':<25} {'Email':<30} {'Telefone':<15}")
        print("-"*80)
        
        for cliente in clientes:
            cliente_id, nome, email, telefone = cliente
            print(f"{cliente_id:<5} {nome:<25} {email:<30} {telefone:<15}")
        
        print("="*80)
        print(f"Total: {len(clientes)} cliente(s)\n")                        