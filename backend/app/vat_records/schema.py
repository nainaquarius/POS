from pydantic import BaseModel
from datetime import datetime

class VatRecordResponse(BaseModel):
  invoice_number: str
  product_names: str
  date: datetime
  invoice_price: float
  vat: float
  total_amount: float