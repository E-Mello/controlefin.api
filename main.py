# Path: main.py

from fastapi import FastAPI
from app.routes import contas
import uvicorn

# Inicializando a aplicação FastAPI com o ciclo de vida para o MySQL
app = FastAPI()


@app.get("/")
def read_root():
    return {"API is running"}


app.include_router(contas.router, prefix="/contas", tags=["Contas"])

if __name__ == "__main__":
    uvicorn.run(app, port=8000, reload=True)
