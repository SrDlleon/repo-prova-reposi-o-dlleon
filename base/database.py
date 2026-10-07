import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("treinos.db")


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    with conectar() as conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL
            )
            """
        )
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS treinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                titulo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                duracao INTEGER NOT NULL,
                concluido INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
            """
        )

def buscar_usuario_por_email(email):
    with conectar() as conexao:
        return conexao.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (email,),
        ).fetchone()


def criar_usuario(nome, email, senha_hash):
    with conectar() as conexao:
        conexao.execute(
            """
            INSERT INTO usuarios (nome, email, senha_hash)
            VALUES (?, ?, ?)
            """,
            (nome, email, senha_hash),
        )


def listar_treinos(usuario_id):
    with conectar() as conexao:
        return conexao.execute(
            """
            SELECT * FROM treinos
            WHERE usuario_id = ?
            ORDER BY id DESC
            """,
            (usuario_id,),
        ).fetchall()


def buscar_treino(treino_id):
    with conectar() as conexao:
        return conexao.execute(
            "SELECT * FROM treinos WHERE id = ?",
            (treino_id,),
        ).fetchone()


def criar_treino(titulo, tipo, duracao, usuario_id=None):
    with conectar() as conexao:
        conexao.execute(
            """
            INSERT INTO treinos (titulo, tipo, duracao, usuario_id)
            VALUES (?, ?, ?, ?)
            """,
            (titulo, tipo, duracao, usuario_id),
        )


def atualizar_treino(treino_id, titulo, tipo, duracao):
    with conectar() as conexao:
        conexao.execute(
            """
            UPDATE treinos
            SET titulo = ?, tipo = ?, duracao = ?
            WHERE id = ?
            """,
            (titulo, tipo, duracao, treino_id),
        )


def alternar_concluido(treino_id):
    with conectar() as conexao:
        conexao.execute(
            """
            UPDATE treinos
            SET concluido = CASE concluido WHEN 1 THEN 0 ELSE 1 END
            WHERE id = ?
            """,
            (treino_id,),
        )


def excluir_treino(treino_id):
    with conectar() as conexao:
        conexao.execute(
            "DELETE FROM treinos WHERE id = ?",
            (treino_id,),
        )
