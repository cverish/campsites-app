from fastapi import FastAPI

from campsites_api.routers import campsites


def create_app() -> FastAPI:
    app = FastAPI(
        title="campsites",
        description="API for campsites in the US and Canada",
        version="1.0",
    )

    @app.get("/health")
    async def health() -> str:
        return "ok"

    app.include_router(campsites.router)

    return app
