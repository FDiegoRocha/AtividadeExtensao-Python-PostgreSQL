import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def criar_banco_de_dados():
    try:
        # Conecta ao PostgreSQL
        con = psycopg2.connect(
            dbname="postgres",  # Conecta ao banco de dados padrão 'postgres'
            user="postgres",
            password="admin",
            host="localhost",
            port="5433"
        )
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Cria o cursor para executar comandos SQL
        cur = con.cursor()

        # Verifica se o banco de dados já existe
        cur.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'controle_visitantes'")
        exists = cur.fetchone()

        if not exists:
            # Cria o banco de dados se ele não existir
            cur.execute('CREATE DATABASE controle_visitantes')
            print("Banco de dados 'controle_visitantes' criado com sucesso!")
        else:
            print("Banco de dados 'controle_visitantes' ja existe.")

        # Fecha a conexão
        cur.close()
        con.close()

    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")


# Chama a função para criar o banco de dados
criar_banco_de_dados()
