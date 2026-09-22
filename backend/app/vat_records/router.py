from fastapi import APIRouter
from app.vat_records.schema import VatRecordCreate,VatRecordResponse
from app.vat_records.service import createRecord

router = APIRouter(prefix="/vat", tags=["Vat"])

@router.post("/" , response_model=VatRecordResponse)
async def create_vat_record(data: VatRecordCreate):
  return await createRecord(data)