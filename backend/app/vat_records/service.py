from app.database.database import invoices_collection
from app.vat_records.schema import VatRecordCreate, VatRecordResponse
from fastapi import HTTPException, status

async def createRecord(data: VatRecordCreate):

  invoice = await invoices_collection.find_one({
    "invoice_number" : data.invoice_number
  })

  if not invoice:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Invoice not found"
    )

  product_names = []

  for item in invoice["items"]:

    product_names.append(item["product_name"])

  product_names = ", ".join(product_names)

  # product_names = ", ".join(
  #   [item["product_name"] for item in invoice["items"] ]
  # )

  invoice_price = invoice["total"]
  vat = invoice_price * 0.05
  total_amount = invoice_price + vat

  return VatRecordResponse(
    invoice_number=invoice["invoice_number"],
    product_names=product_names,
    date=invoice["created_at"],
    invoice_price=invoice_price,
    vat=vat,
    total_amount=total_amount
  )