import sqlite3

conexao = sqlite3.connect("curriculos.db")

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS curriculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT,
    email TEXT NOT NULL,
    site TEXT,
    experiencia TEXT NOT NULL
)
""")

conexao.commit()
conexao.close()