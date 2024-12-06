from typing import Optional

from pydantic import EmailStr

from myfinances.base_service import BaseService
from myfinances.clients.models import ClientIdResponse, ClientData
from myfinances.models import MyFinancesResponse


class ClientsService(BaseService):
    def list_clients(
        self,
        order_by: Optional[str] = None,
        search: Optional[str] = None
    ) -> MyFinancesResponse[ClientData]:
        """List clients under the specified team."""
        params = {}
        if order_by:
            params["order_by"] = order_by
        if search:
            params["search"] = search

        response = self._client._get("/clients/", params=params)
        return MyFinancesResponse(**response.dict())

    def create_client(
        self,
        name: str,
        phone_number: Optional[str] = None,
        email: Optional[EmailStr] = None,
        company: Optional[str] = None,
        contact_method: Optional[str] = None,
        is_representative: bool = False,
        address: Optional[str] = None,
        city: Optional[str] = None,
        country: Optional[str] = None
    ) -> MyFinancesResponse[ClientIdResponse]:
        """List clients under the specified team."""
        params = {
            "name": name,
            "phone_number": phone_number,
            "email": email,
            "company": company,
            "contact_method": contact_method,
            "is_representative": is_representative,
            "address": address,
            "city": city,
            "country": country,
        }

        response = self._client._post("/clients/create/", params)

        return MyFinancesResponse(**response.dict())
