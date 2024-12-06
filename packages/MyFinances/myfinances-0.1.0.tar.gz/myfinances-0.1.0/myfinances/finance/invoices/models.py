from pydantic import BaseModel, condecimal
from typing import Optional, List


class Invoice(BaseModel):
    id: int
    customer_id: int
    amount: condecimal(gt=0)
    status: str
    due_date: Optional[str] = None
    description: Optional[str] = None

class CreateInvoiceResponse(BaseModel):
    customer_id: int
    amount: condecimal(gt=0)
    description: Optional[str] = None
    due_date: Optional[str] = None

class InvoiceList(BaseModel):
    invoices: List[Invoice]