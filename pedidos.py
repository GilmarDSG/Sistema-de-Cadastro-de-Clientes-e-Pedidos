from database import Database
from typing import List, Optional

class GerenciadorPedidos:
    """Classe responsável pelas operações CRUD de pedidos"""
    
    def __init__(self, db: Database):
        """Inicializa o gerenciador de pedidos"""
        self.db = db

    def criar_pedido(self, cliente_id: int, produto: str, valor: float, data: str) -> bool:
        """Cria um novo pedido no banco de dados (CREATE)"""
        # A data deve ser passada no formato YYYY-MM-DD
        query = "INSERT INTO pedidos (cliente_id, produto, valor, data) VALUES (?, ?, ?, ?)"
        resultado = self.db.executar_query(query, (cliente_id, produto, valor, data))
        
        if resultado:
            print(f"✓ Pedido para o cliente ID {cliente_id} cadastrado com sucesso!")
            return True
        return False

    def listar_pedidos(self) -> List[tuple]:
        """Lista todos os pedidos, incluindo o nome do cliente (READ)"""
        query = """
            SELECT 
                p.id, c.nome, p.produto, p.valor, p.data 
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            ORDER BY p.data DESC
        """
        return self.db.buscar_todos(query)
    
    def buscar_pedido_por_id(self, pedido_id: int) -> Optional[tuple]:
        """Busca um pedido específico pelo ID (READ)"""
        query = """
            SELECT 
                p.id, c.nome, p.produto, p.valor, p.data 
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE p.id = ?
        """
        return self.db.buscar_um(query, (pedido_id,))

    def exibir_pedidos(self):
        """Exibe todos os pedidos de forma formatada no terminal"""
        pedidos = self.listar_pedidos()
        
        if not pedidos:
            print("\n⚠ Nenhum pedido cadastrado.")
            return
        
        print("\n" + "="*80)
        print("LISTA DE PEDIDOS".center(80))
        print("="*80)
        print(f"{'ID':<5} {'Cliente':<25} {'Produto':<20} {'Valor':<10} {'Data':<15}")
        print("-"*80)
        
        for pedido in pedidos:
            pedido_id, nome_cliente, produto, valor, data = pedido
            print(f"{pedido_id:<5} {nome_cliente:<25} {produto:<20} R${valor:,.2f} {data:<15}")
        
        print("="*80)
        print(f"Total: {len(pedidos)} pedido(s)\n")

    # Os métodos atualizar e deletar pedidos não foram implementados, mas ficam como um próximo passo!