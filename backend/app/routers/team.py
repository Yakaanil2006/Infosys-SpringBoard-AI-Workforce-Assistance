from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_admin
from app.models.team import TeamMember
from app.models.user import User
from app.schemas.team import TeamCreate

router = APIRouter(tags=["team"])


@router.get("/api/team")
def public_team(db: Session = Depends(get_db)):
    return db.execute(select(TeamMember).order_by(TeamMember.name)).scalars().all()


@router.post("/api/admin/team")
def create_team_member(
    payload: TeamCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    member = TeamMember(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.put("/api/admin/team/{member_id}")
def update_team_member(
    member_id: str,
    payload: TeamCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    member = db.get(TeamMember, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")

    for key, value in payload.model_dump().items():
        setattr(member, key, value)

    db.commit()
    db.refresh(member)
    return member


@router.delete("/api/admin/team/{member_id}")
def delete_team_member(
    member_id: str,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    member = db.get(TeamMember, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")

    db.delete(member)
    db.commit()
    return {"message": "Team member deleted"}
