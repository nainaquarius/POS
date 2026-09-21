<script setup>
import { computed, onMounted, ref } from "vue";
import api from "../services/api";

const products = ref([]);
const loading = ref(false);
const error = ref("");
const search = ref("");
const showForm = ref(false);
const editingProduct = ref(null);

const deleteProduct = async (product) => {
  const confirmed = confirm(`Are you sure you want to deactivate "${product.name}"?"`);

  if (!confirmed) {
    return;
  }

  try {
    await api.delete(`/products/${product.id}`)

    await fetchProducts();
  } catch (err) {
    console.error(err);
    err.value = err.response?.data?.detail || "Failed to deactivate product."
  }
}

const editProduct = (product) => {
  editingProduct.value = product;

  form.value = {
    name: product.name,
    sku: product.sku,
    barcode: product.barcode,
    category: product.category,
    price: product.price,
    cost_price: product.cost_price,
    stock: product.stock,
    low_stock_threshold: product.low_stock_threshold,
    description: product.description,
  };

  showForm.value = true;
}

const updateProduct = async () => {
  formError.value = "";
  submitting.value = true;

  try {
    await api.put(
      `/products/${editingProduct.value.id}`,
      form.value
    );

    showForm.value = false;
    editingProduct.value = null;

    await fetchProducts();
  } catch (err) {
    console.error(err);

    formError.value =
      err.response?.data?.detail || "Failed to update product.";
  } finally {
    submitting.value = false;
  }
};

const form = ref({
  name: "",
  sku: "",
  barcode: "",
  category: "",
  price: 0,
  cost_price: 0,
  stock: 0,
  low_stock_threshold: 5,
  description: "",
});

const formError = ref("");
const submitting = ref(false);

const addProduct = async () => {
  editProduct.value = null;
  formError.value = "";
  submitting.value = true;

  try {
    await api.post("/products", form.value);

    showForm.value = false;

    form.value = {
      name: "",
      sku: "",
      barcode: "",
      category: "",
      price: 0,
      cost_price: 0,
      stock: 0,
      low_stock_threshold: 5,
      description: "",
    };

    await fetchProducts();

  } catch (err) {
    console.error(err);
    
    formError.value = err.response?.data?.detail || "Failed to add product.";
  } finally {
    submitting.value = false
  }
};

const fetchProducts = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await api.get("/products");
    products.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = "Failed to load products.";
  } finally {
    loading.value = false;
  }
};

const filteredProducts = computed(() => {
  const keyword = search.value.toLowerCase().trim();

  if (!keyword) {
    return products.value;
  }

  return products.value.filter((product) => {
    return (
      product.name.toLowerCase().includes(keyword) ||
      product.sku.toLowerCase().includes(keyword) ||
      product.barcode.toLowerCase().includes(keyword) ||
      product.category.toLowerCase().includes(keyword)
    );
  });
});

const getStockStatus = (product) => {
  if (product.stock === 0) {
    return "Out of Stock";
  }

  if (product.stock <= product.low_stock_threshold) {
    return "Low Stock";
  }

  return "In Stock";
};

onMounted(() => {
  fetchProducts();
});
</script>

<template>
  <div class="products-page">
    <div class="page-header">
      <div>
        <h1>Products</h1>
        <p>Manage your products and inventory.</p>
      </div>

      <button class="add-button" @click="showForm = true">
        + Add Product
      </button>
    </div>

    <div class="toolbar">
      <input
        v-model="search"
        type="text"
        placeholder="Search by name, SKU, barcode or category..."
      />
    </div>

    <p v-if="loading" class="message">
      Loading products...
    </p>

    <p v-if="error" class="error">
      {{ error }}
    </p>

    <div v-if="!loading && filteredProducts.length" class="table-container">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>SKU</th>
            <th>Barcode</th>
            <th>Category</th>
            <th>Price</th>
            <th>Stock</th>
            <th>Status</th>
            <th>Action</th>
            <th>Delete</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="product in filteredProducts"
            :key="product.id"
          >
            <td class="product-name">
              {{ product.name }}
            </td>

            <td>{{ product.sku }}</td>

            <td>{{ product.barcode }}</td>

            <td>{{ product.category }}</td>

            <td>
              {{ Number(product.price).toFixed(2) }}
            </td>

            <td>{{ product.stock }}</td>

            <td>
              <span
                class="status"
                :class="{
                  'status-out': product.stock === 0,
                  'status-low':
                    product.stock > 0 &&
                    product.stock <= product.low_stock_threshold,
                  'status-good':
                    product.stock > product.low_stock_threshold,
                }"
              >
                {{ getStockStatus(product) }}
              </span>
            </td>
            <td>
              <button
                class="edit-button"
                @click="editProduct(product)"
              >Edit</button>
            </td>
            <td
              class="delete-button"
              @click="deleteProduct(product)"
            >
              Deactivate
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p
      v-if="!loading && !filteredProducts.length"
      class="message"
    >
      No products found.
    </p>
  </div>

  <div v-if="showForm" class="product-form">
    <div class="form-header">
      <h2>{{ editingProduct ? "Edit Product" : "Add Product" }}</h2>

      <button
        type="button"
        class="close-button"
        @click="showForm = false"
      >
        ×
      </button>
    </div>

    <form @submit.prevent="editingProduct ? updateProduct() : addProduct()">
      <div class="form-grid">
        <div class="form-group">
          <label>Name</label>
          <input v-model="form.name" required />
        </div>

        <div class="form-group">
          <label>SKU</label>
          <input v-model="form.sku" required />
        </div>

        <div class="form-group">
          <label>Barcode</label>
          <input v-model="form.barcode" required />
        </div>

        <div class="form-group">
          <label>Category</label>
          <input v-model="form.category" required />
        </div>

        <div class="form-group">
          <label>Price</label>
          <input
            v-model.number="form.price"
            type="number"
            min="0"
            step="0.01"
            required
          />
        </div>

        <div class="form-group">
          <label>Cost Price</label>
          <input
            v-model.number="form.cost_price"
            type="number"
            min="0"
            step="0.01"
            required
          />
        </div>

        <div class="form-group">
          <label>Stock</label>
          <input
            v-model.number="form.stock"
            type="number"
            min="0"
            required
          />
        </div>

        <div class="form-group">
          <label>Low Stock Threshold</label>
          <input
            v-model.number="form.low_stock_threshold"
            type="number"
            min="0"
            required
          />
        </div>

        <div class="form-group full-width">
          <label>Description</label>
          <textarea
            v-model="form.description"
            rows="3"
          ></textarea>
        </div>
      </div>

      <p v-if="formError" class="error">
        {{ formError }}
      </p>

      <div class="form-actions">
        <button
          type="button"
          class="cancel-button"
          @click="showForm = false"
        >
          Cancel
        </button>

        <button
          type="submit"
          class="save-button"
          :disabled="submitting"
        >
          {{ submitting ? "Saving..." : editingProduct ? "Update Product" : "Save Product" }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.products-page {
  width: 100%;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 25px;
}

.page-header h1 {
  margin: 0 0 5px;
}

.page-header p {
  margin: 0;
  color: #6b7280;
}

.add-button {
  border: none;
  background: #1f2937;
  color: white;
  padding: 11px 18px;
  border-radius: 7px;
  cursor: pointer;
}

.add-button:hover {
  background: #374151;
}

.toolbar {
  background: white;
  padding: 18px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.toolbar input {
  width: 100%;
  max-width: 450px;
  padding: 11px 14px;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  outline: none;
}

.toolbar input:focus {
  border-color: #6b7280;
}

.table-container {
  background: white;
  border-radius: 10px;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

th,
td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

th {
  background: #f9fafb;
  font-size: 13px;
  color: #6b7280;
  text-transform: uppercase;
}

td {
  font-size: 14px;
}

.product-name {
  font-weight: 600;
}

.status {
  display: inline-block;
  padding: 5px 9px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.status-good {
  background: #dcfce7;
  color: #166534;
}

.status-low {
  background: #fef3c7;
  color: #92400e;
}

.status-out {
  background: #fee2e2;
  color: #991b1b;
}

.message {
  padding: 20px;
  text-align: center;
  color: #6b7280;
}

.error {
  color: #dc2626;
}
.product-form {
  background: white;
  padding: 25px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.form-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.form-header h2 {
  margin: 0;
}

.close-button {
  border: none;
  background: transparent;
  font-size: 25px;
  cursor: pointer;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  outline: none;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #6b7280;
}

.full-width {
  grid-column: 1 / -1;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.cancel-button,
.save-button {
  border: none;
  padding: 10px 18px;
  border-radius: 7px;
  cursor: pointer;
}

.cancel-button {
  background: #e5e7eb;
}

.save-button {
  background: #1f2937;
  color: white;
}

.save-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.edit-button {
  border: none;
  background: #e5e7eb;
  color: #1f2937;
  padding: 7px 12px;
  border-radius: 6px;
  cursor: pointer;
}

.edit-button:hover {
  background: #d1d5db;
}
.delete-button {
  border: none;
  background: #fee2e2;
  color: #991b1b;
  padding: 7px 12px;
  border-radius: 6px;
  cursor: pointer;
  margin-left: 8px;
}

.delete-button:hover {
  background: #fecaca;
}
</style>