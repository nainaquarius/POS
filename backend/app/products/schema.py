from pydantic import BaseModel
from datetime import datetime

class ProductCreate(BaseModel):
  name: str
  sku: str
  barcode: str
  category: str
  price: float
  cost_price: float
  stock: int
  low_stock_threshold: int
  description: str

class ProductResponse(BaseModel):
  id: str
  name: str
  sku: str
  barcode: str
  category: str
  price: float
  cost_price: float
  stock: int
  low_stock_threshold: int
  description: str
  is_active: bool
  created_at: datetime
  updated_at: datetime

class ProductUpdate(BaseModel):
  
  name: str | None = None
  sku: str | None = None
  barcode: str | None = None
  category: str | None = None
  price: float | None = None
  cost_price: float | None = None
  stock: int | None = None
  low_stock_threshold: int | None = None
  description: str | None = None