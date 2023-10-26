from datetime import date

from pydantic import BaseModel, ConfigDict


class MaterialsParseSchema(BaseModel):
    name: str


class IndicatorsParseSchema(BaseModel):
    iron_content: float
    silicon_content: float
    aluminum_content: float
    calcium_content: float
    sulfur_content: float
    upload_date: date
    material_id: int
