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
        self.pool.close()
        await self.pool.wait_closed()

    async def fetch(self, query: str, args: tuple = ()) -> List[dict]:
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, args)
                result = await cursor.fetchall()
        return result

    async def execute(self, query: str, args: tuple = ()) -> None:
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, args)


# Dependência para obter uma conexão com o banco de dados
def get_db():
    # Esta função é usada no FastAPI para criar a dependência do banco de dados.
    # Quando uma rota usa Depends(get_db), uma conexão com o banco será criada automaticamente.
    return app.state.mysql


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicia o pool de conexões quando a aplicação iniciar
    mysql = MySQL()
    await mysql.init_pool()
    app.state.mysql = mysql  # Atribui a conexão do MySQL no estado do app
    yield
    await mysql.close_pool()  # Fecha a conexão quando a aplicação parar


# Inicializa a aplicação FastAPI com o gerenciador de ciclo de vida
app = FastAPI(lifespan=lifespan)
