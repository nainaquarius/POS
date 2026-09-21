from fastapi import APIRouter
from app.vat_records.schema import VatRecordCreate
from app.vat_records.service import createRecord

router = APIRouter(prefix="/vat", tags=["Vat"])

@router.post("/")
async def get_vat_record(data: VatRecordCreate):
  return await createRecord(data)