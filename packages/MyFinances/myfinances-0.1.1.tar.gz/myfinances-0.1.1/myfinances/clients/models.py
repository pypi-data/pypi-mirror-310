from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Client(BaseModel):
    id: int
    active: bool
    name: str
    is_representative: bool
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None
    contact_method: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None


class ClientData(BaseModel):
    clients: List[Client]


class ClientIdResponse(BaseModel):
    client_id: int
