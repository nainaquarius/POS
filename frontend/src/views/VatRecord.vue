<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
const error = ref('')
const fromDate = ref('')
const toDate = ref('')
const records = ref([])

const fetchVatRecords = async () => {
  try {
    error.value = ''
    const response = await api.get('/vat/', {
      params: {
        from_date: fromDate.value || undefined,
        to_date: toDate.value || undefined,
      },
    })

    records.value = response.data
  } catch (err) {
    error.value = err?.response?.data?.detail || 'Unable to load VAT records'
  }
}

const exportExcel = async () => {
  try {
    error.value = ''
    const response = await api.get('/vat/export', {
      params: {
        from_date: fromDate.value || undefined,
        to_date: toDate.value || undefined,
      },
      responseType: 'blob',
    })

    const blobUrl = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = blobUrl
    link.download = 'vat_records.xlsx'
    link.click()

    window.URL.revokeObjectURL(blobUrl)
  } catch (err) {
    error.value = err?.response?.data?.detail || 'Unable to export Excel file'
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}
onMounted(() => {
  fetchVatRecords()
})
</script>
<template>
  <div class="vat-page">
    <!-- Header -->
    <div class="page-header">
      <div>
        <span class="eyebrow">TAX MANAGEMENT</span>
        <h1>VAT Records</h1>
        <p>Review VAT records and export reports by date range.</p>
      </div>
      <div class="vat-badge"><span>VAT</span> <strong>5%</strong></div>
    </div>
    <!-- Filter Section -->
    <div class="filter-section">
      <div>
        <label for="fromDate">From Date</label>
        <input id="fromDate" v-model="fromDate" type="date" />
      </div>
      <div>
        <label for="toDate">To Date</label> <input id="toDate" v-model="toDate" type="date" />
      </div>
      <button type="button" @click="fetchVatRecords">Search</button>
      <button type="button" @click="exportExcel">Export Excel</button>
    </div>
    <!-- Error -->
    <div v-if="error" class="error-message">
      <span class="error-icon">!</span>
      <div>
        <strong>Something went wrong</strong>
        <p>{{ error }}</p>
      </div>
    </div>
    <!-- VAT Records Table -->
    <div v-if="records.length" class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Invoice Number</th>
            <th>Product Name</th>
            <th>Date</th>
            <th>Invoice Price</th>
            <th>VAT 5%</th>
            <th>Total Amount</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.invoice_number">
            <td>{{ record.invoice_number }}</td>
            <td>{{ record.product_names }}</td>
            <td>{{ formatDate(record.date) }}</td>
            <td>{{ Number(record.invoice_price).toFixed(2) }}</td>
            <td>{{ Number(record.vat).toFixed(2) }}</td>
            <td>{{ Number(record.total_amount).toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Empty State -->
    <p v-else class="empty-state">No VAT records found.</p>
  </div>
</template>

<style scoped>
.vat-page {
  min-height: 100%;
  padding: 28px;

  background:
    radial-gradient(circle at 90% 5%, rgba(99, 102, 241, 0.12), transparent 28%),
    radial-gradient(circle at 10% 30%, rgba(16, 185, 129, 0.08), transparent 25%);
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 28px;
}

.page-header h1 {
  margin: 5px 0 6px;

  color: #f8fafc;
  font-size: 32px;
  font-weight: 750;
  letter-spacing: -0.8px;
}

.page-header p {
  margin: 0;

  color: #94a3b8;
  font-size: 14px;
}

.eyebrow {
  display: inline-block;

  color: #818cf8;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.8px;
}

.vat-badge {
  display: flex;
  align-items: center;
  gap: 10px;

  padding: 13px 18px;

  border: 1px solid rgba(129, 140, 248, 0.25);
  border-radius: 14px;

  background: rgba(99, 102, 241, 0.08);

  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.vat-badge span {
  color: #a5b4fc;

  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
}

.vat-badge strong {
  color: #818cf8;
  font-size: 20px;
}

.filter-section {
  display: flex;
  align-items: flex-end;
  gap: 14px;

  margin-bottom: 24px;
  padding: 22px 26px;

  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 18px;

  background: rgba(15, 23, 42, 0.72);

  backdrop-filter: blur(18px);

  box-shadow:
    0 20px 60px rgba(0, 0, 0, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.filter-section > div {
  min-width: 170px;
}

.filter-section label {
  display: block;

  margin-bottom: 8px;

  color: #cbd5e1;
  font-size: 12px;
  font-weight: 600;
}

.filter-section input {
  width: 100%;
  box-sizing: border-box;

  height: 44px;
  padding: 0 12px;

  border: 1px solid #334155;
  border-radius: 11px;

  outline: none;

  color: #e2e8f0;
  background: rgba(15, 23, 42, 0.8);

  transition: 0.2s ease;
}

.filter-section input:focus {
  border-color: #818cf8;

  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.filter-section button {
  height: 44px;

  padding: 0 22px;

  border: none;
  border-radius: 11px;

  color: white;

  background: linear-gradient(135deg, #6366f1, #8b5cf6);

  font-size: 13px;
  font-weight: 650;

  white-space: nowrap;

  cursor: pointer;

  box-shadow: 0 8px 22px rgba(99, 102, 241, 0.22);

  transition: all 0.2s ease;
}

.filter-section button:hover {
  transform: translateY(-2px);

  box-shadow: 0 12px 28px rgba(99, 102, 241, 0.3);
}

.filter-section button:active {
  transform: translateY(0);
}

.error-message {
  display: flex;
  align-items: flex-start;
  gap: 12px;

  margin-bottom: 24px;
  padding: 14px 16px;

  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 12px;

  background: rgba(239, 68, 68, 0.07);
}

.error-icon {
  display: flex;
  align-items: center;
  justify-content: center;

  flex-shrink: 0;

  width: 24px;
  height: 24px;

  border-radius: 50%;

  color: #fecaca;
  background: rgba(239, 68, 68, 0.18);

  font-weight: 700;
}

.error-message strong {
  color: #fca5a5;
  font-size: 13px;
}

.error-message p {
  margin: 3px 0 0;

  color: #94a3b8;
  font-size: 12px;
}

/* ================================
   TABLE
================================ */

.table-wrapper {
  overflow-x: auto;

  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;

  background: rgba(15, 23, 42, 0.55);

  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.16);
}

table {
  width: 100%;
  min-width: 850px;

  border-collapse: collapse;
}

thead {
  background: rgba(30, 41, 59, 0.7);
}

th {
  padding: 14px 16px;

  color: #94a3b8;

  font-size: 10px;
  font-weight: 700;

  text-align: left;
  text-transform: uppercase;

  letter-spacing: 0.8px;
}

td {
  padding: 15px 16px;

  border-top: 1px solid rgba(148, 163, 184, 0.07);

  color: #cbd5e1;

  font-size: 13px;
}

tbody tr {
  transition: background 0.2s ease;
}

tbody tr:hover {
  background: rgba(99, 102, 241, 0.055);
}

td:first-child {
  color: #a5b4fc;
  font-weight: 650;
}

td:nth-child(4),
td:nth-child(5),
td:nth-child(6) {
  font-variant-numeric: tabular-nums;
  font-weight: 600;
}

td:nth-child(5) {
  color: #6ee7b7;
}

td:nth-child(6) {
  color: #a5b4fc;
}

.empty-state {
  margin: 0;

  padding: 60px 20px;

  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 16px;

  color: #64748b;

  background: rgba(15, 23, 42, 0.55);

  text-align: center;

  font-size: 13px;
}

@media (max-width: 900px) {
  .vat-page {
    padding: 18px;
  }

  .filter-section {
    flex-wrap: wrap;
  }

  .filter-section > div {
    flex: 1;
  }

  .filter-section button {
    flex: 0 0 auto;
  }
}

@media (max-width: 600px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .page-header h1 {
    font-size: 26px;
  }

  .vat-badge {
    align-self: flex-start;
  }

  .filter-section {
    flex-direction: column;
    align-items: stretch;

    padding: 18px;
  }

  .filter-section > div {
    width: 100%;
  }

  .filter-section button {
    width: 100%;
  }

  .table-wrapper {
    border-radius: 12px;
  }
}
</style>
