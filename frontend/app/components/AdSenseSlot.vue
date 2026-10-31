<template>
  <div
    v-if="shouldDisplay"
    class="sw-adsense-outer"
    data-testid="adsense-slot"
    :data-placement="placement"
    :data-ad-status="liveAdStatus"
  >
    <!-- 1. REAL GOOGLE ADSENSE <ins class="adsbygoogle"> TAG (Always mounted when Client + Slot ID exist) -->
    <div
      v-if="canMountRealGoogleTag"
      class="sw-adsense-live-wrap"
      :class="{ 'sw-adsense-live-hidden': liveAdStatus !== 'filled' && showRichVisualAd }"
    >
      <div v-if="liveAdStatus === 'filled'" class="d-flex align-center justify-space-between px-2 pt-1">
        <span class="text-body-small text-medium-emphasis" style="font-size: 10px">
          ໂຄສະນາ • Google AdSense
        </span>
      </div>
      <ins
        ref="insEl"
        class="adsbygoogle"
        style="display: block; width: 100%"
        :style="{ minHeight: liveAdStatus === 'filled' ? '90px' : '0px' }"
        :data-ad-client="effectiveClientId"
        :data-ad-slot="slotId"
        data-ad-format="auto"
        data-full-width-responsive="true"
        :data-adtest="adsenseConfig.test_mode ? 'on' : undefined"
      />
    </div>

    <!-- 2. RICH VISUAL GOOGLE DISPLAY AD UNIT (Shown when Test/Preview Mode is ON and Google returns unfilled on localhost/LAN) -->
    <v-card
      v-if="liveAdStatus !== 'filled' && showRichVisualAd && !dismissedByUser"
      elevation="0"
      rounded="xl"
      class="sw-visual-ad-card overflow-hidden"
      :class="[
        placement === 'banner' ? 'sw-visual-ad-banner' : 'sw-visual-ad-infeed',
        isDark ? 'sw-visual-ad-dark' : 'sw-visual-ad-light',
      ]"
    >
      <!-- Top Google AdChoices & Status Bar -->
      <div class="sw-adchoices-bar d-flex align-center justify-space-between px-3 py-1">
        <div class="d-flex align-center ga-1 flex-wrap">
          <span class="sw-google-ad-pill">Ad • ໂຄສະນາ</span>
          <span class="text-body-small font-weight-bold" style="font-size: 11px; color: #0284c7">
            Google AdSense
          </span>
          <span
            v-if="hasValidClientId"
            class="text-body-small text-medium-emphasis d-none d-sm-inline"
            style="font-size: 10.5px"
          >
            ({{ effectiveClientId }}<template v-if="slotId"> • Slot {{ slotId }}</template>)
          </span>
        </div>

        <div class="d-flex align-center ga-1">
          <NuxtLink
            v-if="authStore.isAdmin"
            to="/admin/approvals?tab=ADSENSE"
            class="text-decoration-none sw-adchoices-link mr-1"
            title="ຕັ້ງຄ່າ Google AdSense"
          >
            ⚙ ຕັ້ງຄ່າ
          </NuxtLink>

          <!-- Google AdChoices [i] Info Tooltip -->
          <v-menu location="bottom end" max-width="320">
            <template #activator="{ props: infoProps }">
              <button
                v-bind="infoProps"
                type="button"
                class="sw-adchoices-icon-btn"
                title="ຂໍ້ມູນໂຄສະນາ Google AdSense"
              >
                <v-icon icon="mdi-information-outline" size="13" />
              </button>
            </template>
            <v-card class="pa-3 text-body-small" rounded="lg">
              <div class="font-weight-bold text-primary mb-1">
                ✅ Google AdSense ເຊື່ອມຕໍ່ສຳເລັດແລ້ວ!
              </div>
              <div class="text-medium-emphasis mb-1">
                ລະຫັດບັນຊີ: <code>{{ effectiveClientId || 'ຍັງບໍ່ໄດ້ໃສ່' }}</code>
                <span v-if="slotId"><br>Ad Slot: <code>{{ slotId }}</code></span>
              </div>
              <div class="text-medium-emphasis" style="font-size: 11.5px">
                <strong>ເປັນຫຍັງຕອນນີ້ຈຶ່ງເຫັນໂຄສະນາຈຳລອງ?</strong><br>
                Google ຈະສົ່ງໂຄສະນາລູກຄ້າຈິງສະເພາະເທິງໂດເມນອອນລາຍ (ເຊັ່ນ <code>.com</code> / <code>.la</code>) ທີ່ຜ່ານການກວດອະນຸມັດແລ້ວເທົ່ານັ້ນ (ບໍ່ສົ່ງເທິງ <code>localhost</code> ຫຼື IP <code>10.x.x.x</code>). ເມື່ອເວັບອອນລາຍເທິງໂດເມນຈິງ ໂຄສະນາຈິງຈາກ Google ຈະສະແດງແທນອັດຕະໂນມັດທັນທີ!
              </div>
            </v-card>
          </v-menu>

          <button
            type="button"
            class="sw-adchoices-icon-btn"
            title="ປິດໂຄສະນານີ້ຊົ່ວຄາວ"
            @click="dismissedByUser = true"
          >
            <v-icon icon="mdi-close" size="13" />
          </button>
        </div>
      </div>

      <!-- Rich Visual Display Ad Body (Looks & feels like an authentic Google Display Ad creative) -->
      <div
        class="d-flex flex-column flex-sm-row align-stretch"
        :class="placement === 'banner' ? 'sw-banner-body' : 'sw-infeed-body'"
      >
        <!-- Left / Top Vibrant Visual Artwork Banner -->
        <div
          class="sw-ad-visual-panel d-flex flex-column align-center justify-center text-white pa-3 position-relative"
          :style="{ background: activeAd.gradient }"
        >
          <span class="sw-ad-promo-tag">{{ activeAd.promoTag }}</span>
          <v-avatar size="46" color="rgba(255,255,255,0.2)" class="mb-1 sw-ad-visual-icon">
            <v-icon :icon="activeAd.icon" size="26" color="white" />
          </v-avatar>
          <div class="font-weight-black text-center" style="font-size: 12px; line-height: 1.2">
            {{ activeAd.visualTitle }}
          </div>
        </div>

        <!-- Right / Bottom Advertiser Copy & CTA Button -->
        <div class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between ga-2 pa-3 flex-grow-1">
          <div style="min-width: 0; flex: 1">
            <div class="d-flex align-center ga-2 mb-1">
              <span class="text-body-small font-weight-bold text-uppercase" :style="{ color: activeAd.accentColor, fontSize: '10.5px', letterSpacing: '0.03em' }">
                {{ activeAd.advertiser }}
              </span>
              <span class="text-body-small text-medium-emphasis" style="font-size: 10.5px">
                • {{ activeAd.domain }}
              </span>
            </div>

            <div class="text-title-small font-weight-black mb-1" style="line-height: 1.3">
              {{ activeAd.headline }}
            </div>

            <div class="text-body-small text-medium-emphasis sw-clamp-2" style="line-height: 1.4">
              {{ activeAd.description }}
            </div>
          </div>

          <div class="d-flex align-center justify-space-between w-100 w-sm-auto ga-2 mt-1 mt-sm-0">
            <!-- Rotating Ad Carousel Dots -->
            <div class="d-flex align-center ga-1 mr-1">
              <button
                v-for="(_, dotIdx) in richAds"
                :key="dotIdx"
                type="button"
                class="sw-ad-dot"
                :class="{ 'is-active': dotIdx === currentAdIdx }"
                :aria-label="`ໂຄສະນາ ${dotIdx + 1}`"
                @click="currentAdIdx = dotIdx"
              />
            </div>

            <v-btn
              :color="activeAd.btnColor"
              variant="flat"
              size="small"
              rounded="pill"
              append-icon="mdi-chevron-right"
              class="font-weight-bold px-4 flex-shrink-0 text-white"
              @click="cycleNextAd"
            >
              {{ activeAd.cta }}
            </v-btn>
          </div>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { useTheme } from 'vuetify'
import { useAuthStore } from '~/stores/auth'

const props = withDefaults(
  defineProps<{
    placement: 'infeed' | 'banner'
    variantIndex?: number
  }>(),
  {
    variantIndex: 0,
  },
)

const authStore = useAuthStore()
const theme = useTheme()
const isDark = computed(() => theme.global.current.value.dark)

const {
  adsenseConfig,
  effectiveClientId,
  effectiveSlotInfeed,
  effectiveSlotBanner,
  hasValidClientId,
  isAdAllowedOnRoute,
} = useAdSense()

const insEl = ref<HTMLElement | null>(null)
const pushedKey = ref('')
const liveAdStatus = ref<'idle' | 'filled' | 'unfilled'>('idle')
const dismissedByUser = ref(false)
let statusObserver: MutationObserver | null = null
let rotateTimer: ReturnType<typeof setInterval> | null = null

const slotId = computed(() =>
  props.placement === 'infeed' ? effectiveSlotInfeed.value : effectiveSlotBanner.value,
)

const canMountRealGoogleTag = computed(() => hasValidClientId.value && Boolean(slotId.value))

/**
 * Show rich visual display ad whenever Test/Preview Mode is ON and Google hasn't filled
 * a live paid creative (e.g. on localhost / LAN IP 10.227.50.251 or while awaiting domain review).
 */
const showRichVisualAd = computed(() => adsenseConfig.value.test_mode)

const shouldDisplay = computed(() => {
  if (!import.meta.client) return false
  if (!adsenseConfig.value.enabled) return false
  if (!isAdAllowedOnRoute.value) return false
  return canMountRealGoogleTag.value || showRichVisualAd.value
})

const richAds = [
  {
    advertiser: 'Lao SuperNet 5G',
    domain: 'supernet5g.la',
    promoTag: 'PROMO 5G',
    visualTitle: '5G ໄວສຸດ ບໍ່ຈຳກັດ',
    icon: 'mdi-access-point-network',
    gradient: 'linear-gradient(135deg, #1D4ED8 0%, #0EA5E9 100%)',
    accentColor: '#0284C7',
    btnColor: 'primary',
    headline: 'ແພັກເກັດເນັດມືຖື 5G ຄວາມໄວສູງ — ຫຼິ້ນເນັດ & ນຳທາງ GPS ບໍ່ສະດຸດ!',
    description: 'ສະໝັກມື້ນີ້ຮັບດາຕ້າໂບນັດຟຣີ 20GB ທົ່ວນະຄອນຫຼວງວຽງຈັນ ແລະ ຕ່າງແຂວງ.',
    cta: 'ເບິ່ງແພັກເກັດ',
  },
  {
    advertiser: 'Lao SafeDrive Insurance',
    domain: 'safedrive.la',
    promoTag: '24/7 CARE',
    visualTitle: 'ປະກັນໄພລົດ 24 ຊມ.',
    icon: 'mdi-shield-car',
    gradient: 'linear-gradient(135deg, #059669 0%, #10B981 100%)',
    accentColor: '#059669',
    btnColor: 'success',
    headline: 'ລົດເສຍກາງທາງບໍ່ຕ້ອງກັງວົນ! ປະກັນໄພລົດຍົນ ພ້ອມລົດລາກຟຣີ 24 ຊົ່ວໂມງ',
    description: 'ຄຸ້ມຄອງທຸກອຸບັດຕິເຫດ, ແບັດເຕີຣີ້ໝົດ ແລະ ບໍລິການຊ່ວຍເຫຼືອສຸກເສີນເຖິງທີ່.',
    cta: 'ເຊັກລາຄາຟຣີ',
  },
  {
    advertiser: 'Bolaven Roast Café',
    domain: 'bolavencafe.la',
    promoTag: 'BUY 1 GET 1',
    visualTitle: 'ກາເຟສົດ ປາກຊ່ອງ',
    icon: 'mdi-coffee-outline',
    gradient: 'linear-gradient(135deg, #B45309 0%, #F59E0B 100%)',
    accentColor: '#D97706',
    btnColor: 'warning',
    headline: 'ກາເຟອາຣາບິກ້າແທ້ຈາກພູພຽງບໍລະເວນ — ສັ່ງຜ່ານແອັບ ຊື້ 1 ແຖມ 1!',
    description: 'ຫອມເຂັ້ມ ສົດໃໝ່ທຸກມື້ ພ້ອມບໍລິການສົ່ງດ່ວນພາຍໃນ 25 ນາທີ.',
    cta: 'ສັ່ງເລີຍ',
  },
  {
    advertiser: 'CoolHome Aircon Pro',
    domain: 'coolhome.la',
    promoTag: 'SALE -30%',
    visualTitle: 'ລ້າງແອ & ເຕີມນ້ຳຢາ',
    icon: 'mdi-air-conditioner',
    gradient: 'linear-gradient(135deg, #6D28D9 0%, #3B82F6 100%)',
    accentColor: '#7C3AED',
    btnColor: 'primary',
    headline: 'ໂປຣໂມຊັນລ້າງແອບ້ານ & ຫ້ອງການ ຫຼຸດ 30% — ເຢັນໄວ ປະຢັດໄຟ!',
    description: 'ທີມຊ່າງມືອາຊີບ ຮັບປະກັນວຽກສ້ອມແປງ 90 ວັນ ເອີ້ນໃຊ້ບໍລິການເຖິງບ້ານ.',
    cta: 'ຈອງຄິວຊ່າງ',
  },
]

const initialIdx = (props.placement === 'banner' ? 0 : 1 + props.variantIndex) % richAds.length
const currentAdIdx = ref(initialIdx)

const activeAd = computed(() => richAds[currentAdIdx.value % richAds.length]!)

function cycleNextAd() {
  currentAdIdx.value = (currentAdIdx.value + 1) % richAds.length
}

function observeAdStatus() {
  if (!insEl.value || typeof MutationObserver === 'undefined') return
  statusObserver?.disconnect()
  const checkAttr = () => {
    const status = insEl.value?.getAttribute('data-ad-status')
    if (status === 'filled') {
      liveAdStatus.value = 'filled'
    } else if (status === 'unfilled') {
      liveAdStatus.value = 'unfilled'
    }
  }
  checkAttr()
  statusObserver = new MutationObserver(checkAttr)
  statusObserver.observe(insEl.value, {
    attributes: true,
    attributeFilter: ['data-ad-status'],
  })
}

function tryPushAdSense() {
  if (!import.meta.client || !canMountRealGoogleTag.value || !insEl.value) return
  observeAdStatus()
  const key = `${effectiveClientId.value}:${slotId.value}:${props.placement}`
  if (pushedKey.value === key) return
  try {
    const w = window as any
    w.adsbygoogle = w.adsbygoogle || []
    w.adsbygoogle.push({})
    pushedKey.value = key
  } catch {
    // Ignore duplicate push or local adblocker errors gracefully
  }
}

watch([canMountRealGoogleTag, effectiveClientId, slotId], () => {
  nextTick(() => tryPushAdSense())
})

onMounted(() => {
  nextTick(() => tryPushAdSense())
  rotateTimer = setInterval(() => {
    currentAdIdx.value = (currentAdIdx.value + 1) % richAds.length
  }, 7500)
})

onBeforeUnmount(() => {
  statusObserver?.disconnect()
  if (rotateTimer) clearInterval(rotateTimer)
})
</script>

<style scoped>
.sw-adsense-live-wrap {
  width: 100%;
  overflow: hidden;
  border-radius: 12px;
}

.sw-adsense-live-hidden {
  height: 0 !important;
  min-height: 0 !important;
  overflow: hidden !important;
  opacity: 0;
  pointer-events: none;
}

.sw-visual-ad-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.sw-visual-ad-light {
  background: #ffffff !important;
  border: 1.5px solid rgba(14, 165, 233, 0.35) !important;
  box-shadow: 0 6px 20px rgba(2, 132, 199, 0.08) !important;
}

.sw-visual-ad-dark {
  background: rgba(15, 25, 42, 0.96) !important;
  border: 1.5px solid rgba(56, 189, 248, 0.32) !important;
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.35) !important;
}

.sw-adchoices-bar {
  background: rgba(14, 165, 233, 0.08);
  border-bottom: 1px solid rgba(14, 165, 233, 0.16);
}

.sw-google-ad-pill {
  display: inline-flex;
  align-items: center;
  padding: 1px 7px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 800;
  color: #ffffff;
  background: #0284c7;
  letter-spacing: 0.02em;
}

.sw-adchoices-link {
  font-size: 10.5px;
  font-weight: 700;
  color: #0284c7;
}

.sw-adchoices-icon-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 19px;
  height: 19px;
  border-radius: 4px;
  border: none;
  background: rgba(2, 132, 199, 0.12);
  color: #0284c7;
  cursor: pointer;
  transition: background 0.15s ease;
}

.sw-adchoices-icon-btn:hover {
  background: rgba(2, 132, 199, 0.24);
}

.sw-ad-visual-panel {
  min-width: 142px;
  min-height: 92px;
}

@media (max-width: 599px) {
  .sw-ad-visual-panel {
    width: 100%;
    min-height: 76px;
    flex-direction: row !important;
    justify-content: flex-start !important;
    gap: 10px;
  }
}

.sw-ad-promo-tag {
  font-size: 9px;
  font-weight: 900;
  letter-spacing: 0.06em;
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.25);
  margin-bottom: 4px;
}

.sw-ad-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  border: none;
  padding: 0;
  background: rgba(148, 163, 184, 0.45);
  cursor: pointer;
  transition: all 0.2s ease;
}

.sw-ad-dot.is-active {
  width: 16px;
  border-radius: 999px;
  background: #0284c7;
}
</style>
