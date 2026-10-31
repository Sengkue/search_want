import { defineStore } from 'pinia'
import type {
  CategoryOut,
  NearbySearchResponse,
  ProblemKeywordOut,
  ShopOut,
  ShopPayload,
} from '~/types/api'
import { useAuthStore } from '~/stores/auth'

export const useShopsStore = defineStore('shops', () => {
  const { apiFetch } = useApi()
  const { getCurrentCoordinates } = useGps()
  const authStore = useAuthStore()

  const categories = ref<CategoryOut[]>([])
  const symptoms = ref<ProblemKeywordOut[]>([])

  // Default to seeded demo center so first load immediately displays live pins & distances
  const userLat = ref<number>(17.9757)
  const userLng = ref<number>(102.6331)
  const hasLiveGps = ref<boolean>(false)
  const locationLabel = ref<string>('ໃຈກາງນະຄອນຫຼວງວຽງຈັນ')
  const locatingGps = ref<boolean>(false)

  const problemQuery = ref<string>('')
  const selectedCategoryId = ref<number | null>(null)
  const radiusKm = ref<number | null>(15)
  const emergencyOnly = ref<boolean>(false)

  const nearbyData = ref<NearbySearchResponse | null>(null)
  const loadingNearby = ref<boolean>(false)
  const selectedShopId = ref<number | null>(null)

  const myShops = ref<ShopOut[]>([])
  const loadingMyShops = ref<boolean>(false)

  async function loadCategoriesAndSymptoms() {
    const [cats, symp] = await Promise.all([
      apiFetch<CategoryOut[]>('/api/categories'),
      apiFetch<ProblemKeywordOut[]>('/api/categories/symptoms'),
    ])
    categories.value = cats
    symptoms.value = symp
  }

  async function searchNearby(announce = false) {
    loadingNearby.value = true
    try {
      const res = await apiFetch<NearbySearchResponse>('/api/shops/nearby', {
        params: {
          problem: problemQuery.value.trim() || undefined,
          lat: userLat.value,
          lng: userLng.value,
          radius_km: radiusKm.value ?? 0,
          category_id: selectedCategoryId.value ?? undefined,
          emergency_only: emergencyOnly.value ? 'true' : undefined,
        },
      })
      nearbyData.value = res

      if (res.shops.length > 0) {
        if (!res.shops.some((s) => s.id === selectedShopId.value)) {
          selectedShopId.value = res.shops[0].id
        }
      } else {
        selectedShopId.value = null
      }

      if (announce && res.diagnosis.notification_summary) {
        const toastColor = res.total_found > 0 ? 'success' : 'warning'
        const toastIcon = res.total_found > 0 ? 'mdi-map-marker-Bell' : 'mdi-map-search-outline'
        authStore.showToast(
          res.diagnosis.notification_summary,
          toastColor,
          toastIcon === 'mdi-map-marker-Bell' ? 'mdi-bell-ring' : toastIcon,
        )
        if (res.total_found > 0) {
          authStore.triggerBrowserNotification(
            'ພົບຮ້ານໃກ້ຄຽງ — Search-Want',
            res.diagnosis.notification_summary,
          )
        }
      }
    } catch (err: any) {
      authStore.showToast(
        err?.data?.detail || 'ບໍ່ສາມາດເຊື່ອມຕໍ່ເຊີບເວີໄດ້. ກະລຸນາກວດວ່າ Python backend ເປີດຢູ່ທີ່ພອດ 8000.',
        'error',
        'mdi-alert-circle-outline',
      )
    } finally {
      loadingNearby.value = false
    }
  }

  async function detectBrowserGps(announce = true): Promise<boolean> {
    locatingGps.value = true
    try {
      const res = await getCurrentCoordinates()
      if (res.ok && res.lat !== undefined && res.lng !== undefined) {
        userLat.value = res.lat
        userLng.value = res.lng
        hasLiveGps.value = true
        locationLabel.value = `GPS ປັດຈຸບັນ (${userLat.value.toFixed(4)}, ${userLng.value.toFixed(4)})`
        await searchNearby(announce)
        return true
      }

      // Note: if reason === 'insecure_origin', useGps() automatically opens GpsSecureOriginDialog
      if (res.reason !== 'insecure_origin' && res.messageLao) {
        authStore.showToast(res.messageLao, 'warning', 'mdi-map-marker-alert-outline')
      }
      return false
    } finally {
      locatingGps.value = false
    }
  }

  async function setManualUserLocation(lat: number, lng: number, label = 'ໝຸດທີ່ເລືອກເທິງແຜນທີ່') {
    userLat.value = Number(lat.toFixed(6))
    userLng.value = Number(lng.toFixed(6))
    hasLiveGps.value = true
    locationLabel.value = `${label} (${userLat.value.toFixed(4)}, ${userLng.value.toFixed(4)})`
    await searchNearby(true)
  }

  async function seedDemoShopsNearCurrentLocation() {
    try {
      const resp = await apiFetch<{ created_count: number; message: string }>(
        '/api/shops/seed-nearby',
        {
          method: 'POST',
          body: {
            latitude: userLat.value,
            longitude: userLng.value,
            area_name: 'ບໍລິເວນຂອງທ່ານ',
          },
        },
      )
      authStore.showToast(resp.message, 'success', 'mdi-store-plus')
      await loadCategoriesAndSymptoms()
      await searchNearby(true)
    } catch (err: any) {
      authStore.showToast(
        err?.data?.detail || 'ສ້າງຮ້ານທົດລອງບໍ່ສຳເລັດ.',
        'error',
        'mdi-alert-circle',
      )
    }
  }

  async function submitShop(payload: ShopPayload): Promise<ShopOut> {
    const created = await apiFetch<ShopOut>('/api/shops', {
      method: 'POST',
      body: payload,
    })
    await authStore.refreshMe()
    await authStore.fetchNotifications()
    return created
  }

  async function updateShop(shopId: number, payload: ShopPayload): Promise<ShopOut> {
    const updated = await apiFetch<ShopOut>(`/api/shops/${shopId}`, {
      method: 'PUT',
      body: payload,
    })
    await authStore.fetchNotifications()
    return updated
  }

  async function fetchMyShops() {
    loadingMyShops.value = true
    try {
      myShops.value = await apiFetch<ShopOut[]>('/api/shops/mine')
    } finally {
      loadingMyShops.value = false
    }
  }

  return {
    categories,
    symptoms,
    userLat,
    userLng,
    hasLiveGps,
    locationLabel,
    locatingGps,
    problemQuery,
    selectedCategoryId,
    radiusKm,
    emergencyOnly,
    nearbyData,
    loadingNearby,
    selectedShopId,
    myShops,
    loadingMyShops,
    loadCategoriesAndSymptoms,
    searchNearby,
    detectBrowserGps,
    setManualUserLocation,
    seedDemoShopsNearCurrentLocation,
    submitShop,
    updateShop,
    fetchMyShops,
  }
})

