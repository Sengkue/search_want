import type { AdSenseConfig, AdSenseConfigPayload } from '~/types/api'

const PUB_ID_REGEX = /^ca-pub-\d{16}$/
let adsenseScriptInjected = false
let interactionListenersAttached = false

export function useAdSense() {
  const runtimeConfig = useRuntimeConfig()
  const { apiFetch, isNativeApp } = useApi()
  const route = useRoute()

  const adsenseConfig = useState<AdSenseConfig>('sw_adsense_config', () => ({
    enabled: true,
    client_id: String(runtimeConfig.public.adsenseClientId || ''),
    publisher_id: '',
    slot_infeed: String(runtimeConfig.public.adsenseSlotInfeed || ''),
    slot_banner: String(runtimeConfig.public.adsenseSlotBanner || ''),
    auto_ads: true,
    test_mode: true,
    ads_txt_line: '',
    updated_at: '',
  }))

  const adsenseLoaded = useState<boolean>('sw_adsense_loaded', () => false)

  const effectiveClientId = computed(() =>
    (adsenseConfig.value.client_id || String(runtimeConfig.public.adsenseClientId || '')).trim(),
  )

  const effectiveSlotInfeed = computed(() =>
    (adsenseConfig.value.slot_infeed || String(runtimeConfig.public.adsenseSlotInfeed || '')).trim(),
  )

  const effectiveSlotBanner = computed(() =>
    (adsenseConfig.value.slot_banner || String(runtimeConfig.public.adsenseSlotBanner || '')).trim(),
  )

  const hasValidClientId = computed(() => PUB_ID_REGEX.test(effectiveClientId.value))

  /**
   * Google AdSense policy compliance:
   * - Never load Web AdSense inside Capacitor native APK WebViews
   * - Never load AdSense on /login or /admin moderation screens
   */
  const isAdAllowedOnRoute = computed(() => {
    if (isNativeApp()) return false
    const path = route.path || '/'
    if (path.startsWith('/admin') || path.startsWith('/login')) return false
    return true
  })

  const isLocalOrPrivateHost = computed(() => {
    if (!import.meta.client) return false
    const host = window.location.hostname
    return (
      host === 'localhost' ||
      host === '127.0.0.1' ||
      host.startsWith('10.') ||
      host.startsWith('192.168.') ||
      /^172\.(1[6-9]|2\d|3[0-1])\./.test(host)
    )
  })

  async function loadAdSenseConfig(force = false): Promise<AdSenseConfig> {
    if (adsenseLoaded.value && !force) {
      return adsenseConfig.value
    }
    try {
      const data = await apiFetch<AdSenseConfig>('/api/adsense/config')
      adsenseConfig.value = data
      adsenseLoaded.value = true
    } catch {
      // Keep safe runtime fallback if offline
      adsenseLoaded.value = true
    }
    return adsenseConfig.value
  }

  async function updateAdSenseConfig(payload: AdSenseConfigPayload): Promise<AdSenseConfig> {
    const updated = await apiFetch<AdSenseConfig>('/api/admin/adsense', {
      method: 'PUT',
      body: payload,
    })
    adsenseConfig.value = updated
    adsenseLoaded.value = true
    return updated
  }

  /**
   * Injects external Google AdSense `adsbygoogle.js` ONLY on live approved public domains
   * when `test_mode` is turned OFF, and defers injection until first user interaction
   * (`scroll` / `pointerdown` / `touchstart` / `keydown`) so initial FCP, LCP, TBT,
   * and Best Practices (zero unsolicited 3rd-party cookies on load) stay 95-100!
   */
  function scheduleLiveAdSenseScript() {
    if (!import.meta.client || adsenseScriptInjected) return
    if (
      !adsenseConfig.value.enabled ||
      !hasValidClientId.value ||
      !isAdAllowedOnRoute.value ||
      adsenseConfig.value.test_mode ||
      isLocalOrPrivateHost.value
    ) {
      return
    }

    const injectNow = () => {
      if (adsenseScriptInjected) return
      adsenseScriptInjected = true
      const s = document.createElement('script')
      s.async = true
      s.crossOrigin = 'anonymous'
      s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(effectiveClientId.value)}`
      document.head.appendChild(s)
    }

    if (!interactionListenersAttached) {
      interactionListenersAttached = true
      const events = ['scroll', 'pointerdown', 'touchstart', 'keydown'] as const
      const onInteract = () => {
        for (const ev of events) {
          window.removeEventListener(ev, onInteract)
        }
        injectNow()
      }
      for (const ev of events) {
        window.addEventListener(ev, onInteract, { once: true, passive: true })
      }
    }
  }

  function registerAdSenseHead() {
    useHead(() => {
      if (!adsenseConfig.value.enabled || !hasValidClientId.value || isNativeApp()) {
        return {}
      }

      // Always keep verification meta tag in SSR <head> for Google AdSense crawler ownership check
      return {
        meta: [
          {
            key: 'google-adsense-account',
            name: 'google-adsense-account',
            content: effectiveClientId.value,
          },
        ],
      }
    })

    if (import.meta.client) {
      watch(
        () => [
          adsenseConfig.value.enabled,
          adsenseConfig.value.test_mode,
          effectiveClientId.value,
          isAdAllowedOnRoute.value,
        ],
        () => {
          scheduleLiveAdSenseScript()
        },
        { immediate: true },
      )
    }
  }

  return {
    adsenseConfig,
    adsenseLoaded,
    effectiveClientId,
    effectiveSlotInfeed,
    effectiveSlotBanner,
    hasValidClientId,
    isAdAllowedOnRoute,
    isLocalOrPrivateHost,
    loadAdSenseConfig,
    updateAdSenseConfig,
    registerAdSenseHead,
    scheduleLiveAdSenseScript,
  }
}
