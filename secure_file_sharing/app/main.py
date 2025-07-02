from fastapi import FastAPI
from .routers import ops, client

app = FastAPI(title="Secure File Sharing System")
app.include_router(ops.router)
app.include_router(client.router)