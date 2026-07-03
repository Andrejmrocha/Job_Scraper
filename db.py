import os
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def conectar():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao MYSQL: {e}")
        return None


def criar_tabela():
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS vagas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255),
            empresa VARCHAR(255),
            data_publicacao DATE,
            link TEXT,
            responsabilidades JSON,
            requisitos JSON,
            UNIQUE KEY chave_unica (titulo, empresa, data_publicacao)
        )
        """
        cursor.execute(query)
        conexao.commit()
        cursor.close()
        conexao.close()


def salvar_no_banco(lista_vagas):
    conexao = conectar()
    if conexao:
        cursor = conexao.cursor()
        query = """
        INSERT IGNORE INTO vagas (titulo, empresa, data_publicacao, link, responsabilidades, requisitos)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = []
        for vaga in lista_vagas:
            valores.append((
                vaga["titulo"],
                vaga["empresa"],
                vaga["data_publicacao"],
                vaga["link"],
                json.dumps(vaga["responsabilidades"], ensure_ascii=False),
                json.dumps(vaga["requisitos"], ensure_ascii=False),
            ))

        cursor.executemany(query, valores)
        conexao.commit()
        print(f"{cursor.rowcount} registros inseridos com sucesso.")
        cursor.close()
        conexao.close()