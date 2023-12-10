from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.schema import GraphQLApiSchema
from dependencies import AppDependencies
from loggers import get_logger

logger = get_logger(__name__)


def create_app() -> FastAPI:
    container = AppDependencies()

    app = FastAPI()
    app.container = container

    logger.info("Setting up middleware")

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    static_files_dir = container.config.api.static_files()
    if static_files_dir is not None:
        static_files_dir = Path(static_files_dir).resolve().absolute()
        logger.info(f"Setting up static files dir {static_files_dir}")
        for elem in static_files_dir.iterdir():
            elem = Path(elem)
            if elem.is_file():
                logger.info(f"Registering get route `/{elem.name}`")
                app.get(f"/{elem.name}", include_in_schema=False)(
                    lambda: FileResponse(str(elem.absolute()))
                )

                if elem.name == "index.html":
                    logger.info("Detected index.html, setting up `/`")
                    app.get(f"/", include_in_schema=False)(
                        lambda: FileResponse(str(elem.absolute()))
                    )

            elif elem.is_dir():
                name = elem.name
                logger.info(f"Mounting `/{name}` static files")
                app.mount(f"/{name}", StaticFiles(directory=str(elem)), name=name)
            else:
                logger.warning(f"Skipped {elem}")
    else:
        logger.debug("No static files dir provided")

    logger.info("Setting up graphql route")

    app.include_router(
        GraphQLRouter(
            schema=GraphQLApiSchema, context_getter=lambda: {"injections": container}
        ),
        prefix="/graphql",
    )
    return app


app = create_app()
