import sqlite3
from pathlib import Path

# Configuração e conexão com SQLITE
ROOT_PATH = Path(__file__).parent
connection = sqlite3.connect(ROOT_PATH / "clientes.sqlite")
cursor = connection.cursor()
cursor.row_factory = sqlite3.Row

dados = [
    ('Matheus', 'matheus@email.com'),
    ('João', 'joao@email.com'),
    ('maria', 'maria@email.com'),
    ('carlos', 'carlos@email.com'),
    ('leticia', 'leticia@email.com'),
]

# Cria a tabela 'clientes' no banco de dados, caso ela ainda não exista.
def create_table_clients(connection, cursor):
    try:
        # Verifica se a tabela já existe no banco de dados
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'")
        
        if cursor.fetchone():
            print("A tabela 'clientes' já existe.")
            return

        cursor.execute('CREATE TABLE clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(50))')
        connection.commit()
        print("Tabela 'clientes' criada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela 'clientes': {e}")
        return
    finally:
        connection.close()
    

# Insere um registro na tabela 'clientes'.
def insert_into_clients(connection, cursor, nome: str, email: str):
    try:
        dados = (nome, email)
        cursor.execute("INSERT INTO clientes (nome, email) VALUES (?,?);", dados)
        connection.commit()
        print(f"Cliente '{nome}' inserido com sucesso.")
    except Exception as e:
        connection.rollback()
        print(f"Ocorreu um erro ao inserir o cliente '{nome}' com o email '{email}': {e}")
    finally:
        connection.close()
    

# Atualiza um registro na tabela 'clientes'.
def update_table_clients(connection, cursor, nome: str, email: str, id: int):
    try:
        data = (nome, email, id)
        cursor.execute("UPDATE clientes SET nome=?, email=? WHERE id=?", data)
        connection.commit()
        print(f"Cliente com ID {id} atualizado com sucesso.")
    except Exception as e:
        connection.rollback()
        print(f"Ocorreu um erro ao atualizar o cliente com ID {id}: {e}")
    

# Remove um registro da tabela 'clientes' com base no ID fornecido.
def delete_user_clients(connection, cursor, id: int):
    try:
        data = (id,)
        cursor.execute("DELETE FROM clientes WHERE id=?", data)
        connection.commit()

        if cursor.rowcount == 0:
            print(f"Nenhum cliente encontrado com o ID {id}.")
            return

        print(f"Cliente com ID {id} deletado com sucesso.")
    except Exception as e:
        connection.rollback()
        print(f"Ocorreu um erro: {e}")
    

# Insere múltiplos registros na tabela 'clientes'.
def insert_many_clients(connection, cursor, dados: tuple):
    try:
        if not dados:
            print("Nenhum dado fornecido para inserção")
            return

        cursor.executemany("INSERT INTO clientes (nome, email) VALUES (?,?);", dados)
        connection.commit()
        
        print(f"{cursor.rowcount} registros inseridos com sucesso.")
    
    except Exception as e:
        print(f"Ocorreu um erro ao inserir dados: {e}")
        return
    

# Busca um registro na tabela 'clientes' pelo ID.
def fetch_one_clients(cursor, id: int):
    try:
        if not isinstance(id, int) or id <= 0:
            print("O ID deve ser um número inteiro positivo.")
            return {}

        cursor.execute("SELECT * FROM clientes WHERE id=?", (id,))
        cliente = cursor.fetchone()

        if cliente is None:
            print(f"Nenhum cliente encontrado com o ID {id}.")
            return {}
        
        print(f"Cliente encontrado: {cliente}")
        return dict(cliente)

    except Exception as e:
        print(f"Ocorreu um erro ao buscar o cliente com ID {id}: {e}")
        return {}
    

# Recupera todos os registros da tabela 'clientes'.
def fetch_all_clients(cursor):
    try:
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

        if not clientes:
            print("Nenhum cliente encontrado na tabela.")
            return []
        
        print(f"{len(clientes)} cliente(s) recuperado(s) com sucesso.")
        return (clientes)

    except Exception as e:
        print(f"Ocorreu um erro ao recuperar todos os clientes: {e}")
        return []
    finally:
        connection.close()
    


create_table_clients(connection, cursor)
insert_many_clients(connection, cursor, dados)
insert_into_clients(connection, cursor, 'Matheeus', 'matheus@email.com')
update_table_clients(connection, cursor, 'Matheus', 'matheus@email.com', 22)
delete_user_clients(connection, cursor, 1)

# Print em um único registro solicitado se houver o id
cliente = fetch_one_clients(cursor, 2)
print(cliente)

# Print de todos os registros
clientes = fetch_all_clients(cursor)
for cliente in clientes:
    print(dict(cliente))
