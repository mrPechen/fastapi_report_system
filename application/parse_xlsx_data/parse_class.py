import pandas as pd
from fastapi import Depends
from sqlalchemy.orm import Session

from application.database.schemas import MaterialsParseSchema, IndicatorsParseSchema
from application.repositories.models_repository import ModelsRepository
from application.database.db_root import connect_db

"""
Класс для парсинга загруженного файла и добавления данных в БД.
"""


class XlsxDataSource:
    def __init__(self, file, session: Session = Depends(connect_db)):
        self.session = session
        self.filename = file
        self.materials_file_data: list = []
        self.indicators_file_data: list = []

    async def parse(self):
        df = pd.DataFrame(data=pd.read_excel(self.filename))
        for index, row in df.iterrows():
            material_create = await ModelsRepository(session=self.session).create_material(
                material_schemas=MaterialsParseSchema(name=row[0]))
            material_id = material_create
            await ModelsRepository(session=self.session).create_indicators(
                indicator_schemas=IndicatorsParseSchema(iron_content=row[1],
                                                        silicon_content=row[2],
                                                        aluminum_content=row[3],
                                                        calcium_content=row[4],
                                                        sulfur_content=row[5],
                                                        upload_date=row[6],
                                                        material_id=material_id))
