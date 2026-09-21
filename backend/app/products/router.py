from fastapi import APIRouter, Depends
from app.dependencies import require_roles
from app.products.service import create_product, get_products, get_single_product, update_product, product_delete
from app.products.schema import ProductResponse, ProductCreate, ProductUpdate


router = APIRouter(prefix="/products" , tags=["Products"])

@router.post("", response_model=ProductResponse)
async def product_create(data: ProductCreate, current_user = Depends(require_roles("admin", "manager"))):
  return await create_product(data)

@router.get("", response_model=list[ProductResponse])
async def product_get(_current_user = Depends(require_roles("admin", "manager", "cashier"))):
  return await get_products()

@router.get("/{product_id}", response_model=ProductResponse)
async def single_product(product_id: str, _current_user = Depends(require_roles("admin", "manager", "cashier"))):
  return await get_single_product(product_id)

@router.put("/{product_id}", response_model=ProductResponse)
async def product_update(data: ProductUpdate,product_id: str, _current_user = Depends(require_roles("admin", "manager"))):
  return await update_product(product_id, data)

@router.delete("/{product_id}")
async def delete_product(product_id: str, _current_user = Depends(require_roles("admin"))):
  return await product_delete(product_id)