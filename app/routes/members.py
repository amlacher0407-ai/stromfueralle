from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_login
from app.models.member import Member

router = APIRouter(prefix="/members")
templates = Jinja2Templates(directory="app/templates")


def _next_member_number(db: Session) -> int:
    max_num = db.query(func.max(Member.member_number)).scalar()
    return max_num + 1 if max_num is not None else 1000


@router.get("")
def list_members(
    request: Request,
    user: str = Depends(require_login),
    db: Session = Depends(get_db),
):
    members = db.query(Member).order_by(Member.member_number).all()
    return templates.TemplateResponse(
        "members/list.html", {"request": request, "members": members}
    )


@router.get("/new")
def new_member_form(
    request: Request,
    user: str = Depends(require_login),
):
    return templates.TemplateResponse(
        "members/form.html", {"request": request, "member": None}
    )


@router.post("/new")
def create_member(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    address: str = Form(...),
    email: str = Form(...),
    iban: Optional[str] = Form(None),
    user: str = Depends(require_login),
    db: Session = Depends(get_db),
):
    member = Member(
        member_number=_next_member_number(db),
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        address=address.strip(),
        email=email.strip(),
        iban=iban.strip() if iban and iban.strip() else None,
    )
    db.add(member)
    db.commit()
    return RedirectResponse(url="/members", status_code=302)


@router.get("/{member_id}/edit")
def edit_member_form(
    member_id: int,
    request: Request,
    user: str = Depends(require_login),
    db: Session = Depends(get_db),
):
    member = db.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        "members/form.html", {"request": request, "member": member}
    )


@router.post("/{member_id}/edit")
def update_member(
    member_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    address: str = Form(...),
    email: str = Form(...),
    iban: Optional[str] = Form(None),
    user: str = Depends(require_login),
    db: Session = Depends(get_db),
):
    member = db.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404)
    member.first_name = first_name.strip()
    member.last_name = last_name.strip()
    member.address = address.strip()
    member.email = email.strip()
    member.iban = iban.strip() if iban and iban.strip() else None
    db.commit()
    return RedirectResponse(url="/members", status_code=302)


@router.get("/{member_id}/delete")
def confirm_delete(
    member_id: int,
    request: Request,
    user: str = Depends(require_login),
    db: Session = Depends(get_db),
):
    member = db.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        "members/confirm_delete.html", {"request": request, "member": member}
    )


@router.post("/{member_id}/delete")
def delete_member(
    member_id: int,
    user: str = Depends(require_login),
    db: Session = Depends(get_db),
):
    member = db.get(Member, member_id)
    if not member:
        raise HTTPException(status_code=404)
    db.delete(member)
    db.commit()
    return RedirectResponse(url="/members", status_code=302)
