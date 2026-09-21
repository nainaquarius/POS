from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.products.router import router as product_router
from app.invoices.router import router as invoice_router
from app.stock.router import router as stock_router
from fastapi.middleware.cors import CORSMiddleware
from app.vat_records.router import router as vat_router

app = FastAPI(
  title="POS System API",
  version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(invoice_router)
app.include_router(stock_router)
app.include_router(vat_router)

@app.get("/")
async def root():
  return {
    "message" : "POS System API is running"
  }
