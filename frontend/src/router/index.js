import { createRouter, createWebHistory } from 'vue-router'

import DashboardLayout from '../layouts/DashboardLayout.vue'
import DashboardView from '../views/DashboardView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      component: DashboardLayout,
      meta: {
        requiresAuth: true,
      },
      children: [
        {
          path: '',
          name: 'dashboard',
          component: DashboardView,
        },
        {
          path: 'products',
          name: 'products',
          component: () => import('../views/ProductsView.vue'),
        },
        {
          path: 'pos',
          name: 'pos',
          component: () => import('../views/POSView.vue'),
        },
        {
          path: 'stock',
          name: 'stock',
          component: () => import('../views/StockView.vue'),
        },
        {
          path: 'invoices',
          name: 'invoice',
          component: () => import('../views/InvoicesView.vue'),
        },
        {
          path: 'vat',
          name: 'vat',
          component: () => import('../views/VatRecord.vue'),
        },
      ],
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
  ],
})

router.beforeEach((to) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    return '/login'
  }

  if (to.name === 'login' && token) {
    return '/'
  }
})

export default router
