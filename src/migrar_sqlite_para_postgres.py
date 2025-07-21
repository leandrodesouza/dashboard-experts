import os
import sqlite3
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert

# Caminho absoluto correto para o SQLite
base_dir = os.path.dirname(__file__)
sqlite_path = os.path.join(base_dir, 'database', 'app.db')
sqlite_conn = sqlite3.connect(sqlite_path)
sqlite_cursor = sqlite_conn.cursor()

# Conexão com PostgreSQL (use a variável de ambiente ou o link direto)
POSTGRES_URL = os.environ.get("DATABASE_URL") or "postgresql://dashboard_user:8gy7fG5w4jpYPBlkBZoCWw48BWTHvDcq@dpg-d1ukspjuibrs738jqkvg-a.oregon-postgres.render.com/dashboard_experts"
pg_engine = create_engine(POSTGRES_URL)
pg_conn = pg_engine.connect()
pg_metadata = MetaData()
pg_metadata.reflect(bind=pg_engine)

# Listar todas as tabelas do SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = [linha[0] for linha in sqlite_cursor.fetchall() if linha[0] != 'sqlite_sequence']

for tabela in tabelas:
    print(f"Migrando: {tabela}")
    # Pega todos os dados da tabela atual
    sqlite_cursor.execute(f"SELECT * FROM {tabela}")
    dados = sqlite_cursor.fetchall()

    # Nome das colunas
    colunas = [desc[0] for desc in sqlite_cursor.description]

    # Define tabela destino no PostgreSQL
    destino = Table(tabela, pg_metadata, autoload_with=pg_engine)

    with pg_engine.begin() as conn:
        for linha in dados:
            valores = dict(zip(colunas, linha))

            # Pula o usuário admin com id=1 se estiver na tabela "coordenadores"
            if tabela == "coordenadores" and valores.get("id") == 1:
                continue

            stmt = insert(destino).values(**valores)
            stmt = stmt.on_conflict_do_nothing(index_elements=['id'])  # Ignora duplicatas
            conn.execute(stmt)

print("✅ Migração concluída com sucesso!")
