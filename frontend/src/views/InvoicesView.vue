<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

const route = useRoute()

const invoices = ref([])
const loading = ref(false)
const error = ref('')
const selectedInvoice = ref(null)
const search = ref('')

const filteredInvoices = computed(() => {
  const keyword = search.value.toLowerCase().trim()

  if (!keyword) {
    return invoices.value
  }

  return invoices.value.filter((invoice) => {
    return (
      invoice.invoice_number.toLowerCase().includes(keyword) ||
      invoice.cashier.toLowerCase().includes(keyword) ||
      invoice.payment_method.toLowerCase().includes(keyword)
    )
  })
})

const fetchInvoiceDetails = async (invoiceID) => {
  error.value = ''

  try {
    const response = await api.get(`/invoice/${invoiceID}`)
    selectedInvoice.value = response.data
  } catch (err) {
    console.error(err)

    error.value = err?.response?.data?.detail || 'Failed to load invoice details'
  }
}

const closeInvoiceDetails = () => {
  selectedInvoice.value = null
}

const printInvoice = () => {
  document.body.classList.add('printing-invoice')

  window.onafterprint = () => {
    document.body.classList.remove('printing-invoice')
  }

  window.print()
}

const printInvoiceFromSale = async () => {
  const invoiceID = route.query.print

  if (!invoiceID) {
    return
  }

  await fetchInvoiceDetails(invoiceID)

  if (selectedInvoice.value) {
    setTimeout(() => {
      printInvoice()
    }, 300)
  }
}

const fetchInvoices = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get('/invoice/')
    invoices.value = response.data
  } catch (err) {
    console.error(err)

    error.value = err?.response?.data?.detail || 'Failed to load Invoices'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchInvoices()
  printInvoiceFromSale()
})
</script>

<template>
  <div class="invoices-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1>Invoices</h1>
        <p>View completed sales.</p>
      </div>
    </div>

    <div class="search-section">
      <input
        v-model="search"
        type="text"
        placeholder="Search invoice, cashier, or payment method..."
      />
    </div>

    <p v-if="loading" class="message">Loading invoices...</p>

    <p v-else-if="error" class="error">
      {{ error }}
    </p>

    <div v-else class="invoice-card">
      <table>
        <thead>
          <tr>
            <th>Invoice</th>
            <th>Cashier</th>
            <th>Total</th>
            <th>Payment</th>
            <th>Date</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="invoice in filteredInvoices" :key="invoice.id">
            <td>
              <button type="button" class="invoice-link" @click="fetchInvoiceDetails(invoice.id)">
                {{ invoice.invoice_number }}
              </button>
            </td>

            <td>{{ invoice.cashier }}</td>

            <td>
              {{ Number(invoice.total).toFixed(2) }}
            </td>

            <td>
              {{ invoice.payment_method }}
            </td>

            <td>
              {{ new Date(invoice.created_at).toLocaleString() }}
            </td>
          </tr>

          <tr v-if="filteredInvoices.length === 0">
            <td colspan="5" class="no-results">No invoices found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="selectedInvoice" class="modal-overlay" @click.self="closeInvoiceDetails">
      <div class="invoice-details">
        <!-- Details Header -->
        <div class="details-header">
          <div>
            <h2>Invoice Details</h2>
            <p>{{ selectedInvoice.invoice_number }}</p>
          </div>

          <button type="button" class="close-button" @click="closeInvoiceDetails">×</button>
        </div>

        <div class="invoice-info">
          <div>
            <span>Invoice</span>
            <strong>
              {{ selectedInvoice.invoice_number }}
            </strong>
          </div>

          <div>
            <span>Cashier</span>
            <strong>
              {{ selectedInvoice.cashier }}
            </strong>
          </div>

          <div>
            <span>Payment</span>
            <strong>
              {{ selectedInvoice.payment_method }}
            </strong>
          </div>

          <div>
            <span>Date</span>
            <strong>
              {{ new Date(selectedInvoice.created_at).toLocaleString() }}
            </strong>
          </div>
        </div>

        <div class="items-section">
          <h3>Items</h3>

          <table class="items-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Subtotal</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="item in selectedInvoice.items" :key="item.product_id">
                <td>{{ item.product_name }}</td>

                <td>{{ item.quantity }}</td>

                <td>
                  {{ Number(item.price).toFixed(2) }}
                </td>

                <td>
                  {{ Number(item.subtotal).toFixed(2) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="details-total">
          <span>Total</span>

          <strong>
            {{ Number(selectedInvoice.total).toFixed(2) }}
          </strong>
        </div>

        <button type="button" class="print-button" @click="printInvoice">Print Invoice</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.invoices-page {
  width: 100%;
  height: calc(100vh - 70px);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

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

.invoice-card {
  flex: 1;
  min-height: 0;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
  overflow: hidden;
}

.invoice-card table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.invoice-card thead {
  display: table;
  width: 100%;
  table-layout: fixed;
  background: #f8fafc;
}

.invoice-card th {
  padding: 14px 18px;
  text-align: left;
  font-size: 12px;
  font-weight: 700;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.invoice-card tbody {
  display: block;
  height: calc(100vh - 260px);
  overflow-y: auto;
  overflow-x: hidden;
}

.invoice-card tbody tr {
  display: table;
  width: 100%;
  table-layout: fixed;
}

.invoice-card td {
  padding: 14px 18px;
  font-size: 13px;
  color: #374151;
  border-bottom: 1px solid #eef0f3;
}

.invoice-card tbody tr:hover {
  background: #f9fafb;
}

.invoice-link {
  padding: 0;
  border: none;
  background: transparent;
  color: #111827;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.invoice-link:hover {
  text-decoration: underline;
}

.message {
  margin: 0;
  padding: 20px;
  text-align: center;
  color: #6b7280;
  font-size: 13px;
}

.error {
  margin: 0;
  padding: 12px 14px;
  border-radius: 8px;
  background: #fef2f2;
  color: #dc2626;
  font-size: 13px;
}

.no-results {
  text-align: center;
  color: #6b7280;
  padding: 30px !important;
}

/* Modal */

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30px;
  z-index: 1000;
}

.invoice-details {
  width: min(850px, 100%);
  max-height: 90vh;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 50px rgba(15, 23, 42, 0.2);
  padding: 25px;
  overflow-y: auto;
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 18px;
  border-bottom: 1px solid #e5e7eb;
}

.details-header h2 {
  margin: 0 0 5px;
  font-size: 21px;
  color: #111827;
}

.details-header p {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
}

.close-button {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 7px;
  background: #f3f4f6;
  color: #374151;
  font-size: 22px;
  line-height: 1;
  cursor: pointer;
}

.close-button:hover {
  background: #e5e7eb;
}

.invoice-info {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  padding: 20px 0;
}

.invoice-info div {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.invoice-info span {
  font-size: 11px;
  color: #6b7280;
  text-transform: uppercase;
  font-weight: 600;
}

.invoice-info strong {
  font-size: 13px;
  color: #111827;
}

.items-section {
  margin-top: 5px;
}

.items-section h3 {
  margin: 0 0 12px;
  font-size: 16px;
  color: #111827;
}

.items-table {
  width: 100%;
  border-collapse: collapse;
}

.items-table th {
  padding: 11px 12px;
  text-align: left;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
  font-size: 11px;
  color: #374151;
}

.items-table td {
  padding: 12px;
  border-bottom: 1px solid #eef0f3;
  font-size: 12px;
  color: #374151;
}

.details-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 15px;
  border-radius: 9px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
}

.details-total span {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
}

.details-total strong {
  font-size: 21px;
  color: #111827;
}

.invoice-card tbody::-webkit-scrollbar,
.invoice-details::-webkit-scrollbar {
  width: 6px;
}

.invoice-card tbody::-webkit-scrollbar-track,
.invoice-details::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.invoice-card tbody::-webkit-scrollbar-thumb,
.invoice-details::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.invoice-card tbody::-webkit-scrollbar-thumb:hover,
.invoice-details::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

@media (max-width: 800px) {
  .invoices-page {
    height: auto;
    overflow: visible;
  }

  .invoice-card {
    overflow-x: auto;
  }

  .invoice-card table {
    min-width: 700px;
  }

  .invoice-card tbody {
    height: 400px;
  }

  .invoice-info {
    grid-template-columns: repeat(2, 1fr);
  }

  .modal-overlay {
    padding: 15px;
  }

  .invoice-details {
    padding: 20px;
  }
}

@media (max-width: 500px) {
  .invoice-info {
    grid-template-columns: 1fr;
  }
}
.print-button {
  width: 100%;
  margin-top: 15px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  background: #111827;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.print-button:hover {
  background: #1f2937;
}
.print-button {
  width: 100%;
  margin-top: 15px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  background: #111827;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.print-button:hover {
  background: #1f2937;
}
</style>
