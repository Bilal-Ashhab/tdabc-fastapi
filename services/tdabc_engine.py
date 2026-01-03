from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
from models.event import Event
from models.delay import Delay


@dataclass
class ActivityCost:
    activity: str
    minutes: int
    resource: Optional[str]
    rate: Optional[float]
    cost: Optional[float]


class TDABCEngine:

    ROLE_MAP = {
        "Reception": "NURSE",
        "Exam": "SPECIALIST",
        "Delivery": "TEAM",
        "FollowUp": "MIDWIFE"
    }

    DEFAULT_TIMES = {
        "PRIMI": {"Reception": 40, "Exam": 80, "Delivery": 320, "FollowUp": 28},
        "MULTI": {"Reception": 30, "Exam": 50, "Delivery": 200, "FollowUp": 27},
        "CS": {"Reception": 20, "Exam": 30, "Delivery": 60, "FollowUp": 22},
    }

    def calculate(
        self,
        case_pathway: str,
        db: Session,
        role_rates: Dict[str, float],
        case_id: int
    ) -> Tuple[float, int, List[ActivityCost]]:

        events = (
            db.query(Event)
            .filter(Event.case_id == case_id)
            .order_by(Event.ts)
            .all()
        )

        delays = db.query(Delay).filter(Delay.case_id == case_id).all()

        # -------------------------------
        # Event-based duration calculation
        # -------------------------------
        def minutes_between(start_type, end_type):
            start = next((e.ts for e in events if e.event_type == start_type), None)
            end = next((e.ts for e in events if e.event_type == end_type), None)
            if start and end:
                return int((end - start).total_seconds() / 60)
            return 0

        activity_durations = {
            "Reception": minutes_between("arrival", "triage_end"),
            "Exam": minutes_between("exam_start", "exam_end"),
            "Delivery": minutes_between("exam_end", "delivery"),
            "FollowUp": minutes_between("delivery", "followup"),
        }

        # Fallback to defaults
        if all(v == 0 for v in activity_durations.values()):
            activity_durations = self.DEFAULT_TIMES.get(
                case_pathway, activity_durations
            )

        details: List[ActivityCost] = []
        total_minutes = 0
        total_cost = 0.0

        # -------------------------------
        # Value-added activities
        # -------------------------------
        for activity, mins in activity_durations.items():
            role = self.ROLE_MAP.get(activity)
            rate = role_rates.get(role)
            cost = mins * rate

            details.append(
                ActivityCost(
                    activity=activity,
                    minutes=mins,
                    resource=role,
                    rate=rate,
                    cost=cost
                )
            )

            total_minutes += mins
            total_cost += cost

        # -------------------------------
        # Delays (NON–VALUE ADDED)
        # -------------------------------
        delay_minutes = sum(d.minutes for d in delays)

        if delay_minutes > 0:
            details.append(
                ActivityCost(
                    activity="Delay / Waiting",
                    minutes=delay_minutes,
                    resource=None,
                    rate=None,
                    cost=None
                )
            )

            total_minutes += delay_minutes

        return total_cost, total_minutes, details
