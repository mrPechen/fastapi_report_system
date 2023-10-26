import datetime

from fastapi import Depends
from sqlalchemy import select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from application.database import schemas
from application.database.models import Material, Indicators
from sqlalchemy.orm import Session
from application.database.db_root import connect_db
from sqlalchemy import func, distinct


class ModelsRepository:
    def __init__(self, session: Session = Depends(connect_db)):
        self.material_model = Material
        self.indicator_model = Indicators
        self.db: AsyncSession = session

    """
    Запрос для создания сырья.
    """

    async def create_material(self, material_schemas: schemas.MaterialsParseSchema):
        name = material_schemas.name
        exist = await self.db.execute(select(self.material_model).where(
            self.material_model.name == name))  # exists().where(self.material_model.name == name)
        if exist.scalar():
            result = await self.db.execute(select(self.material_model.id).where(self.material_model.name == name))
            return result.scalar()
        material = self.material_model(**material_schemas.model_dump())
        self.db.add(material)
        await self.db.commit()
        await self.db.refresh(material)
        return material.id

    """
    Запрос для создания составляющих сырья.
    """

    async def create_indicators(self, indicator_schemas: schemas.IndicatorsParseSchema):
        indicator = self.indicator_model(**indicator_schemas.model_dump())
        self.db.add(indicator)
        await self.db.commit()
        await self.db.refresh(indicator)
        return indicator

    """
    Запрос для получения всего сырья с минимальными, максимальными и средними значениями составляющих.
    """

    async def get_values(self, date: str):
        date_data = datetime.datetime.strptime('01-' + date, '%d-%m-%Y').date()
        month = date_data.month
        year = date_data.year
        result = await self.db.execute(
            select(
                self.material_model.id,
                self.material_model.name,
                func.min(distinct(self.indicator_model.iron_content)).label('min_iron_content'),
                func.max(distinct(self.indicator_model.iron_content)).label('max_iron_content'),
                func.avg(distinct(self.indicator_model.iron_content)).label('avg_iron_content'),
                func.min(distinct(self.indicator_model.silicon_content)).label('min_silicon_content'),
                func.max(distinct(self.indicator_model.silicon_content)).label('max_silicon_content'),
                func.avg(distinct(self.indicator_model.silicon_content)).label('avg_silicon_content'),
                func.min(distinct(self.indicator_model.aluminum_content)).label('min_aluminum_content'),
                func.max(distinct(self.indicator_model.aluminum_content)).label('max_aluminum_content'),
                func.avg(distinct(self.indicator_model.aluminum_content)).label('avg_aluminum_content'),
                func.min(distinct(self.indicator_model.calcium_content)).label('min_calcium_content'),
                func.max(distinct(self.indicator_model.calcium_content)).label('max_calcium_content'),
                func.avg(distinct(self.indicator_model.calcium_content)).label('avg_calcium_content'),
                func.min(distinct(self.indicator_model.sulfur_content)).label('min_sulfur_content'),
                func.max(distinct(self.indicator_model.sulfur_content)).label('max_sulfur_content'),
                func.avg(distinct(self.indicator_model.sulfur_content)).label('avg_sulfur_content'),
            )
            .outerjoin(self.indicator_model, self.material_model.id == self.indicator_model.material_id)
            .filter(extract('month', self.indicator_model.upload_date) == month)
            .filter(extract('year', self.indicator_model.upload_date) == year)
            .group_by(self.material_model.id)
        )

        return result.all()
