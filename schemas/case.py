from pydantic import BaseModel


class CaseCreate(BaseModel):
    patient_key: str
    pathway: str
    year: int = 2024
