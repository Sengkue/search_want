export function useApi() {
  const config = useRuntimeConfig()

  /** True when running inside the Capacitor Android/iOS shell (the APK). */
  const isNativeApp = (): boolean => {
    if (!import.meta.client) return false
    const cap = (window as any).Capacitor
    return Boolean(cap?.isNativePlatform?.())
  }

  const getBaseUrl = (): string => {
    // 1. Explicit backend URL, set at build time with NUXT_PUBLIC_API_BASE
    //    (required for the APK on a real phone: e.g. http://<PC-LAN-IP>:8000).
    if (config.public.apiBase) {
      return String(config.public.apiBase).replace(/\/$/, '')
    }
    // 2. APK without a configured URL: 10.0.2.2 is the Android emulator's alias for the host PC.
    if (isNativeApp()) {
      return 'http://10.0.2.2:8000'
    }
    // 3. Web browser (HTTP localhost, HTTP LAN IP, or HTTPS :3443):
    //    Use same-origin relative URL ('') so Nuxt/Nitro proxies /api/** -> FastAPI :8000
    //    cleanly without Mixed-Content errors on HTTPS or extra firewall ports on Wi-Fi!
    if (import.meta.client) {
      return ''
    }
    return 'http://127.0.0.1:8000'
  }

  const getToken = (): string | null => {
    if (!import.meta.client) return null
    return localStorage.getItem('sw_access_token')
  }

  async function apiFetch<T>(
    path: string,
    options: {
      method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
      body?: Record<string, any> | null
      params?: Record<string, any>
    } = {},
  ): Promise<T> {
    const token = getToken()
    const headers: Record<string, string> = {}
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }

    // Filter out null/undefined query params cleanly
    const cleanParams: Record<string, any> = {}
    if (options.params) {
      for (const [k, v] of Object.entries(options.params)) {
        if (v !== undefined && v !== null && v !== '') {
          cleanParams[k] = v
        }
      }
    }

    return await $fetch<T>(`${getBaseUrl()}${path}`, {
      method: options.method || 'GET',
      headers,
      body: options.body ?? undefined,
      query: Object.keys(cleanParams).length > 0 ? cleanParams : undefined,
    })
  }

  return {
    getBaseUrl,
    isNativeApp,
    apiFetch,
  }
}
