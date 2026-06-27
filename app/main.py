from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.dependencies import NotAuthenticatedException
from app.routes import auth, live


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.seed import seed_admin
    seed_admin()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="strom für alle", lifespan=lifespan)

    app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    app.include_router(auth.router)
    app.include_router(live.router)

    @app.exception_handler(NotAuthenticatedException)
    async def not_authenticated_handler(request: Request, exc: NotAuthenticatedException):
        return RedirectResponse(url="/login", status_code=302)

    @app.get("/")
    def index(request: Request):
        from fastapi.templating import Jinja2Templates
        templates = Jinja2Templates(directory="app/templates")
        return templates.TemplateResponse("index.html", {"request": request})

    return app


app = create_app()
