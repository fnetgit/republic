import sqlite3
import os

DATABASE = 'instance/banco.db'

def inserir_admin():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (nome, email, senha, telefone, tipo_usuario)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Admin Master', 'admin@site.com', 'admin123', '(00) 00000-0000', 'admin'))
    db.commit()
    db.close()

if __name__ == '__main__':
    inserir_admin()
    print("Usuário admin criado ou já existia.")

