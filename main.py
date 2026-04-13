from fastapi import FastAPI
from middleware.auth import GatewayAuthMiddleware
from routes.chat import router

app = FastAPI(title="Chatbot API")
app.add_middleware(GatewayAuthMiddleware)
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok"}