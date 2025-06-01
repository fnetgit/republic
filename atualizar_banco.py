# adicionar_coluna_db.py
import sqlite3
import os

# Certifique-se de que o caminho para o seu banco de dados está correto
DATABASE = 'instance/banco.db' 

def adicionar_coluna_solicitacao_exclusao():
    conn = None
    try:
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True) # Garante que a pasta 'instance' exista
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Verifica se a coluna já existe para evitar erros ao rodar mais de uma vez
        cursor.execute("PRAGMA table_info(usuarios)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'solicitacao_exclusao' not in columns:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN solicitacao_exclusao INTEGER DEFAULT 0")
            print("Coluna 'solicitacao_exclusao' adicionada à tabela 'usuarios' com sucesso.")
        else:
            print("Coluna 'solicitacao_exclusao' já existe na tabela 'usuarios'.")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    adicionar_coluna_solicitacao_exclusao()