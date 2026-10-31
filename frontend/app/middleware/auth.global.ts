import { isSafeInternalPath, useAuthStore } from '~/stores/auth'

/**
 * Global Role-Based Access Control (RBAC) Route Guard:
 * - Protects `/admin/**` for ADMIN & SUPER_ADMIN only (redirects guests to `/login`, blocks regular users/owners)
 * - Restricts `?tab=ADSENSE` and `?tab=RBAC` inside `/admin/approvals` strictly to `SUPER_ADMIN`
 * - Protects `/shops/mine` for authenticated users
 * - Prevents already logged-in users from getting stuck on `/login` and sanitizes `?redirect=`
 */
export default defineNuxtRouteMiddleware(async (to) => {
  if (!import.meta.client) return

  const authStore = useAuthStore()
  await authStore.initAuth()

  // 1. Protect all /admin/* routes
  if (to.path.startsWith('/admin')) {
    if (!authStore.isLoggedIn) {
      return navigateTo({
        path: '/login',
        query: { redirect: to.fullPath },
      })
    }

    if (!authStore.isAdmin) {
      authStore.showToast(
        'ທ່ານບໍ່ມີສິດເຂົ້າເຖິງໜ້າຜູ້ດູແລລະບົບ.',
        'error',
        'mdi-shield-lock-outline',
      )
      return navigateTo('/')
    }

    // Super-Admin-only tabs inside /admin/approvals
    const requestedTab = typeof to.query.tab === 'string' ? to.query.tab.toUpperCase() : ''
    if ((requestedTab === 'ADSENSE' || requestedTab === 'RBAC') && !authStore.isSuperAdmin) {
      authStore.showToast(
        'ສະເພາະຜູ້ບໍລິຫານສູງສຸດ (Super Admin) ເທົ່ານັ້ນທີ່ເຂົ້າຕັ້ງຄ່າສ່ວນນີ້ໄດ້.',
        'warning',
        'mdi-shield-crown-outline',
      )
      return navigateTo({ path: '/admin/approvals', query: {} })
    }
  }

  // 2. Protect /shops/mine for authenticated users
  if (to.path === '/shops/mine' && !authStore.isLoggedIn) {
    return navigateTo({
      path: '/login',
      query: { redirect: '/shops/mine' },
    })
  }

  // 3. Redirect already authenticated users away from /login safely
  if (to.path === '/login' && authStore.isLoggedIn) {
    const redir = to.query.redirect
    if (isSafeInternalPath(redir) && redir !== '/login') {
      return navigateTo(redir)
    }
    return navigateTo(authStore.isAdmin ? '/admin/approvals' : '/')
  }
})
