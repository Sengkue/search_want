<template>
  <div class="position-relative w-100 h-100" :style="{ minHeight: height }">
    <div ref="mapContainer" class="sw-map-container" :style="{ height: height }" />

    <!-- Floating Map Overlay Legend / Helper -->
    <div
      class="position-absolute d-flex flex-wrap ga-1 align-center"
      style="top: 8px; right: 8px; z-index: 500; pointer-events: auto"
    >
      <v-chip
        v-if="mode === 'picker'"
        color="error"
        variant="elevated"
        size="x-small"
        prepend-icon="mdi-gesture-tap"
        class="font-weight-bold"
      >
        ແຕະແຜນທີ່ ຫຼື ລາກໝຸດ
      </v-chip>

      <v-btn
        v-if="mode === 'discover'"
        :color="pickingUserPin ? 'warning' : 'surface'"
        size="x-small"
        rounded="pill"
        elevation="2"
        :prepend-icon="pickingUserPin ? 'mdi-crosshairs-gps' : 'mdi-map-marker-account'"
        @click="pickingUserPin = !pickingUserPin"
      >
        {{ pickingUserPin ? 'ແຕະແຜນທີ່ເພື່ອຍ້າຍໝຸດ' : 'ຍ້າຍໝຸດຂອງຂ້ອຍ' }}
      </v-btn>

      <v-btn
        v-if="mode === 'discover'"
        color="surface"
        size="x-small"
        elevation="2"
        icon="mdi-crosshairs"
        title="ກັບໄປຕຳແໜ່ງຂອງຂ້ອຍ"
        @click="recenterOnUser"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import 'leaflet/dist/leaflet.css'
import type { ShopOut } from '~/types/api'

const props = withDefaults(
  defineProps<{
    mode?: 'discover' | 'picker' | 'preview'
    userLat?: number
    userLng?: number
    radiusKm?: number | null
    shops?: ShopOut[]
    selectedShopId?: number | null
    pickerLat?: number
    pickerLng?: number
    height?: string
  }>(),
  {
    mode: 'discover',
    userLat: 17.9757,
    userLng: 102.6331,
    radiusKm: 15,
    shops: () => [],
    selectedShopId: null,
    pickerLat: 17.9757,
    pickerLng: 102.6331,
    height: '100%',
  },
)

const emit = defineEmits<{
  (e: 'select-shop', shopId: number): void
  (e: 'update:userLocation', coords: { lat: number; lng: number }): void
  (e: 'update:pickerLocation', coords: { lat: number; lng: number }): void
}>()

const mapContainer = ref<HTMLElement | null>(null)
const pickingUserPin = ref(false)
const { requestMapPinPickCount } = useGps()

watch(requestMapPinPickCount, () => {
  if (props.mode === 'discover') {
    pickingUserPin.value = true
  }
})

let L: typeof import('leaflet') | null = null
let map: import('leaflet').Map | null = null
let userMarker: import('leaflet').Marker | null = null
let radiusCircle: import('leaflet').Circle | null = null
let pickerMarker: import('leaflet').Marker | null = null
let shopLayerGroup: import('leaflet').LayerGroup | null = null
const shopMarkersMap = new Map<number, import('leaflet').Marker>()
let resizeObserver: ResizeObserver | null = null
let initializingMap = false
let hasFittedInitialShops = false

function escapeHtml(raw: string): string {
  return raw
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function buildUserIcon() {
  if (!L) return undefined
  return L.divIcon({
    className: 'sw-pin-wrapper',
    html: '<div class="sw-user-pulse" title="ຕຳແໜ່ງຂອງທ່ານ"></div>',
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  })
}

function buildShopIcon(shop: ShopOut, isSelected: boolean) {
  if (!L) return undefined
  const bg = shop.category_color || '#1565C0'
  const iconName = shop.category_icon || 'mdi-store-marker'
  const selClass = isSelected ? 'is-selected' : ''
  return L.divIcon({
    className: 'sw-pin-wrapper',
    html: `<div class="sw-shop-marker ${selClass}" style="background:${bg}"><i class="mdi ${iconName}"></i></div>`,
    iconSize: [38, 38],
    iconAnchor: [19, 38],
    popupAnchor: [0, -36],
  })
}

function buildPickerIcon() {
  if (!L) return undefined
  return L.divIcon({
    className: 'sw-pin-wrapper',
    html: '<div class="sw-picker-marker"><i class="mdi mdi-store-plus"></i></div>',
    iconSize: [44, 44],
    iconAnchor: [22, 44],
  })
}

function renderUserAndRadius() {
  if (!L || !map || props.mode !== 'discover') return

  const latlng: [number, number] = [props.userLat, props.userLng]
  if (!userMarker) {
    userMarker = L.marker(latlng, {
      icon: buildUserIcon(),
      draggable: true,
      zIndexOffset: 900,
    })
      .addTo(map)
      .bindPopup(
        '<strong>ຕຳແໜ່ງປັດຈຸບັນຂອງທ່ານ</strong><br/><span style="font-size:11px;color:#64748b">ລາກໝຸດສີຟ້ານີ້ເພື່ອປ່ຽນຕຳແໜ່ງໄດ້ທັນທີ</span>',
      )

    userMarker.on('dragend', () => {
      if (!userMarker) return
      const pos = userMarker.getLatLng()
      emit('update:userLocation', {
        lat: Number(pos.lat.toFixed(6)),
        lng: Number(pos.lng.toFixed(6)),
      })
    })
  } else {
    userMarker.setLatLng(latlng)
  }

  if (radiusCircle) {
    map.removeLayer(radiusCircle)
    radiusCircle = null
  }
  if (props.radiusKm && props.radiusKm > 0 && props.radiusKm <= 200) {
    radiusCircle = L.circle(latlng, {
      radius: props.radiusKm * 1000,
      color: '#1565C0',
      weight: 1.5,
      dashArray: '6, 6',
      fillColor: '#1E88E5',
      fillOpacity: 0.07,
    }).addTo(map)
  }
}

function renderShopMarkers(fitBounds = false) {
  if (!L || !map || props.mode !== 'discover' || !shopLayerGroup) return
  shopLayerGroup.clearLayers()
  shopMarkersMap.clear()

  const boundsPoints: [number, number][] = [[props.userLat, props.userLng]]

  for (const shop of props.shops) {
    const isSel = shop.id === props.selectedShopId
    const marker = L.marker([shop.latitude, shop.longitude], {
      icon: buildShopIcon(shop, isSel),
      zIndexOffset: isSel ? 700 : 200,
    })

    const distBadge =
      shop.distance_km !== null && shop.distance_km !== undefined
        ? `<span style="background:#E3F2FD;color:#1565C0;padding:2px 8px;border-radius:12px;font-weight:700;font-size:12px;">ຫ່າງ ${shop.distance_km} ກມ.</span>`
        : ''

    const gmapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${shop.latitude},${shop.longitude}`

    marker.bindPopup(`
      <div style="min-width:210px;font-family:var(--sw-font-lao);line-height:1.55;">
        <div style="font-weight:700;font-size:14px;margin-bottom:4px;">${escapeHtml(shop.name)}</div>
        <div style="font-size:12px;color:#546E7A;margin-bottom:6px;">
          ${escapeHtml(shop.category_name)} ${distBadge}
        </div>
        <div style="font-size:12px;color:#37474F;margin-bottom:8px;">
          📍 ${escapeHtml(shop.address)}<br/>
          🕒 ${escapeHtml(shop.opening_hours)}
        </div>
        <div style="display:flex;gap:8px;">
          <a href="${gmapsUrl}" target="_blank" rel="noopener"
             style="background:#1565C0;color:#fff;text-decoration:none;padding:5px 10px;border-radius:6px;font-size:12px;font-weight:600;">
            ນຳທາງ
          </a>
          <a href="tel:${escapeHtml(shop.phone)}"
             style="background:#2E7D32;color:#fff;text-decoration:none;padding:5px 10px;border-radius:6px;font-size:12px;font-weight:600;">
            ໂທ
          </a>
        </div>
      </div>
    `)

    marker.on('click', () => {
      emit('select-shop', shop.id)
    })

    shopLayerGroup.addLayer(marker)
    shopMarkersMap.set(shop.id, marker)
    boundsPoints.push([shop.latitude, shop.longitude])
  }

  if (fitBounds && boundsPoints.length > 1) {
    const b = L.latLngBounds(boundsPoints)
    map.fitBounds(b, { padding: [45, 45], maxZoom: 15 })
  }
}

function renderPickerOrPreview() {
  if (!L || !map || props.mode === 'discover') return
  const coords: [number, number] = [props.pickerLat, props.pickerLng]
  const draggable = props.mode === 'picker'

  if (!pickerMarker) {
    pickerMarker = L.marker(coords, {
      icon: buildPickerIcon(),
      draggable,
    }).addTo(map)

    if (draggable) {
      pickerMarker.on('dragend', () => {
        if (!pickerMarker) return
        const pos = pickerMarker.getLatLng()
        emit('update:pickerLocation', {
          lat: Number(pos.lat.toFixed(6)),
          lng: Number(pos.lng.toFixed(6)),
        })
      })
    }
  } else {
    pickerMarker.setLatLng(coords)
  }
}

function recenterOnUser() {
  if (!map) return
  map.flyTo([props.userLat, props.userLng], 14, { duration: 0.6 })
}

async function initMap(container: HTMLElement) {
  if (map || initializingMap) return
  initializingMap = true
  try {
    const leafletModule = await import('leaflet')
    L = (leafletModule as any).default || leafletModule

    const targetEl = mapContainer.value || container
    if (!L || !targetEl || !targetEl.isConnected) return

    const initCenter: [number, number] =
      props.mode === 'discover'
        ? [props.userLat, props.userLng]
        : [props.pickerLat, props.pickerLng]

    map = L.map(targetEl, {
      center: initCenter,
      zoom: props.mode === 'preview' ? 15 : 13,
      zoomControl: true,
    })

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 19,
    }).addTo(map)

    shopLayerGroup = L.layerGroup().addTo(map)

    map.on('click', (e: import('leaflet').LeafletMouseEvent) => {
      if (props.mode === 'picker') {
        const coords = {
          lat: Number(e.latlng.lat.toFixed(6)),
          lng: Number(e.latlng.lng.toFixed(6)),
        }
        pickerMarker?.setLatLng([coords.lat, coords.lng])
        emit('update:pickerLocation', coords)
      } else if (props.mode === 'discover' && pickingUserPin.value) {
        pickingUserPin.value = false
        emit('update:userLocation', {
          lat: Number(e.latlng.lat.toFixed(6)),
          lng: Number(e.latlng.lng.toFixed(6)),
        })
      }
    })

    if (props.mode === 'discover') {
      renderUserAndRadius()
      if (props.shops.length > 0) {
        hasFittedInitialShops = true
      }
      renderShopMarkers(true)
    } else {
      renderPickerOrPreview()
    }

    resizeObserver = new ResizeObserver(() => {
      map?.invalidateSize()
    })
    resizeObserver.observe(targetEl)
  } finally {
    initializingMap = false
  }
}

watch(
  mapContainer,
  (el) => {
    if (el && !map) {
      void initMap(el)
    }
  },
  { immediate: true, flush: 'post' },
)

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  map?.remove()
  map = null
  userMarker = null
  radiusCircle = null
  pickerMarker = null
  shopLayerGroup = null
  shopMarkersMap.clear()
  initializingMap = false
  hasFittedInitialShops = false
})

watch(
  () => [props.userLat, props.userLng, props.radiusKm],
  ([newLat, newLng], [oldLat, oldLng]) => {
    if (!map || props.mode !== 'discover') return
    renderUserAndRadius()
    if (newLat !== oldLat || newLng !== oldLng) {
      map.flyTo([Number(newLat), Number(newLng)], 13, { duration: 0.6 })
    }
  },
)

watch(
  () => props.shops,
  (newShops) => {
    if (!map || props.mode !== 'discover') return
    const shouldFit = !hasFittedInitialShops && newShops.length > 0
    if (shouldFit) {
      hasFittedInitialShops = true
    }
    renderShopMarkers(shouldFit)
  },
  { deep: true },
)

watch(
  () => props.selectedShopId,
  (newId) => {
    if (!map || props.mode !== 'discover') return
    renderShopMarkers(false)
    if (newId) {
      const shop = props.shops.find((s) => s.id === newId)
      const marker = shopMarkersMap.get(newId)
      if (shop) {
        map.flyTo([shop.latitude, shop.longitude], Math.max(map.getZoom(), 14), {
          duration: 0.5,
        })
      }
      marker?.openPopup()
    }
  },
)

watch(
  () => [props.pickerLat, props.pickerLng],
  ([lat, lng]) => {
    if (!map || props.mode === 'discover') return
    renderPickerOrPreview()
    map.panTo([Number(lat), Number(lng)])
  },
)
</script>

