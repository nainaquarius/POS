<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="dashboard-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <h2>POS System</h2>

      <nav>
        <router-link to="/">Dashboard</router-link>
        <router-link to="/pos">POS</router-link>
        <router-link to="/products">Products</router-link>
        <router-link to="/invoices">Invoices</router-link>
        <router-link to="/stock">Stock</router-link>
        <router-link to="/vat">Vat Record</router-link>
      </nav>

      <button @click="handleLogout">Logout</button>
    </aside>

    <!-- Main content -->
    <div class="main-area">
      <!-- Header -->
      <header class="header">
        <div>
          <h3>Dashboard</h3>
        </div>

        <div class="user-info">
          <strong>{{ authStore.user?.name }}</strong>
          <span>{{ authStore.user?.role }}</span>
        </div>
      </header>

      <!-- Page content -->
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  display: flex;
  background: #f5f6f8;
}

.sidebar {
  width: 230px;
  background: #1f2937;
  color: white;
  padding: 25px 15px;
  display: flex;
  flex-direction: column;
}

.sidebar h2 {
  margin-bottom: 30px;
}

.sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar a {
  color: #d1d5db;
  text-decoration: none;
  padding: 10px;
  border-radius: 6px;
}

.sidebar a:hover,
.sidebar a.router-link-active {
  background: #374151;
  color: white;
}

.sidebar button {
  margin-top: auto;
  padding: 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.main-area {
  flex: 1;
}

.header {
  height: 70px;
  background: white;
  padding: 0 30px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #ddd;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-info span {
  font-size: 13px;
  color: #6b7280;
  text-transform: capitalize;
}

.content {
  padding: 30px;
}
</style>
