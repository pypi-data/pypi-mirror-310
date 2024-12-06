from myfinances.finance.invoices.service import InvoicesService


class FinanceService:
    def __init__(self, client):
        self.invoices = InvoicesService(client)