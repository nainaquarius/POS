<script setup>
import { onMounted, ref } from 'vue'
import api from '../services/api'

const error = ref('')
const loading = ref(false)
const invoices = ref([])

const fetchInvoices = async () => {
  error.value = ''
  loading.value = true

  try {
    const response = await api.get('/vat')
    invoices.value = response.data
    console.log(response.data)
  } catch (err) {
    console.log(err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchInvoices()
})
</script>

<template>
  <h1>Hello from vat</h1>
</template>
