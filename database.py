# database.py

import sqlite3
import os
from flask import g, current_app


def get_db():
    """
    Obtém uma conexão com o banco de dados SQLite.
    A conexão é armazenada no objeto 'g' do Flask para ser reutilizada
    durante a mesma requisição. Se a conexão não existe, ela é criada.
    """
    if 'db' not in g:
        # Garante que o diretório do banco de dados exista
        os.makedirs(os.path.dirname(
            current_app.config['DATABASE']), exist_ok=True)
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return g.db


def close_db(e=None):
    """
    Fecha a conexão com o banco de dados no final da requisição.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def inicializar_banco():
    """
    Inicializa o esquema do banco de dados criando as tabelas 'usuarios' e 'imoveis'
    se elas ainda não existirem.
    """
    db = get_db()
    cursor = db.cursor()

    # Criação da tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            telefone TEXT,
            tipo_usuario TEXT
        )
    ''')

    # Criação da tabela de imóveis
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imoveis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endereco TEXT, bairro TEXT, numero TEXT, cep TEXT,
            complemento TEXT, valor REAL, quartos INTEGER,
            banheiros INTEGER, inclusos TEXT, outros TEXT,
            descricao TEXT, imagem TEXT, tipo TEXT,
            usuario_id INTEGER, ativo INTEGER DEFAULT 1,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    db.commit()
    close_db()  # Fecha a conexão após a inicialização
