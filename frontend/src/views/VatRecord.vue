<script setup>
import { ref } from 'vue'
import api from '../services/api'

const error = ref('')
const loading = ref(false)
const invoiceNumber = ref('')
const vatRecord = ref(null)

const generateVatRecord = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await api.post('/vat/', {
      invoice_number: invoiceNumber.value,
    })
    vatRecord.value = response.data
  } catch (err) {
    console.log(err)
    error.value = err?.response?.data?.detail || 'Something went wrong'
  } finally {
    loading.value = false
  }
}

generateVatRecord()
</script>

<template>
  <h1>Hello from vat</h1>
</template>
