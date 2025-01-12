from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes import router
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title='iashchak')

# Include routes
app.include_router(router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Isekai Scenario Generator API",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {"url": "https://isekai.fly.dev", "description": "Production server"}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)