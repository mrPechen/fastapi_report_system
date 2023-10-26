from fastapi import Depends

from application.repositories.models_repository import ModelsRepository


class ModelsService:
    def __init__(self, repository: ModelsRepository = Depends()):
        self.repository = repository
    """
    Получение всего сырья с минимальными, максимальными и средними значениями составляющих
    """
    async def get_values(self, date: str):
        return await self.repository.get_values(date=date)
