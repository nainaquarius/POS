from pydantic import BaseModel

class VatRecordCreate(BaseModel):
  invoice_number: str