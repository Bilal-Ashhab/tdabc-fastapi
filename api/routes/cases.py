from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db, engine, Base
from models.case import Case
from models.event import Event
from models.delay import Delay
from schemas.case import CaseCreate
from schemas.event import EventCreate
from schemas.delay import DelayCreate

Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("")
def create_case(payload: CaseCreate, db: Session = Depends(get_db)):
    case = Case(
        patient_key=payload.patient_key,
        pathway=payload.pathway,
        year=payload.year,
        is_cs=payload.pathway == "CS",
        is_primipara=payload.pathway == "PRIMI"
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return {"id": case.id, "pathway": case.pathway}


@router.get("")
def list_cases(db: Session = Depends(get_db)):
    cases = db.query(Case).all()
    return {
        "total": len(cases),
        "cases": [{"id": c.id, "pathway": c.pathway} for c in cases]
    }


@router.post("/{case_id}/events")
def add_event(case_id: int, payload: EventCreate, db: Session = Depends(get_db)):
    event = Event(
        case_id=case_id,
        event_type=payload.event_type,
        actor_role=payload.actor_role
    )
    db.add(event)
    db.commit()
    return {"status": "event added"}


@router.post("/{case_id}/delays")
def add_delay(case_id: int, payload: DelayCreate, db: Session = Depends(get_db)):
    delay = Delay(
        case_id=case_id,
        code=payload.code,
        minutes=payload.minutes,
        note=payload.note
    )
    db.add(delay)
    db.commit()
    return {"status": "delay added"}
