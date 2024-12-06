from typing import Optional

import requests

from myfinances.clients.service import ClientsService
from myfinances.finance import FinanceService
from myfinances.models import MyFinancesResponse

DEFAULT_BASE_URL = "https://app.myfinances.cloud/api/public"

class MyFinancesClient:
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.base_url = base_url or DEFAULT_BASE_URL
        self.api_key = api_key if not api_key.startswith("Bearer ") else api_key[7:]
        self.session = requests.Session()

        self.finance = FinanceService(self)
        self.clients = ClientsService(self)

    def _get(self, endpoint: str, params=None):
        params = params or {}
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = self.session.get(url, params=params, headers=headers)
        return MyFinancesResponse.from_http_response(response)

    def _post(self, endpoint: str, json: dict):
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = self.session.post(url, json=json, headers=headers)
        return MyFinancesResponse.from_http_response(response)

    def close(self):
        self.session.close()