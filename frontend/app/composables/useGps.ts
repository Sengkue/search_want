export interface GpsResult {
  ok: boolean
  lat?: number
  lng?: number
  reason?: 'insecure_origin' | 'permission_denied' | 'unavailable' | 'unsupported'
  messageLao?: string
}

function browserPositionOnce(options: PositionOptions): Promise<GeolocationPosition> {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(resolve, reject, options)
  })
}

export function useGps() {
  const { isNativeApp } = useApi()
  const config = useRuntimeConfig()

  // Global shared state so any page's GPS button can open the friendly HTTPS/Map helper dialog
  const gpsSecureDialogOpen = useState<boolean>('sw_gps_secure_dialog', () => false)
  const requestMapPinPickCount = useState<number>('sw_request_map_pin_pick', () => 0)

  const httpsPort = computed(() => String(config.public.httpsPort || '3443'))

  function buildSecureHttpsUrl(): string {
    if (!import.meta.client) return 'https://localhost:3443'
    const url = new URL(window.location.href)
    url.protocol = 'https:'
    url.port = httpsPort.value
    url.searchParams.set('autoGps', '1')
    return url.toString()
  }

  function buildLocalhostUrl(): string {
    if (!import.meta.client) return 'http://localhost:3000'
    const url = new URL(window.location.href)
    url.protocol = 'http:'
    url.hostname = 'localhost'
    url.port = window.location.port || '3000'
    url.searchParams.set('autoGps', '1')
    return url.toString()
  }

  function triggerManualMapPick() {
    gpsSecureDialogOpen.value = false
    requestMapPinPickCount.value += 1
  }

  async function getCurrentCoordinates(): Promise<GpsResult> {
    if (!import.meta.client) {
      return { ok: false, reason: 'unsupported' }
    }

    // 1. Native Android / iOS Capacitor APK -> Use hardware OS location plugin (@capacitor/geolocation)
    if (isNativeApp()) {
      try {
        const { Geolocation } = await import('@capacitor/geolocation')
        const perm = await Geolocation.checkPermissions()
        if (perm.location !== 'granted' && perm.coarseLocation !== 'granted') {
          const req = await Geolocation.requestPermissions()
          if (req.location !== 'granted' && req.coarseLocation !== 'granted') {
            return {
              ok: false,
              reason: 'permission_denied',
              messageLao:
                'ກະລຸນາອະນຸຍາດສິດ Location ໃຫ້ແອັບ Search-Want ໃນຕັ້ງຄ່າໂທລະສັບ ຫຼື ລາກໝຸດເທິງແຜນທີ່.',
            }
          }
        }

        let pos
        try {
          pos = await Geolocation.getCurrentPosition({
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 20000,
          })
        } catch {
          // Indoor fallback (Wi-Fi / cell tower location)
          pos = await Geolocation.getCurrentPosition({
            enableHighAccuracy: false,
            timeout: 10000,
            maximumAge: 60000,
          })
        }

        return {
          ok: true,
          lat: Number(pos.coords.latitude.toFixed(6)),
          lng: Number(pos.coords.longitude.toFixed(6)),
        }
      } catch {
        return {
          ok: false,
          reason: 'unavailable',
          messageLao:
            'ກະລຸນາເປີດ GPS / Location ໃນໂທລະສັບຂອງທ່ານ ຫຼື ລາກໝຸດສີຟ້າເທິງແຜນທີ່ໂດຍກົງ.',
        }
      }
    }

    // 2. Web Browser on an Insecure LAN IP (e.g. http://10.227.50.251:3000)
    //    Browsers block navigator.geolocation unless protocol is https: or host is localhost/127.0.0.1.
    if (!window.isSecureContext) {
      gpsSecureDialogOpen.value = true
      return {
        ok: false,
        reason: 'insecure_origin',
        messageLao:
          'ບຣາວເຊີຕ້ອງການ HTTPS ຫຼື localhost ເພື່ອເປີດ GPS — ກະລຸນາເລືອກວິທີເປີດໃນກ່ອງແນະນຳ.',
      }
    }

    if (!navigator.geolocation) {
      return {
        ok: false,
        reason: 'unsupported',
        messageLao:
          'ບຣາວເຊີນີ້ບໍ່ຮອງຮັບ GPS — ທ່ານສາມາດລາກໝຸດສີຟ້າ ຫຼື ແຕະເທິງແຜນທີ່ເພື່ອເລືອກຕຳແໜ່ງໄດ້ທັນທີ.',
      }
    }

    // 3. Web Browser on a Secure Origin (https://... or http://localhost:3000)
    try {
      let pos: GeolocationPosition
      try {
        pos = await browserPositionOnce({
          enableHighAccuracy: true,
          timeout: 8000,
          maximumAge: 20000,
        })
      } catch (firstErr: any) {
        // Retry once with network/Wi-Fi accuracy if high-accuracy satellite lock timed out indoors
        if (firstErr?.code === 2 || firstErr?.code === 3) {
          pos = await browserPositionOnce({
            enableHighAccuracy: false,
            timeout: 10000,
            maximumAge: 60000,
          })
        } else {
          throw firstErr
        }
      }

      return {
        ok: true,
        lat: Number(pos.coords.latitude.toFixed(6)),
        lng: Number(pos.coords.longitude.toFixed(6)),
      }
    } catch (err: any) {
      const rawMsg = String(err?.message || '').toLowerCase()
      if (rawMsg.includes('secure origin') || !window.isSecureContext) {
        gpsSecureDialogOpen.value = true
        return {
          ok: false,
          reason: 'insecure_origin',
        }
      }

      if (err?.code === 1) {
        return {
          ok: false,
          reason: 'permission_denied',
          messageLao:
            'ບຣາວເຊີຖືກປິດສິດ Location — ກະລຸນາກົດໄອຄອນ 🔒 ຂ້າງແຖບ URL ເພື່ອອະນຸຍາດ Location ຫຼື ລາກໝຸດສີຟ້າເທິງແຜນທີ່.',
        }
      }

      return {
        ok: false,
        reason: 'unavailable',
        messageLao:
          'ອຸປະກອນຍັງບໍ່ສາມາດຈັບສັນຍານ GPS ໄດ້ (ກະລຸນາກວດວ່າເປີດ Location ໃນເຄື່ອງແລ້ວ) — ຫຼື ລາກໝຸດສີຟ້າເທິງແຜນທີ່ແທນ.',
      }
    }
  }

  return {
    gpsSecureDialogOpen,
    requestMapPinPickCount,
    buildSecureHttpsUrl,
    buildLocalhostUrl,
    triggerManualMapPick,
    getCurrentCoordinates,
  }
}

