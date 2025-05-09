import sqlite3

# Caminho do banco de dados
caminho_banco = 'instance/banco.db'


def criar_tabela_imoveis():
    # Conecta ao banco de dados
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    # Criação da tabela imoveis (caso ainda não exista)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imoveis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endereco TEXT,
            bairro TEXT,
            numero TEXT,
            cep TEXT,
            complemento TEXT,
            valor REAL,
            quartos INTEGER,
            banheiros INTEGER,
            inclusos TEXT,
            outros TEXT,
            descricao TEXT,
            imagem TEXT,
            tipo TEXT,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()
    conn.close()


def cadastrar_imovel(endereco, bairro, numero, cep, complemento, valor, quartos, banheiros, inclusos, outros, descricao, imagem, tipo, usuario_id):
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO imoveis (endereco, bairro, numero, cep, complemento, valor, quartos, banheiros, inclusos, outros, descricao, imagem, tipo, usuario_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (endereco, bairro, numero, cep, complemento, valor, quartos, banheiros, ','.join(inclusos), outros, descricao, imagem, tipo, usuario_id))

    conn.commit()
    conn.close()
