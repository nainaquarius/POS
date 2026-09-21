from app.products.schema import ProductCreate, ProductResponse, ProductUpdate
from fastapi import HTTPException, status
from app.database.database import products_collection
from datetime import datetime, timezone
from bson import ObjectId


async def create_product(data: ProductCreate):
  sku_exists = await products_collection.find_one({"sku": data.sku})

  if sku_exists:
    raise HTTPException(
      status_code=status.HTTP_409_CONFLICT,
      detail="Product with this SKU already exists"
    )
  
  current_time = datetime.now(timezone.utc)

  new_product = {
    "name" : data.name,
    "sku" : data.sku,
    "barcode" : data.barcode,
    "category" : data.category,
    "price" : data.price,
    "cost_price" : data.cost_price,
    "stock" : data.stock,
    "low_stock_threshold" : data.low_stock_threshold,
    "description" : data.description,
    "is_active" : True,
    "created_at" : current_time,
    "updated_at" : current_time
  }

  insert_product = await products_collection.insert_one(new_product)

  new_product["id"] = str(insert_product.inserted_id)

  return ProductResponse(
    id=new_product["id"],
    name=new_product["name"],
    sku=new_product["sku"],
    barcode=new_product["barcode"],
    category=new_product["category"],
    price=new_product["price"],
    cost_price=new_product["cost_price"],
    stock=new_product["stock"],
    low_stock_threshold=new_product["low_stock_threshold"],
    description=new_product["description"],
    is_active=new_product["is_active"],
    created_at=new_product["created_at"],
    updated_at=new_product["updated_at"],
  )

async def get_products():

  products = products_collection.find({"is_active" : True})

  product_list = []

  async for product in products:

    product_response = ProductResponse(
      id=str(product["_id"]),
      name=product["name"],
      sku=product["sku"],
      barcode=product["barcode"],
      category=product["category"],
      price=product["price"],
      cost_price=product["cost_price"],
      stock=product["stock"],
      low_stock_threshold=product["low_stock_threshold"],
      description=product["description"],
      is_active=product["is_active"],
      created_at=product["created_at"],
      updated_at=product["updated_at"]
    )

    product_list.append(product_response)

  return product_list

async def get_single_product(product_id:str):

  if not ObjectId.is_valid(product_id):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid Product ID"
    )
  
  object_id = ObjectId(product_id)

  product = await products_collection.find_one({"_id": object_id})

  if not product:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Product not found"
    )

  return ProductResponse(
    id=str(product["_id"]),
    name=product["name"],
    sku=product["sku"],
    barcode=product["barcode"],
    category=product["category"],
    price=product["price"],
    cost_price=product["cost_price"],
    stock=product["stock"],
    low_stock_threshold=product["low_stock_threshold"],
    description=product["description"],
    is_active=product["is_active"],
    created_at=product["created_at"],
    updated_at=product["updated_at"]
  )

async def update_product(product_id: str, data: ProductUpdate):
  if not ObjectId.is_valid(product_id):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid product ID"
    )
  
  object_id = ObjectId(product_id)

  product = await products_collection.find_one({"_id" : object_id})

  if not product:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Product do not exist"
    )
  update_data = data.model_dump(exclude_none=True)
  current_time = datetime.now(timezone.utc)
  update_data["updated_at"] = current_time

  await products_collection.update_one({"_id": object_id},{"$set": update_data})

  updated_product = await products_collection.find_one({"_id" : object_id})

  return ProductResponse(
    id=str(updated_product["_id"]),
    name=updated_product["name"],
    sku=updated_product["sku"],
    barcode=updated_product["barcode"],
    category=updated_product["category"],
    price=updated_product["price"],
    cost_price=updated_product["cost_price"],
    stock=updated_product["stock"],
    low_stock_threshold=updated_product["low_stock_threshold"],
    description=updated_product["description"],
    is_active=updated_product["is_active"],
    created_at=updated_product["created_at"],
    updated_at=updated_product["updated_at"]
  )

async def product_delete(product_id : str):

  if not ObjectId.is_valid(product_id):
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Invalid Product ID"
    )

  obj_id = ObjectId(product_id)

  product = await products_collection.find_one({"_id": obj_id})

  if not product:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Product not found"
    )

  current_time = datetime.now(timezone.utc)

  await products_collection.update_one({"_id": obj_id},{"$set": {"is_active": False, "updated_at": current_time}})

  return {
    "message" : "Product deleted successfully"
  }