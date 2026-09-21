from app.stock.schema import StockAdjustmentCreate, StockHistoryResponse
from bson import ObjectId
from fastapi import HTTPException, status
from app.database.database import products_collection, stock_history_collection, client
from datetime import datetime, timezone

async def adjust_stock(data: StockAdjustmentCreate, current_user):
  if not ObjectId.is_valid(data.product_id):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid Product ID"
    )
  product_id = ObjectId(data.product_id)

  product = await products_collection.find_one({"_id": product_id})

  if not product:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Product Not Found"
    )

  if not product["is_active"]:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Product is Inactive"
    )

  async with await client.start_session() as session:
    async with session.start_transaction():

      await products_collection.update_one(
        {"_id" : product_id},
        {"$inc" : {"stock": data.quantity}},
        session=session
      )

      new_stock = data.quantity + product["stock"]

      history = {
        "product_id" : data.product_id,
        "quantity" : data.quantity,
        "reason" : data.reason,
        "previous_stock" : product["stock"],
        "new_stock" : new_stock,
        "adjusted_by" : current_user.name,
        "adjusted_at" : datetime.now(timezone.utc)
      }

      history_insert = await stock_history_collection.insert_one(history, session=session)

  return {
    "stock_history_id" : str(history_insert.inserted_id),
    "message" : "Stock adjusted successfully!"
  }

async def get_stock_history():

  results = stock_history_collection.find()

  history_list = []

  async for result in results:
    result_response = StockHistoryResponse(
      id=str(result["_id"]),
      product_id=result["product_id"],
      quantity=result["quantity"],
      reason=result["reason"],
      previous_stock=result["previous_stock"],
      new_stock=result["new_stock"],
      adjusted_by=result["adjusted_by"],
      adjusted_at=result["adjusted_at"]      
    )

    history_list.append(result_response)

  return history_list

async def get_low_stock_products():
  pass