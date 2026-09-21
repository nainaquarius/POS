from app.invoices.schema import InvoiceCreate, InvoiceItemResponse, InvoiceResponse
from bson import ObjectId
from fastapi import HTTPException, status
from app.database.database import (
    client,
    products_collection,
    invoices_collection
)
from datetime import datetime, timezone
import uuid


async def create_invoice(data: InvoiceCreate, current_user):
  invoice_items = []
  total = 0

  now = datetime.now(timezone.utc)

  invoice_number = (
    f"INV-{now.strftime('%Y%m%d%H%M%S')}-"
    f"{uuid.uuid4().hex[:4].upper()}"
  )

  async with await client.start_session() as session:

    async with session.start_transaction():

      for item in data.items:

        if not ObjectId.is_valid(item.product_id):
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product ID"
          )

        object_id = ObjectId(item.product_id)

        product = await products_collection.find_one(
          {"_id": object_id},
          session=session
        )

        if not product:
          raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
          )

        if not product["is_active"]:
          raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Product is not active"
          )

        price = product["price"]
        subtotal = item.quantity * price
        total += subtotal

        invoice_items.append(
          InvoiceItemResponse(
            product_id=item.product_id,
            product_name=product["name"],
            quantity=item.quantity,
            price=price,
            subtotal=subtotal
          )
        )

        result = await products_collection.update_one(
          {
            "_id": object_id,
            "stock": {"$gte": item.quantity}
          },
          {
            "$inc": {"stock": -item.quantity}
          },
          session=session
        )

        if result.modified_count == 0:
          raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
          )

      invoice = {
        "invoice_number": invoice_number,
        "cashier": current_user.name,
        "items": [item.model_dump()
                  for item in invoice_items
                  ],
        "total": total,
        "payment_method": data.payment_method,
        "created_at": now
      }

      result = await invoices_collection.insert_one(
        invoice,
        session=session
      )

    return InvoiceResponse(
      id=str(result.inserted_id),
      invoice_number=invoice["invoice_number"],
      cashier=invoice["cashier"],
      items=invoice["items"],
      total=invoice["total"],
      payment_method=invoice["payment_method"],
      created_at=invoice["created_at"]
    )

async def get_all_invoices():
  invoices = invoices_collection.find()
  result = []
  async for invoce in invoices:
    response = InvoiceResponse(
      id=str(invoce["_id"]),
      invoice_number=invoce["invoice_number"],
      cashier=invoce["cashier"],
      items=invoce["items"],
      total=invoce["total"],
      payment_method=invoce["payment_method"],
      created_at=invoce["created_at"]
    )

    result.append(response)
  return result


async def get_single_invoice(invoice_id: str):
  if not ObjectId.is_valid(invoice_id):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid Invoice ID"
    )
  obj_id = ObjectId(invoice_id)

  result_invoice = await invoices_collection.find_one({"_id": obj_id})

  if result_invoice is None:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Invoice not found"
    )

  return InvoiceResponse(
    id=str(obj_id),
    invoice_number=result_invoice["invoice_number"],
    cashier=result_invoice["cashier"],
    items=result_invoice["items"],
    total=result_invoice["total"],
    payment_method=result_invoice["payment_method"],
    created_at=result_invoice["created_at"]
  )