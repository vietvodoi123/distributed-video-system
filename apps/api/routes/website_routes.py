from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from apps.api.db.deps import get_db
from apps.api.models.website import Website
from apps.api.schemas.website_schema import (
    WebsiteCreate,
    WebsiteResponse
)

router = APIRouter(prefix="/websites", tags=["websites"])


@router.post("/", response_model=WebsiteResponse)
def create_website(
        payload: WebsiteCreate,
        db: Session = Depends(get_db)
):
    website = Website(**payload.model_dump())

    db.add(website)
    db.commit()
    db.refresh(website)

    return website


@router.get("/", response_model=list[WebsiteResponse])
def get_websites(
        db: Session = Depends(get_db)
):
    return db.query(Website).all()


@router.get("/{website_id}", response_model=WebsiteResponse)
def get_website(
        website_id: str,
        db: Session = Depends(get_db)
):
    return db.query(Website).filter(
        Website.id == website_id
    ).first()