# Para atualizações futuras do banco de dados

import sqlite3

# Conecta ao banco
conn = sqlite3.connect('instance/banco.db')
cursor = conn.cursor()

# Tenta adicionar a coluna "ativo"
try:
    cursor.execute("ALTER TABLE imoveis ADD COLUMN ativo INTEGER DEFAULT 1;")
    print("Coluna 'ativo' adicionada com sucesso.")
except sqlite3.OperationalError as e:
    print("Erro:", e)

# Salva e fecha
conn.commit()
conn.close()
