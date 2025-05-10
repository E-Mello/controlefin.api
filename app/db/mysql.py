# Path: app/db/mysql.py

from contextlib import asynccontextmanager
import aiomysql
from fastapi import FastAPI
from typing import List
from app.config.env import EnvConfig


class MySQL:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        """Inicializa o pool de conexões MySQL"""
        self.pool = await aiomysql.create_pool(
            host=EnvConfig.DB_HOST,
            port=EnvConfig.DB_PORT,
            user=EnvConfig.DB_USER,
            password=EnvConfig.DB_PASSWORD,
            db=EnvConfig.DB_NAME,
            minsize=5,
            maxsize=10,
            autocommit=True,
        )

    async def close_pool(self):
        """Fecha o pool de conexões"""
        self.pool.close()
        await self.pool.wait_closed()

    async def fetch(self, query: str, args: tuple = ()) -> List[dict]:
        """Executa uma consulta SELECT e retorna os resultados"""
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, args)
                result = await cursor.fetchall()
        return result

    async def execute(self, query: str, args: tuple = ()) -> None:
        """Executa uma consulta (INSERT, UPDATE, DELETE)"""
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)


# Dependência para obter uma conexão com o banco de dados
def get_db():
    return app.state.mysql


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação (inicia o pool e fecha ao finalizar)"""
    mysql = MySQL()
    await mysql.init_pool()
    app.state.mysql = mysql  # Atribui o pool no estado do app
    yield
    await mysql.close_pool()  # Fecha o pool de conexões quando a aplicação parar


# Inicializa a aplicação FastAPI com o gerenciador de ciclo de vida
app = FastAPI(lifespan=lifespan)
