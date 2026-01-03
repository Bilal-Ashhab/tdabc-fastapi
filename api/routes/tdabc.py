from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.case import Case
from services.tdabc_engine import TDABCEngine

router = APIRouter()
engine = TDABCEngine()


@router.post("/calculate/{case_id}")
def calculate_tdabc(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id==case_id).first()
    if not case:
        return {"error": "Case not found"}

    # Role rates from database or hardcoded
    role_rates = {
        "NURSE": 2.0,
        "SPECIALIST": 6.0,
        "TEAM": 8.0,
        "MIDWIFE": 2.5
    }

    total_cost, total_minutes, details = engine.calculate(case.pathway, db, role_rates, case_id)

    # Return structured data
    return {
        "case_id": case_id,
        "pathway": case.pathway,
        "total_minutes": total_minutes,
        "total_cost": total_cost,
        "details": [d.__dict__ for d in details]
    }
