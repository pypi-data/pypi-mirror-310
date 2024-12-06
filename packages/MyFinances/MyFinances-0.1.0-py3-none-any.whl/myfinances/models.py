from json import JSONDecodeError
from typing import Optional, Dict, Any, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')


class Meta(BaseModel):
    success: bool
    status_code: int
    content: Optional[str] = None


class MyFinancesResponse(BaseModel, Generic[T]):
    meta: Meta
    data: Optional[T] = None

    @classmethod
    def from_http_response(cls, response) -> 'MyFinancesResponse':
        """Create a MyFinancesResponse from an HTTP response."""
        content = response.content.decode() if response.content else None
        success = str(response.status_code).startswith("2")

        if success:
            try:
                json_data = response.json()
            except JSONDecodeError:
                json_data = {}
        else:
            json_data = {}

        return cls(
            meta=Meta(
                success=success,
                status_code=response.status_code,
                content=content or json_data.get("message", "Unknown error occurred")
            ),
            data=json_data.get("data")
        )


class BaseResponse(BaseModel):
    meta: Meta
    data: dict
