from pydantic import BaseModel, Field
from datetime import datetime


class InvoiceItemCreate(BaseModel):
  product_id: str
  quantity: int = Field(gt=0)


class InvoiceCreate(BaseModel):
  items: list[InvoiceItemCreate] = Field(min_length=1)
  payment_method: str


class InvoiceItemResponse(BaseModel):
  product_id: str
  product_name: str
  quantity: int
  price: float
  subtotal: float


class InvoiceResponse(BaseModel):
  id: str
  invoice_number: str
  cashier: str
  items: list[InvoiceItemResponse]
  total: float
  payment_method: str
  created_at: datetime