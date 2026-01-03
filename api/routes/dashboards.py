from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.case import Case
from services.tdabc_engine import TDABCEngine

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

ROLE_RATES = {
    "NURSE": 2.0,
    "SPECIALIST": 6.0,
    "TEAM": 8.0,
    "MIDWIFE": 2.5
}


@router.get("/metrics")
def dashboard_metrics(db: Session = Depends(get_db)):
    cases = db.query(Case).all()

    total_cases = len(cases)
    if total_cases == 0:
        return {
            "total_cases": 0,
            "avg_case_time": 0,
            "cs_rate": 0
        }

    engine = TDABCEngine()
    total_minutes_sum = 0
    cs_count = 0

    for case in cases:
        _, minutes, _ = engine.calculate(
            case_pathway=case.pathway,
            db=db,
            role_rates=ROLE_RATES,
            case_id=case.id
        )
        total_minutes_sum += minutes

        if case.is_cs:
            cs_count += 1

    avg_case_time = round(total_minutes_sum / total_cases)
    cs_rate = round((cs_count / total_cases) * 100, 1)

    return {
        "total_cases": total_cases,
        "avg_case_time": avg_case_time,
        "cs_rate": cs_rate
    }
