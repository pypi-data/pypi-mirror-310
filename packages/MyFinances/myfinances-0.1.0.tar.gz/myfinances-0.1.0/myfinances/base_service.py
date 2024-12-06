from typing import Optional

class BaseService:
    def __init__(self, client):
        from myfinances import MyFinancesClient
        self._client = client