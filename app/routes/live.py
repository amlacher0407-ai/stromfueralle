from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/live")
def live(request: Request):
    return templates.TemplateResponse("live.html", {"request": request})
