from fastapi import APIRouter, UploadFile, Depends
from fastapi_keycloak import OIDCUser

from application.database.db_root import connect_db
from application.keycloak import idp
from application.parse_xlsx_data.parse_class import XlsxDataSource
from application.services.models_service import ModelsService
from sqlalchemy.orm import Session
from application.parse_xlsx_data.data_to_xlsx import report
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

router = APIRouter(prefix='/api/v1')

"""
Эндпоинт загрузки файла для добавления данных в БД.
"""


@router.post('/upload')
async def upload_file(file: UploadFile, db: Session = Depends(connect_db),
                      user: OIDCUser = Depends(idp.get_current_user())):
    if file.filename.endswith('.xlsx'):
        await XlsxDataSource(file=file.file, session=db).parse()
        return {"success": "file uploaded"}
    return HTTPException(detail='not "xlsx" file', status_code=404)


"""
Эндпоинт для скачивания файла с результатом.
"""


@router.get('/report/{filter_date}')
async def download_report(filter_date: str, service: ModelsService = Depends(),
                          user: OIDCUser = Depends(idp.get_current_user())):
    data = await service.get_values(date=filter_date)
    if data is not None:
        file = report(data=data, date=filter_date)
        return FileResponse(path=file, filename=file, media_type='multipart/form-data')
    return HTTPException(detail='date not found', status_code=404)
