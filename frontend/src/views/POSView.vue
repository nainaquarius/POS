<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import router from '@/router'

const products = ref([])
const loading = ref(false)
const error = ref('')
const search = ref('')
const cart = ref([])
const paymentMethod = ref('')
const saleError = ref('')

const completeSale = async () => {
  saleError.value = ''

  if (cart.value.length === 0) {
    return
  }

  if (!paymentMethod.value) {
    saleError.value = 'Please Select Payment Method'
    return
  }

  const items = cart.value.map((item) => {
    return {
      product_id: item.id,
      quantity: item.quantity,
    }
  })

  const invoiceData = {
    items: items,
    payment_method: paymentMethod.value,
  }

  try {
    const response = await api.post('/invoice/', invoiceData)

    const invoiceID = response.data.id

    cart.value = []
    paymentMethod.value = ''

    router.push(`/invoices?print=${invoiceID}`)
  } catch (err) {
    console.error(err)

    saleError.value = err?.response?.data?.detail || 'Failed to complete sale'
  }
}

const addToCart = (product) => {
  const existingItem = cart.value.find((item) => item.id === product.id)

  if (existingItem) {
    existingItem.quantity++
  } else {
    cart.value.push({
      ...product,
      quantity: 1,
    })
  }
}

const increaseQuantity = (item) => {
  item.quantity++
}

const decreaseQuantity = (item) => {
  if (item.quantity > 1) {
    item.quantity--
  }
}

const removeFromCart = (item) => {
  const index = cart.value.findIndex((cartItem) => cartItem.id === item.id)

  if (index !== -1) {
    cart.value.splice(index, 1)
  }
}

const cartTotal = computed(() => {
  let total = 0

  for (const item of cart.value) {
    total += item.price * item.quantity
  }

  return total
})

const fetchProducts = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/products')

    products.value = response.data
  } catch (err) {
    console.error(err)

    error.value = 'Failed to load products'
  } finally {
    loading.value = false
  }
}

const filteredProducts = computed(() => {
  const keyword = search.value.toLowerCase().trim()

  if (!keyword) {
    return products.value
  }

  return products.value.filter((product) => {
    return (
      product.name.toLowerCase().includes(keyword) ||
      product.sku.toLowerCase().includes(keyword) ||
      product.barcode.toLowerCase().includes(keyword)
    )
  })
})

onMounted(() => {
  fetchProducts()
})
</script>

<template>
  <div class="pos-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1>POS</h1>
        <p>Create a new sale.</p>
      </div>
    </div>

    <!-- Search -->
    <div class="search-section">
      <input v-model="search" type="text" placeholder="Search product or scan barcode..." />
    </div>

    <!-- POS Content -->
    <div class="pos-content">
      <!-- Products -->
      <section class="products-section">
        <div class="section-header">
          <div>
            <h2>Products</h2>
            <p>Select a product to add it to the cart.</p>
          </div>
        </div>

        <div class="products-body">
          <p v-if="loading" class="message">Loading products...</p>

          <p v-else-if="error" class="error">
            {{ error }}
          </p>

          <div v-else-if="filteredProducts.length" class="product-grid">
            <div v-for="product in filteredProducts" :key="product.id" class="product-card">
              <div class="product-info">
                <h3>{{ product.name }}</h3>

                <p>SKU: {{ product.sku }}</p>

                <p>Barcode: {{ product.barcode }}</p>

                <strong>
                  {{ Number(product.price).toFixed(2) }}
                </strong>
              </div>

              <button @click="addToCart(product)">Add to Cart</button>
            </div>
          </div>

          <p v-else class="message">No products found.</p>
        </div>
      </section>

      <!-- Cart -->
      <section class="cart-section">
        <div class="cart-header">
          <h2>Cart</h2>
          <span>{{ cart.length }} item(s)</span>
        </div>

        <div v-if="cart.length" class="cart-content">
          <!-- Scrollable Cart Items -->
          <div class="cart-items">
            <div v-for="item in cart" :key="item.id" class="cart-item">
              <div class="cart-item-info">
                <strong>
                  {{ item.name }}
                </strong>

                <p>
                  {{ Number(item.price).toFixed(2) }}
                  ×
                  {{ item.quantity }}
                </p>
              </div>

              <div class="cart-item-actions">
                <div class="quantity-controls">
                  <button type="button" @click="decreaseQuantity(item)">−</button>

                  <span>
                    {{ item.quantity }}
                  </span>

                  <button type="button" @click="increaseQuantity(item)">+</button>
                </div>

                <strong class="item-total">
                  {{ (item.price * item.quantity).toFixed(2) }}
                </strong>

                <button type="button" class="remove-button" @click="removeFromCart(item)">
                  Remove
                </button>
              </div>
            </div>
          </div>

          <!-- Fixed Bottom Area -->
          <div class="cart-footer">
            <!-- Total -->
            <div class="cart-total">
              <span>Total</span>

              <strong>
                {{ cartTotal.toFixed(2) }}
              </strong>
            </div>

            <!-- Payment -->
            <div class="payment-section">
              <label for="payment-method"> Payment Method </label>

              <select id="payment-method" v-model="paymentMethod">
                <option value="">Select payment method</option>

                <option value="cash">Cash</option>

                <option value="card">Card</option>
              </select>
            </div>

            <!-- Error -->
            <p v-if="saleError" class="error">
              {{ saleError }}
            </p>

            <!-- Complete Sale -->
            <button class="complete-sale-button" @click="completeSale">Complete Sale</button>
          </div>
        </div>

        <!-- Empty Cart -->
        <div v-else class="empty-cart">
          <p>No products selected.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
/* ========================================
   POS PAGE
======================================== */

.pos-page {
  width: 100%;
  height: calc(100vh - 70px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ========================================
   PAGE HEADER
======================================== */

.page-header {
  flex-shrink: 0;
  margin-bottom: 18px;
}

.page-header h1 {
  margin: 0 0 5px;
  font-size: 26px;
  font-weight: 700;
  color: #111827;
}

.page-header p {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

/* ========================================
   SEARCH
======================================== */

.search-section {
  flex-shrink: 0;
  background: white;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 18px;
  border: 1px solid #e5e7eb;
}

.search-section input {
  width: 100%;
  padding: 11px 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  outline: none;
  color: #111827;
}

.search-section input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

/* ========================================
   MAIN POS CONTENT
======================================== */

.pos-content {
  flex: 1;
  min-height: 0;

  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;

  overflow: hidden;
}

/* ========================================
   PRODUCTS SECTION
======================================== */

.products-section {
  min-width: 0;
  min-height: 0;

  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;

  padding: 20px;

  display: flex;
  flex-direction: column;

  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);

  overflow: hidden;
}

/* Products Header */

.section-header {
  flex-shrink: 0;
  margin-bottom: 18px;
}

.section-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #111827;
}

.section-header p {
  margin: 5px 0 0;
  color: #6b7280;
  font-size: 13px;
}

/* Products Body */

.products-body {
  flex: 1;
  min-height: 0;
  overflow: hidden;

  display: flex;
  flex-direction: column;
}

/* Product Grid */

.product-grid {
  flex: 1;
  min-height: 0;

  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 15px;

  overflow-y: auto;
  overflow-x: hidden;

  padding-right: 6px;
  align-content: start;
}

/* Product Card */

.product-card {
  border: 1px solid #e5e7eb;
  padding: 15px;
  border-radius: 10px;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  min-height: 170px;

  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease,
    transform 0.2s ease;
}

.product-card:hover {
  border-color: #d1d5db;
  box-shadow: 0 5px 15px rgba(15, 23, 42, 0.06);
  transform: translateY(-1px);
}

.product-info h3 {
  margin: 0 0 10px;
  font-size: 15px;
  font-weight: 700;
  color: #111827;
}

.product-info p {
  margin: 4px 0;
  font-size: 12px;
  color: #6b7280;
}

.product-info strong {
  display: block;
  margin-top: 12px;
  font-size: 18px;
  font-weight: 800;
  color: #111827;
}

.product-card button {
  width: 100%;
  margin-top: 14px;
  padding: 9px;

  border: none;
  border-radius: 7px;

  background: #1f2937;
  color: white;

  font-size: 13px;
  font-weight: 600;

  cursor: pointer;

  transition:
    background 0.2s ease,
    transform 0.2s ease;
}

.product-card button:hover {
  background: #111827;
  transform: translateY(-1px);
}

/* ========================================
   CART SECTION
======================================== */

.cart-section {
  min-width: 0;
  min-height: 0;

  background: #ffffff;

  border: 1px solid #e5e7eb;
  border-radius: 14px;

  padding: 20px;

  display: flex;
  flex-direction: column;

  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);

  overflow: hidden;
}

/* Cart Header */

.cart-header {
  flex-shrink: 0;

  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-bottom: 15px;

  padding-bottom: 15px;

  border-bottom: 1px solid #eef0f3;
}

.cart-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #111827;
}

.cart-header span {
  font-size: 12px;
  color: #6b7280;
}

/* ========================================
   CART CONTENT
======================================== */

.cart-content {
  flex: 1;
  min-height: 0;

  display: flex;
  flex-direction: column;

  overflow: hidden;
}

/* ========================================
   CART ITEMS - ONLY THIS SCROLLS
======================================== */

.cart-items {
  flex: 1;
  min-height: 0;

  overflow-y: auto;
  overflow-x: hidden;

  padding-right: 5px;
}

/* Cart Item */

.cart-item {
  display: flex;
  justify-content: space-between;
  align-items: center;

  gap: 12px;

  padding: 14px 0;

  border-bottom: 1px solid #eef0f3;
}

.cart-item-info {
  min-width: 0;
  flex: 1;
}

.cart-item-info strong {
  display: block;

  font-size: 14px;
  color: #111827;

  margin-bottom: 5px;

  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cart-item-info p {
  margin: 0;

  color: #6b7280;
  font-size: 12px;
}

/* Cart Item Actions */

.cart-item-actions {
  flex-shrink: 0;

  display: flex;
  align-items: center;

  gap: 8px;
}

.item-total {
  min-width: 55px;

  text-align: right;

  font-size: 13px;
  color: #111827;
}

/* ========================================
   QUANTITY CONTROLS
======================================== */

.quantity-controls {
  display: flex;
  align-items: center;

  border: 1px solid #dfe3e8;
  border-radius: 7px;

  overflow: hidden;

  background: #f9fafb;
}

.quantity-controls button {
  width: 28px;
  height: 28px;

  border: none;
  background: transparent;

  cursor: pointer;

  font-size: 16px;
  color: #374151;
}

.quantity-controls button:hover {
  background: #e5e7eb;
}

.quantity-controls span {
  min-width: 28px;

  text-align: center;

  font-size: 13px;
  font-weight: 600;

  color: #111827;
}

/* ========================================
   REMOVE BUTTON
======================================== */

.remove-button {
  border: none;

  background: #fef2f2;
  color: #dc2626;

  padding: 6px 8px;

  border-radius: 6px;

  cursor: pointer;

  font-size: 11px;
  font-weight: 600;
}

.remove-button:hover {
  background: #fee2e2;
}

/* ========================================
   CART FOOTER - FIXED
======================================== */

.cart-footer {
  flex-shrink: 0;

  padding-top: 15px;

  background: white;
}

/* ========================================
   TOTAL
======================================== */

.cart-total {
  display: flex;
  justify-content: space-between;
  align-items: center;

  padding: 14px;

  border-radius: 9px;

  background: #f8fafc;
  border: 1px solid #e5e7eb;
}

.cart-total span {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
}

.cart-total strong {
  font-size: 21px;
  font-weight: 800;
  color: #111827;
}

/* ========================================
   PAYMENT
======================================== */

.payment-section {
  margin-top: 14px;
}

.payment-section label {
  display: block;

  margin-bottom: 7px;

  font-size: 13px;
  font-weight: 600;

  color: #374151;
}

.payment-section select {
  width: 100%;

  padding: 10px 12px;

  border: 1px solid #d1d5db;
  border-radius: 8px;

  background: white;
  color: #111827;

  outline: none;

  cursor: pointer;
}

.payment-section select:focus {
  border-color: #6366f1;

  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.12);
}

/* ========================================
   COMPLETE SALE
======================================== */

.complete-sale-button {
  width: 100%;

  margin-top: 14px;

  padding: 12px 16px;

  border: none;
  border-radius: 8px;

  background: #111827;
  color: white;

  font-size: 14px;
  font-weight: 700;

  cursor: pointer;

  transition:
    background 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.complete-sale-button:hover {
  background: #1f2937;

  transform: translateY(-1px);

  box-shadow: 0 6px 15px rgba(17, 24, 39, 0.18);
}

.complete-sale-button:active {
  transform: translateY(0);
}

/* ========================================
   ERROR / MESSAGES
======================================== */

.error {
  margin: 10px 0 0;

  padding: 9px 11px;

  border-radius: 7px;

  background: #fef2f2;
  color: #dc2626;

  font-size: 12px;
}

.message {
  margin: 0;

  padding: 20px;

  text-align: center;

  color: #6b7280;

  font-size: 13px;
}

/* ========================================
   EMPTY CART
======================================== */

.empty-cart {
  flex: 1;

  display: flex;
  align-items: center;
  justify-content: center;

  color: #6b7280;

  font-size: 14px;
}

/* ========================================
   SCROLLBAR
======================================== */

.product-grid::-webkit-scrollbar,
.cart-items::-webkit-scrollbar {
  width: 6px;
}

.product-grid::-webkit-scrollbar-track,
.cart-items::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.product-grid::-webkit-scrollbar-thumb,
.cart-items::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.product-grid::-webkit-scrollbar-thumb:hover,
.cart-items::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1000px) {
  .pos-content {
    grid-template-columns: 1fr;
    overflow-y: auto;
  }

  .products-section,
  .cart-section {
    min-height: 500px;
  }

  .pos-page {
    height: auto;
    overflow: visible;
  }
}

@media (max-width: 700px) {
  .product-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .cart-item {
    align-items: flex-start;
    flex-direction: column;
  }

  .cart-item-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 500px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>
