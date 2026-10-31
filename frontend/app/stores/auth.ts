import { defineStore } from 'pinia'
import type {
  NotificationOut,
  PublicSecurityConfig,
  TokenResponse,
  UserOut,
} from '~/types/api'

export function isSafeInternalPath(path: unknown): path is string {
  return (
    typeof path === 'string' &&
    path.startsWith('/') &&
    !path.startsWith('//') &&
    !path.includes('://')
  )
}

export const useAuthStore = defineStore('auth', () => {
  const { apiFetch } = useApi()

  const user = ref<UserOut | null>(null)
  const token = ref<string | null>(null)
  const notifications = ref<NotificationOut[]>([])
  const initialized = ref(false)
  let initPromise: Promise<void> | null = null

  // Runtime environment & production demo-gating flags fetched from backend
  const publicConfig = reactive<PublicSecurityConfig>({
    app_env: 'development',
    is_production: false,
    demo_mode: true,
  })
  const publicConfigLoaded = ref(false)

  // Global snackbar toast state for rich in-app notifications
  const toast = reactive({
    show: false,
    message: '',
    color: 'primary',
    icon: 'mdi-bell-ring-outline',
  })

  const isLoggedIn = computed(() => Boolean(token.value && user.value && user.value.is_active !== false))
  /** Both ADMIN (Moderator) and SUPER_ADMIN (System Owner) can access shop moderation */
  const isAdmin = computed(
    () => user.value?.role === 'ADMIN' || user.value?.role === 'SUPER_ADMIN',
  )
  /** Strictly SUPER_ADMIN only: AdSense revenue settings, User Role RBAC, and Production Security */
  const isSuperAdmin = computed(() => user.value?.role === 'SUPER_ADMIN')
  const isShopOwner = computed(
    () => user.value?.role === 'SHOP_OWNER' || isAdmin.value,
  )
  const unreadCount = computed(() => notifications.value.filter((n) => !n.is_read).length)

  function hasPermission(perm: string): boolean {
    if (!user.value) return false
    if (user.value.role === 'SUPER_ADMIN') return true
    return Boolean(user.value.permissions?.includes(perm))
  }

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

  function clearSessionSilently() {
    token.value = null
    user.value = null
    notifications.value = []
    if (import.meta.client) {
      localStorage.removeItem('sw_access_token')
    }
  }

  function logout() {
    clearSessionSilently()
    showToast('ອອກຈາກລະບົບແລ້ວ.', 'info', 'mdi-logout')
  }

  async function loadPublicConfig(force = false) {
    if (publicConfigLoaded.value && !force) return
    try {
      const cfg = await apiFetch<PublicSecurityConfig>('/api/auth/public-config')
      publicConfig.app_env = cfg.app_env
      publicConfig.is_production = cfg.is_production
      publicConfig.demo_mode = cfg.demo_mode
      publicConfigLoaded.value = true
    } catch {
      // Keep safe defaults if backend is temporarily unreachable
    }
  }

  async function initAuth() {
    if (!import.meta.client) return
    if (initialized.value) return
    if (initPromise) {
      await initPromise
      return
    }

    initPromise = (async () => {
      await loadPublicConfig()
      const saved = localStorage.getItem('sw_access_token')
      if (!saved) {
        initialized.value = true
        return
      }
      token.value = saved
      try {
        user.value = await apiFetch<UserOut>('/api/auth/me')
        await fetchNotifications()
      } catch {
        clearSessionSilently()
      } finally {
        initialized.value = true
      }
    })()

    try {
      await initPromise
    } finally {
      initPromise = null
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

  async function changePassword(currentPassword: string, newPassword: string) {
    const resp = await apiFetch<TokenResponse>('/api/auth/change-password', {
      method: 'POST',
      body: {
        current_password: currentPassword,
        new_password: newPassword,
      },
    })
    setSession(resp)
    showToast('ປ່ຽນລະຫັດຜ່ານສຳເລັດ ແລະ ຍົກເລີກເຊດຊັນເກົ່າໃນອຸປະກອນອື່ນແລ້ວ!', 'success', 'mdi-lock-check')
    return resp.user
  }

  async function refreshMe() {
    if (!token.value) return
    try {
      user.value = await apiFetch<UserOut>('/api/auth/me')
    } catch {
      clearSessionSilently()
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
    publicConfig,
    publicConfigLoaded,
    toast,
    isLoggedIn,
    isAdmin,
    isSuperAdmin,
    isShopOwner,
    unreadCount,
    hasPermission,
    showToast,
    triggerBrowserNotification,
    requestBrowserNotificationPermission,
    loadPublicConfig,
    initAuth,
    login,
    register,
    changePassword,
    logout,
    refreshMe,
    fetchNotifications,
    markNotificationRead,
    markAllNotificationsRead,
  }
})
