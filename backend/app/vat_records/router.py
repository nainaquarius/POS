from fastapi import APIRouter, Depends
from app.vat_records.schema import VatRecordCreate,VatRecordResponse
from app.vat_records.service import createRecord
from app.dependencies import require_roles

router = APIRouter(prefix="/vat", tags=["Vat"])

@router.post("/" , response_model=VatRecordResponse)
async def create_vat_record(data: VatRecordCreate, current_user = Depends(require_roles("admin", "manager", "cashier"))):
  return await createRecord(data)