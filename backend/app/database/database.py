from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = AsyncIOMotorClient(settings.mongodb_url)

db = client[settings.database_name]
users_collection = db['users']
products_collection = db["products"]
invoices_collection = db["invoices"]
stock_history_collection = db["stock_history"]
vat_records_collection = db["vat_records"]