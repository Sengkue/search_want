import { defineStore } from 'pinia'
import type { NotificationOut, TokenResponse, UserOut } from '~/types/api'

export const useAuthStore = defineStore('auth', () => {
  const { apiFetch } = useApi()

  const user = ref<UserOut | null>(null)
  const token = ref<string | null>(null)
  const notifications = ref<NotificationOut[]>([])
  const initialized = ref(false)

  // Global snackbar toast state for rich in-app notifications
  const toast = reactive({
    show: false,
    message: '',
    color: 'primary',
    icon: 'mdi-bell-ring-outline',
  })

  const isLoggedIn = computed(() => Boolean(token.value && user.value))
  const isAdmin = computed(() => user.value?.role === 'ADMIN')
  const unreadCount = computed(() => notifications.value.filter((n) => !n.is_read).length)

  function showToast(
    message: string,
    color: 'primary' | 'success' | 'warning' | 'error' | 'info' = 'primary',
    icon = 'mdi-bell-ring-outline',
  ) {
    toast.message = message
    toast.color = color
    toast.icon = icon
    toast.show = true
  }

  function triggerBrowserNotification(title: string, body: string) {
    if (!import.meta.client || !('Notification' in window)) return
    if (Notification.permission === 'granted') {
      try {
        new Notification(title, { body })
      } catch {
        // Ignore on mobile browsers requiring service-worker registration
      }
    }
  }

  async function requestBrowserNotificationPermission() {
    if (!import.meta.client || !('Notification' in window)) return false
    if (Notification.permission === 'granted') return true
    if (Notification.permission !== 'denied') {
      const perm = await Notification.requestPermission()
      return perm === 'granted'
    }
    return false
  }

  function setSession(resp: TokenResponse) {
    token.value = resp.access_token
    user.value = resp.user
    if (import.meta.client) {
      localStorage.setItem('sw_access_token', resp.access_token)
    }
  }

  function logout() {
    token.value = null
    user.value = null
    notifications.value = []
    if (import.meta.client) {
      localStorage.removeItem('sw_access_token')
    }
    showToast('ອອກຈາກລະບົບແລ້ວ.', 'info', 'mdi-logout')
  }

  async function initAuth() {
    if (initialized.value) return
    initialized.value = true
    if (!import.meta.client) return
    const saved = localStorage.getItem('sw_access_token')
    if (!saved) return
    token.value = saved
    try {
      user.value = await apiFetch<UserOut>('/api/auth/me')
      await fetchNotifications()
    } catch {
      token.value = null
      user.value = null
      localStorage.removeItem('sw_access_token')
    }
  }

  async function login(email: string, password: string) {
    const resp = await apiFetch<TokenResponse>('/api/auth/login', {
      method: 'POST',
      body: { email, password },
    })
    setSession(resp)
    await fetchNotifications()
    showToast(`ຍິນດີຕ້ອນຮັບກັບມາ, ${resp.user.full_name}!`, 'success', 'mdi-check-circle-outline')
    return resp.user
  }

  async function register(payload: {
    email: string
    password: string
    full_name: string
    phone?: string
  }) {
    const resp = await apiFetch<TokenResponse>('/api/auth/register', {
      method: 'POST',
      body: payload,
    })
    setSession(resp)
    await fetchNotifications()
    showToast(`ສ້າງບັນຊີສຳເລັດ! ຍິນດີຕ້ອນຮັບ, ${resp.user.full_name}.`, 'success', 'mdi-account-check')
    return resp.user
  }

  async function refreshMe() {
    if (!token.value) return
    try {
      user.value = await apiFetch<UserOut>('/api/auth/me')
    } catch {
      // ignore
    }
  }

  async function fetchNotifications() {
    if (!token.value) return
    try {
      notifications.value = await apiFetch<NotificationOut[]>('/api/notifications')
    } catch {
      // ignore
    }
  }

  async function markNotificationRead(id: number) {
    try {
      const updated = await apiFetch<NotificationOut>(`/api/notifications/${id}/read`, {
        method: 'POST',
      })
      const idx = notifications.value.findIndex((n) => n.id === id)
      if (idx !== -1) notifications.value[idx] = updated
    } catch {
      // ignore
    }
  }

  async function markAllNotificationsRead() {
    try {
      await apiFetch('/api/notifications/read-all', { method: 'POST' })
      notifications.value = notifications.value.map((n) => ({ ...n, is_read: true }))
    } catch {
      // ignore
    }
  }

  return {
    user,
    token,
    notifications,
    initialized,
    toast,
    isLoggedIn,
    isAdmin,
    unreadCount,
    showToast,
    triggerBrowserNotification,
    requestBrowserNotificationPermission,
    initAuth,
    login,
    register,
    logout,
    refreshMe,
    fetchNotifications,
    markNotificationRead,
    markAllNotificationsRead,
  }
})

