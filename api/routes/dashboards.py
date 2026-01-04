from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models.case import Case
from services.tdabc_engine import TDABCEngine

router = APIRouter()
engine = TDABCEngine()

ROLE_RATES = {
    "NURSE": 2.0,
    "MIDWIFE": 2.5,
    "SPECIALIST": 6.0,
    "TEAM": 8.0
}


@router.get("/metrics")
def dashboard_metrics(db: Session = Depends(get_db)):
    cases = db.query(Case).all()
    total_cases = len(cases)

    case_minutes = []

    for case in cases:
        try:
            total_cost, total_minutes, _ = engine.calculate(
                case_pathway=case.pathway,
                db=db,
                role_rates=ROLE_RATES,
                case_id=case.id
            )

            if total_minutes > 0:
                case_minutes.append(total_minutes)

        except Exception as e:
            print(f"TDABC error for case {case.id}: {e}")

    avg_case_time = (
        round(sum(case_minutes) / len(case_minutes))
        if case_minutes else 0
    )

    cs_cases = db.query(Case).filter(Case.pathway == "CS").count()
    cs_rate = round((cs_cases / total_cases) * 100, 1) if total_cases else 0

    return {
        "total_cases": total_cases,
        "avg_case_time": avg_case_time,
        "cs_rate": cs_rate
    }
