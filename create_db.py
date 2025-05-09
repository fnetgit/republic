import sqlite3
import os

# Caminho do banco de dados
caminho_banco = 'instance/banco.db'


def criar_tabela_usuarios():
    # Garante que o diretório 'instance' exista
    os.makedirs('instance', exist_ok=True)

    # Conecta ao banco de dados
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    # Criação da tabela usuarios (caso ainda não exista)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            celular TEXT NOT NULL,
            tipo_usuario TEXT
        )
    ''')

    conn.commit()
    conn.close()


def cadastrar_usuario(nome, email, senha, celular, tipo_usuario):
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, celular, tipo_usuario)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, senha, celular, tipo_usuario))

        conn.commit()
        conn.close()
        return 'Cadastro realizado com sucesso!'
    except sqlite3.IntegrityError:
        conn.close()
        return 'Email já cadastrado.'


# Exemplo de uso (executado só se rodar diretamente este arquivo)
if __name__ == '__main__':
    criar_tabela_usuarios()
    resultado = cadastrar_usuario(
        'Admin', 'admin@example.com', '1234', '88999999999', 'anunciante'
    )
    print(resultado)
