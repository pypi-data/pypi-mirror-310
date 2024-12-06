from myfinances.base_service import BaseService
from myfinances.finance.invoices.models import InvoiceList, CreateInvoiceResponse
from myfinances.models import MyFinancesResponse


class InvoicesService(BaseService):
    def create_invoice(self,
                       customer_id: int, amount: float, description: str = None, due_date: str = None) -> MyFinancesResponse[CreateInvoiceResponse]:
        payload = {
            "customer_id": customer_id,
            "amount": amount,
            "description": description,
            "due_date": due_date,
        }

        response = self._client._post("/invoices/create", json=payload)

        return MyFinancesResponse(**response.dict())


    def list_invoices(self) -> MyFinancesResponse[InvoiceList]:
        response = self._client._get(f"/invoices/")
        return MyFinancesResponse(**response.dict())
