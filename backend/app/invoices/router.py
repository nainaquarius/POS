from fastapi import APIRouter, Depends
from app.invoices.service import create_invoice, get_single_invoice, get_all_invoices
from app.dependencies import require_roles
from app.invoices.schema import InvoiceCreate, InvoiceResponse

router = APIRouter(prefix="/invoice", tags=["Invoice"])

@router.post("/", response_model=InvoiceResponse)
async def invoice_create(data: InvoiceCreate, current_user = Depends(require_roles("admin", "manager", "cashier"))):
  return await create_invoice(data, current_user)

@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: str, current_user = Depends(require_roles("admin", "manager", "cashier"))):
  return await get_single_invoice(invoice_id)

@router.get("/", response_model=list[InvoiceResponse])
async def get_invoices_all(current_user = Depends(require_roles("admin", "manager", "cashier"))):
  return await get_all_invoices()