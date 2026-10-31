import type { AdSenseConfig, AdSenseConfigPayload } from '~/types/api'

const PUB_ID_REGEX = /^ca-pub-\d{16}$/

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

  function registerAdSenseHead() {
    useHead(() => {
      if (!adsenseConfig.value.enabled || !hasValidClientId.value || isNativeApp()) {
        return {}
      }

      const clientId = effectiveClientId.value
      const meta = [
        {
          key: 'google-adsense-account',
          name: 'google-adsense-account',
          content: clientId,
        },
      ]

      const shouldLoadScript =
        isAdAllowedOnRoute.value &&
        (adsenseConfig.value.auto_ads ||
          Boolean(effectiveSlotInfeed.value) ||
          Boolean(effectiveSlotBanner.value))

      const script = shouldLoadScript
        ? [
            {
              key: 'google-adsense-script',
              src: `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${encodeURIComponent(clientId)}`,
              async: true,
              crossorigin: 'anonymous' as const,
            },
          ]
        : []

      return { meta, script }
    })
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
  }
}

