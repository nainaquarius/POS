from fastapi import APIRouter, Depends
from app.stock.service import adjust_stock, get_stock_history
from app.dependencies import require_roles
from app.stock.schema import StockAdjustmentCreate, StockHistoryResponse

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.post("/adjust")
async def stock_adjust(data: StockAdjustmentCreate, current_user = Depends(require_roles("admin", "manager"))):
  return await adjust_stock(data, current_user)

@router.get("/history", response_model=list[StockHistoryResponse])
async def stock_history(current_user = Depends(require_roles("admin", "manager"))):
  return await get_stock_history()