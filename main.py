# Importações do FastAPI e Pydantic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Importações dos seus módulos
from database import Database
from clientes import GerenciadorClientes

# --- 1. CONFIGURAÇÃO INICIAL E DEPENDÊNCIAS ---

# Inicializa o banco de dados e o GerenciadorClientes
db = Database("cadastro.db")
db.conectar()
db.criar_tabelas() # Garante que as tabelas estão prontas

gerenciador_clientes = GerenciadorClientes(db)

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Sistema de Cadastro de Clientes e Pedidos API",
    version="1.0.0",
    description="API para gerenciar clientes e pedidos usando SQLite."
)

# --- 2. MODELOS Pydantic (Schema de Dados) ---

# Pydantic define a estrutura dos dados esperados na entrada (POST/PUT)
class ClienteCreate(BaseModel):
    nome: str
    email: str
    telefone: str

# Pydantic define a estrutura de saída (GET)
class Cliente(ClienteCreate):
    id: int

# --- 3. ROTAS (Endpoints da API) ---

# 🌐 Rota de Teste Simples
@app.get("/", tags=["Status"])
def read_root():
    return {"status": "API está online!", "versao": app.version}


# 📦 Rota: Criar Novo Cliente (POST)
@app.post("/clientes/", response_model=Cliente, tags=["Clientes"])
def criar_novo_cliente(cliente: ClienteCreate):
    # Tenta criar o cliente usando a lógica existente no GerenciadorClientes
    sucesso = gerenciador_clientes.criar_cliente(
        cliente.nome, cliente.email, cliente.telefone
    )
    
    if not sucesso:
        # Se falhar (ex: email duplicado), retorna um erro HTTP
        raise HTTPException(
            status_code=400, 
            detail="Erro ao cadastrar cliente. O e-mail pode já estar em uso."
        )
    
    # Busca o cliente recém-criado (o GerenciadorClientes precisaria de um método para isso, 
    # mas para simplificar, vamos assumir que foi criado e retornar o objeto)
    # Nota: Em um projeto real, você buscaria o último ID inserido
    
    # Como não temos o ID exato, vamos simular a resposta para manter o modelo Cliente
    # Em uma aplicação real, o método criar_cliente retornaria o ID.
    
    # Para fins de demonstração, buscamos o cliente pelo email (assumindo que é UNIQUE)
    
    # Mapeamento temporário (necessita de um método de busca por email no GerenciadorClientes real)
    # Como não temos a busca por email, esta parte é um ponto de melhoria.
    # Por agora, vamos retornar uma resposta simples de sucesso
    
    # Vamos adaptar o retorno para ser realista com a nossa classe existente:
    
    # A maneira mais limpa é criar um método no GerenciadorClientes para buscar pelo ID ou retornar o objeto
    # Como não podemos editar o GerenciadorClientes agora, simularemos o sucesso:
    return {
        "id": gerenciador_clientes.db.cursor.lastrowid if gerenciador_clientes.db.cursor else 0, # Tenta pegar o último ID
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone,
    }

# 📋 Rota: Listar Todos os Clientes (GET)
@app.get("/clientes/", response_model=List[Cliente], tags=["Clientes"])
def listar_todos_clientes():
    clientes_tuplas = gerenciador_clientes.listar_clientes()
    
    # O FastAPI precisa que transformemos as tuplas do SQLite em dicionários 
    # que correspondam ao nosso modelo Pydantic (Cliente)
    clientes_dict = []
    for cliente in clientes_tuplas:
        clientes_dict.append({
            "id": cliente[0],
            "nome": cliente[1],
            "email": cliente[2],
            "telefone": cliente[3]
        })
    
    return clientes_dict


# 🔍 Rota: Buscar Cliente por ID (GET)
@app.get("/clientes/{cliente_id}", response_model=Cliente, tags=["Clientes"])
def buscar_cliente(cliente_id: int):
    cliente = gerenciador_clientes.buscar_cliente_por_id(cliente_id)
    
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente ID {cliente_id} não encontrado.")
    
    # Converte a tupla para o dicionário do Pydantic
    return {
        "id": cliente[0],
        "nome": cliente[1],
        "email": cliente[2],
        "telefone": cliente[3]
    }


# ✍️ Rota: Atualizar Cliente (PUT)
@app.put("/clientes/{cliente_id}", response_model=Cliente, tags=["Clientes"])
def atualizar_dados_cliente(cliente_id: int, cliente_data: ClienteCreate):
    # Verifica se o cliente existe primeiro
    cliente_existente = gerenciador_clientes.buscar_cliente_por_id(cliente_id)
    if not cliente_existente:
        raise HTTPException(status_code=404, detail=f"Cliente ID {cliente_id} não encontrado.")

    sucesso = gerenciador_clientes.atualizar_cliente(
        cliente_id, 
        cliente_data.nome, 
        cliente_data.email, 
        cliente_data.telefone
    )
    
    if not sucesso:
        raise HTTPException(status_code=400, detail="Erro ao atualizar cliente.")
        
    # Retorna o objeto atualizado
    return {
        "id": cliente_id,
        "nome": cliente_data.nome,
        "email": cliente_data.email,
        "telefone": cliente_data.telefone
    }

# ❌ Rota: Deletar Cliente (DELETE)
@app.delete("/clientes/{cliente_id}", tags=["Clientes"])
def deletar_cliente_existente(cliente_id: int):
    sucesso = gerenciador_clientes.deletar_cliente(cliente_id)
    
    if not sucesso:
        # Erro 404 se não deletar (provavelmente porque não existe)
        raise HTTPException(status_code=404, detail=f"Cliente ID {cliente_id} não encontrado.")
    
    return {"message": f"Cliente ID {cliente_id} removido com sucesso."}