from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from campsites_api.routers import campsites

tags_metadata = [
    {
        "name": "health",
        "description": "Health check"
    },
    {
        "name": "GET",
        "description": "Open to all users.",
    },
    {
        "name": "POST",
        "description": "Restricted.",
    },
    {
        "name": "PATCH",
        "description": "Restricted.",
    },
    {
        "name": "DELETE",
        "description": "Restricted.",
    },
]


def create_app() -> FastAPI:
    app = FastAPI(
        title="campsites",
        description="API for campsites in the US and Canada",
        version="1.0",
        openapi_tags=tags_metadata
    )

    origins = [
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["health"])
    async def health() -> str:
        return "ok"

    app.include_router(campsites.router)

    return app
