# criar_tabela_cliques.py
import sqlite3
import os
from app import Config # Assumindo que Config está acessível de app.py

DATABASE = Config.DATABASE

def criar_tabela_contagem_cliques():
    conn = None
    try:
        os.makedirs(os.path.dirname(DATABASE), exist_ok=True) # Garante que a pasta 'instance' exista
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Verifica se a tabela já existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='click_counts';")
        if cursor.fetchone() is None: # Se a tabela não existe
            cursor.execute('''
                CREATE TABLE click_counts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_name TEXT NOT NULL UNIQUE,
                    count INTEGER DEFAULT 0
                )
            ''')
            # Inicializa com o evento específico que queremos rastrear
            cursor.execute("INSERT INTO click_counts (event_name, count) VALUES (?, ?)", ('contact_anunciante_click', 0))
            print("Tabela 'click_counts' criada e inicializada com 'contact_anunciante_click'.")
        else:
            print("Tabela 'click_counts' já existe.")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    criar_tabela_contagem_cliques()