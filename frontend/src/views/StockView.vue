<script setup>
import { onMounted, ref } from 'vue'
import api from '../services/api'

const products = ref([])
const history = ref([])

const loading = ref(false)
const error = ref('')

const showForm = ref(false)
const submitting = ref(false)
const formError = ref('')

const form = ref({
  product_id: '',
  quantity: 1,
  reason: '',
})

const getProductName = (productID) => {
  const product = products.value.find((product) => product.id === productID)

  return product?.name || 'Unknown Product'
}

const adjustStock = async () => {
  formError.value = ''
  submitting.value = true

  try {
    await api.post('/stock/adjust', form.value)

    showForm.value = false

    form.value = {
      product_id: '',
      quantity: 1,
      reason: '',
    }

    await fetchProducts()
    await fetchHistory()
  } catch (err) {
    console.error(err)

    formError.value = err?.response?.data?.detail || 'Failed to adjust stock.'
  } finally {
    submitting.value = false
  }
}

const fetchProducts = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/products')
    products.value = response.data
  } catch (err) {
    error.value = 'Failed to load products'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const fetchHistory = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/stock/history')
    history.value = response.data
  } catch (err) {
    error.value = 'Failed to fetch history'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProducts()
  fetchHistory()
})
</script>

<template>
  <div class="stock-page">
    <div class="page-header">
      <div>
        <h1>Stock Management</h1>
        <p>Manage and monitor your inventory stock.</p>
      </div>

      <button @click="showForm = true">Adjust Stock</button>
    </div>

    <p v-if="loading">Loading stock...</p>

    <p v-else-if="error" class="error">
      {{ error }}
    </p>

    <div v-else class="stock-card">
      <table>
        <thead>
          <tr>
            <th>Product</th>
            <th>SKU</th>
            <th>Category</th>
            <th>Current Stock</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.name }}</td>
            <td>{{ product.sku }}</td>
            <td>{{ product.category }}</td>
            <td>{{ product.stock }}</td>
          </tr>
        </tbody>
      </table>

      <p v-if="products.length === 0">No products found.</p>
    </div>
    <div class="history-section">
      <div class="section-header">
        <div>
          <h2>Stock Adjustment History</h2>
          <p>Track previous stock adjustments.</p>
        </div>
      </div>

      <div class="history-card">
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Quantity</th>
              <th>Previous Stock</th>
              <th>New Stock</th>
              <th>Reason</th>
              <th>Date</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="item in history" :key="item.id">
              <td>
                {{ getProductName(item.product_id) }}
              </td>

              <td>
                {{ item.quantity }}
              </td>

              <td>
                {{ item.previous_stock }}
              </td>

              <td>
                {{ item.new_stock }}
              </td>

              <td>
                {{ item.reason }}
              </td>

              <td>
                {{ new Date(item.adjusted_at).toLocaleString() }}
              </td>
            </tr>
          </tbody>
        </table>

        <p v-if="history.length === 0">No stock adjustment history found.</p>
      </div>
    </div>
  </div>
  <div v-if="showForm" class="form-overlay">
    <div class="stock-form">
      <div class="form-header">
        <div>
          <h2>Adjust Stock</h2>
          <p>Add stock to an existing product.</p>
        </div>

        <button type="button" class="close-button" @click="showForm = false">×</button>
      </div>

      <form @submit.prevent="adjustStock">
        <div class="form-group">
          <label for="product">Product</label>

          <select id="product" v-model="form.product_id">
            <option value="">Select a product</option>

            <option v-for="product in products" :key="product.id" :value="product.id">
              {{ product.name }} — Stock: {{ product.stock }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label for="quantity">Quantity</label>

          <input id="quantity" v-model.number="form.quantity" type="number" min="1" />
        </div>

        <div class="form-group">
          <label for="reason">Reason</label>

          <textarea
            id="reason"
            v-model="form.reason"
            rows="3"
            placeholder="Enter reason for stock adjustment"
          ></textarea>
        </div>

        <p v-if="formError" class="error">
          {{ formError }}
        </p>

        <div class="form-actions">
          <button type="button" class="cancel-button" @click="showForm = false">Cancel</button>

          <button type="submit" class="submit-button" :disabled="submitting">
            {{ submitting ? 'Adjusting...' : 'Adjust Stock' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.stock-page {
  width: 100%;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.page-header h1 {
  margin: 0;
  font-size: 26px;
  font-weight: 700;
  color: #111827;
}

.page-header p {
  margin: 6px 0 0;
  color: #6b7280;
  font-size: 14px;
}

.page-header button {
  border: none;
  padding: 11px 18px;
  border-radius: 8px;
  background: #111827;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-header button:hover {
  background: #1f2937;
  transform: translateY(-1px);
  box-shadow: 0 5px 12px rgba(17, 24, 39, 0.15);
}

/* Stock Card */
.stock-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
}

/* Table */
table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8fafc;
}

th {
  padding: 14px 18px;
  text-align: left;
  font-size: 12px;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid #e5e7eb;
}

td {
  padding: 16px 18px;
  font-size: 14px;
  color: #374151;
  border-bottom: 1px solid #f1f5f9;
}

tbody tr {
  transition: background 0.2s ease;
}

tbody tr:hover {
  background: #f8fafc;
}

tbody tr:last-child td {
  border-bottom: none;
}

/* Empty state */
.stock-card > p {
  padding: 25px;
  margin: 0;
  text-align: center;
  color: #6b7280;
  font-size: 14px;
}

/* Error */
.error {
  padding: 12px 14px;
  border-radius: 8px;
  background: #fef2f2;
  color: #dc2626;
  font-size: 14px;
  margin: 15px 0;
}
@media (max-width: 700px) {
  .stock-card {
    overflow-x: auto;
  }

  .stock-card table {
    min-width: 600px;
  }

  .history-card {
    overflow-x: auto;
  }

  .history-card table {
    min-width: 750px;
  }
}

.form-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  z-index: 1000;
}

.stock-form {
  width: 100%;
  max-width: 500px;
  background: white;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.2);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 22px;
}

.form-header h2 {
  margin: 0;
  font-size: 20px;
  color: #111827;
}

.form-header p {
  margin: 5px 0 0;
  color: #6b7280;
  font-size: 13px;
}

.close-button {
  border: none;
  background: transparent;
  color: #6b7280;
  font-size: 25px;
  line-height: 1;
  cursor: pointer;
}

.close-button:hover {
  color: #111827;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  margin-bottom: 7px;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 11px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #111827;
  outline: none;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

.form-group textarea {
  resize: vertical;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 22px;
}

.cancel-button,
.submit-button {
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.cancel-button {
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
}

.cancel-button:hover {
  background: #f9fafb;
}

.submit-button {
  border: none;
  background: #111827;
  color: white;
}

.submit-button:hover {
  background: #1f2937;
}
.history-section {
  margin-top: 30px;
}

.section-header {
  margin-bottom: 15px;
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
  font-size: 14px;
}

/* Fixed history card */
.history-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
  overflow: hidden;
}

/* Table */
.history-card table {
  width: 100%;
  border-collapse: collapse;
}

/* Fixed header */
.history-card thead {
  display: table;
  width: 100%;
  table-layout: fixed;
  background: #f8fafc;
}

/* Scroll only the table rows */
.history-card tbody {
  display: block;
  height: 300px;
  overflow-y: auto;
  overflow-x: hidden;
}

/* Keep columns aligned */
.history-card tbody tr {
  display: table;
  width: 100%;
  table-layout: fixed;
}

.history-card th {
  padding: 14px 18px;
  text-align: left;
  font-size: 12px;
  font-weight: 700;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid #e5e7eb;
}

.history-card td {
  padding: 16px 18px;
  font-size: 14px;
  color: #374151;
  border-bottom: 1px solid #f1f5f9;
}

.history-card tbody tr:hover {
  background: #f8fafc;
}

.history-card tbody tr:last-child td {
  border-bottom: none;
}

/* Empty state */
.history-card > p {
  padding: 25px;
  margin: 0;
  text-align: center;
  color: #6b7280;
}
</style>
