<template>
  <v-dialog v-model="internalOpen" max-width="360">
    <v-card rounded="xl" class="sw-hero-card pa-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <div class="d-flex align-center ga-3">
          <BrandLogo :size="46" />
          <div>
            <div class="text-title-small font-weight-black" style="line-height: 1.2">
              ຕິດຕັ້ງແອັບ Search-Want
            </div>
            <div class="text-body-small text-success font-weight-bold">
              ໃຊ້ງານເທິງມືຖືໄດ້ໄວ ແລະ ສະດວກກວ່າ
            </div>
          </div>
        </div>
        <v-btn icon="mdi-close" variant="text" size="x-small" @click="dismissForSession" />
      </div>

      <p class="text-body-small text-medium-emphasis mb-3">
        ດາວໂຫຼດໄຟລ໌ <strong>APK</strong> ເພື່ອຕິດຕັ້ງເປັນແອັບລົງໂທລະສັບ ເປີດແຜນທີ່ ແລະ ຄົ້ນຫາຊ່າງໃກ້ຕົວໄດ້ທັນທີ.
      </p>

      <!-- Android Direct APK Download CTA -->
      <v-btn
        v-if="!isIos"
        :href="apkDownloadUrl"
        download="Search-Want.apk"
        color="primary"
        variant="flat"
        block
        prepend-icon="mdi-android"
        class="mb-2"
        :disabled="!apkInfo.available && apkChecked"
        @click="onDownloadApkClick"
      >
        ດາວໂຫຼດ ແລະ ຕິດຕັ້ງ APK
        <span v-if="apkInfo.available && apkInfo.size_mb > 0" class="ml-1 opacity-90">
          ({{ apkInfo.size_mb }} MB)
        </span>
      </v-btn>

      <!-- 1-Tap Native Browser PWA Install -->
      <v-btn
        v-if="deferredPrompt"
        color="secondary"
        variant="tonal"
        size="small"
        block
        prepend-icon="mdi-cellphone-check"
        class="mb-2"
        @click="triggerBrowserPwaInstall"
      >
        ຕິດຕັ້ງດ່ວນຜ່ານບຣາວເຊີ
      </v-btn>

      <!-- Compact Step Helper (Adapts cleanly to Light & Dark themes) -->
      <v-sheet
        v-if="!isIos"
        rounded="lg"
        class="pa-2 px-3 mb-3 border"
        style="background: rgba(26, 115, 232, 0.08)"
      >
        <div class="text-body-small font-weight-bold text-primary mb-1">
          ຂັ້ນຕອນການຕິດຕັ້ງ APK ງ່າຍໆ:
        </div>
        <div class="text-body-small text-high-emphasis" style="line-height: 1.45">
          1. ກົດດາວໂຫຼດ APK &rarr; 2. ເປີດໄຟລ໌ <code>Search-Want.apk</code> &rarr; 3. ກົດ <strong>Install</strong>
        </div>
      </v-sheet>

      <v-sheet
        v-else
        rounded="lg"
        class="pa-2 px-3 mb-3 border"
        style="background: rgba(26, 115, 232, 0.08)"
      >
        <div class="text-body-small font-weight-bold text-primary mb-1">
          ວິທີຕິດຕັ້ງແອັບສຳລັບ iPhone / iPad:
        </div>
        <div class="text-body-small text-high-emphasis" style="line-height: 1.45">
          ກົດປຸ່ມ <strong>Share</strong> ໃນ Safari &rarr; ເລືອກ <strong>Add to Home Screen</strong>
        </div>
      </v-sheet>

      <v-btn
        variant="text"
        color="medium-emphasis"
        block
        size="x-small"
        @click="dismissForSession"
      >
        ໃຊ້ຜ່ານເວັບຕໍ່ໄປກ່ອນ
      </v-btn>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'
import { useAuthStore } from '~/stores/auth'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const { getBaseUrl, isNativeApp, apiFetch } = useApi()
const authStore = useAuthStore()
const { smAndDown } = useDisplay()

const SESSION_DISMISS_KEY = 'sw_apk_dialog_dismissed'

const internalOpen = computed({
  get: () => props.modelValue,
  set: (v: boolean) => emit('update:modelValue', v),
})

const deferredPrompt = ref<any>(null)
const isIos = ref(false)
const apkChecked = ref(false)
const apkInfo = reactive({
  available: true,
  filename: 'Search-Want.apk',
  size_mb: 0,
})

const apkDownloadUrl = computed(() => `${getBaseUrl()}/api/app/apk`)

function isStandaloneMode(): boolean {
  if (!import.meta.client) return false
  return (
    window.matchMedia?.('(display-mode: standalone)').matches ||
    Boolean((window.navigator as any)?.standalone)
  )
}

function isMobilePhone(): boolean {
  if (!import.meta.client) return false
  const ua = navigator.userAgent || ''
  return /Android|iPhone|iPad|iPod|Mobile/i.test(ua) || smAndDown.value
}

async function loadApkInfo() {
  try {
    const info = await apiFetch<{
      available: boolean
      filename: string
      size_mb: number
    }>('/api/app/apk-info')
    apkInfo.available = info.available
    apkInfo.filename = info.filename
    apkInfo.size_mb = info.size_mb
  } catch {
    // Allow fallback click even if metadata request fails
  } finally {
    apkChecked.value = true
  }
}

function onDownloadApkClick() {
  if (import.meta.client) {
    sessionStorage.setItem(SESSION_DISMISS_KEY, '1')
  }
  internalOpen.value = false
  authStore.showToast(
    'ກຳລັງດາວໂຫຼດ Search-Want.apk — ເມື່ອສຳເລັດແລ້ວ ກົດເປີດໄຟລ໌ເພື່ອຕິດຕັ້ງ!',
    'success',
    'mdi-download-circle-outline',
  )
}

async function triggerBrowserPwaInstall() {
  if (!deferredPrompt.value) return
  deferredPrompt.value.prompt()
  const choice = await deferredPrompt.value.userChoice.catch(() => null)
  deferredPrompt.value = null
  if (choice?.outcome === 'accepted') {
    dismissForSession()
    authStore.showToast('ຕິດຕັ້ງແອັບ Search-Want ສຳເລັດແລ້ວ!', 'success', 'mdi-check-decagram')
  }
}

function dismissForSession() {
  if (import.meta.client) {
    sessionStorage.setItem(SESSION_DISMISS_KEY, '1')
  }
  internalOpen.value = false
}

onMounted(async () => {
  if (!import.meta.client) return
  if (isNativeApp() || isStandaloneMode()) return

  const ua = navigator.userAgent || ''
  isIos.value = /iPhone|iPad|iPod/i.test(ua) && !/Android/i.test(ua)

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {})
  }

  window.addEventListener('beforeinstallprompt', (e: Event) => {
    e.preventDefault()
    deferredPrompt.value = e
  })

  await loadApkInfo()

  const alreadyDismissed = sessionStorage.getItem(SESSION_DISMISS_KEY) === '1'
  if (!alreadyDismissed && isMobilePhone()) {
    setTimeout(() => {
      if (
        !isNativeApp() &&
        !isStandaloneMode() &&
        sessionStorage.getItem(SESSION_DISMISS_KEY) !== '1'
      ) {
        internalOpen.value = true
      }
    }, 650)
  }
})
</script>
