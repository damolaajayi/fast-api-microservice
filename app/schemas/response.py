from typing import Generic, List, TypeVar, Optional, Union
from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")

class APIResponse(GenericModel, Generic[T]):
    data: Optional[T] = None
    message: str = "success"
    status_code: int = 200
    count: Optional[int] = None
    
    
class ErrorResponse(BaseModel):
    status_code: int
    message: str
    error: Optional[Union[str, List[str], List[dict]]] = None
