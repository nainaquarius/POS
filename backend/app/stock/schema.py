from pydantic import BaseModel, Field
from datetime import datetime

class StockAdjustmentCreate(BaseModel):
  product_id: str
  quantity: int = Field(gt=0)
  reason: str

class StockHistoryResponse(BaseModel):
  id: str
  product_id : str
  quantity : int
  reason : str
  previous_stock: int
  new_stock: int
  adjusted_by: str
  adjusted_at: datetime