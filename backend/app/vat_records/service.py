from app.database.database import invoices_collection
from app.vat_records.schema import VatRecordResponse
from app.database.database import vat_records_collection
from datetime import datetime

async def getVatRecords(from_date: str | None = None,to_date: str | None = None):
  query = {}

  if from_date and to_date:
    start_date = datetime.fromisoformat(from_date)
    end_date = datetime.fromisoformat(to_date)

    end_date = end_date.replace(
      hour=23,
      minute=59,
      second=59,
      microsecond=999999
    )

    query["date"] = {
      "$gte" : start_date,
      "$lte" : end_date
    }

    records = await vat_records_collection.find(query).sort(
      "date",
      1
    ).to_list(length=None)

    return [
      VatRecordResponse(
        invoice_number=record["invoice_number"],
        product_names=record["product_names"],
        date=record["date"],
        invoice_price=record["invoice_price"],
        vat=record["vat"],
        total_amount=record["total_amount"]
      )

      for record in records
    ]