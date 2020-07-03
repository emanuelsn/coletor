import sqlite3
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'banco.db')
print(db_path)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def conectaBanco():
    conn = sqlite3.connect('banco.db')
    print("Conectado")
    cursor = conn.cursor()
    return cursor

def insert_produto(produto):
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        sql = '''INSERT INTO produtos (nomeProduto, valorAVista, valorAPrazo, descricao, linkProduto, codigoBarras)
            VALUES (?,?,?,?,?,?) '''
        cursor.execute(sql,produto)
        conn.commit()
    except Exception as ex:
        print(ex)
    finally:
        return cursor.lastrowid
        conn.close()
    
def pesquisa_produto(nomeProduto):
    print("pesquisando....")
    
    cursor = conectaBanco()
    cursor.execute("select idProduto, nomeProduto from produtos where nomeProduto = ?", (nomeProduto,))
    rows = cursor.fetchall()
    for r in rows:
        print(r)
    
def insert_produto_relacionado(produtoRelacionado):
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    sql =  '''INSERT INTO produtos_relacionados (nomeProduto, nomeProdutoRelacionado) VALUES (?,?) '''
    cursor.execute(sql,produtoRelacionado)
    conn.commit()
    return cursor.lastrowid



#cursor.execute ("CREATE TABLE [if not exists]produtos (idProduto INTEGER PRIMARY KEY AUTOINCREMENT,nomeProduto VARCHAR(255) NOT NULL,	valorAVista decimal(10,2) DEFAULT 0 NOT NULL,valorAPrazo decimal(10,2) DEFAULT 0 NOT NULL,	descricao TEXT)")

