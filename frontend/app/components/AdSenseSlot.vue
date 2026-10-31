<template>
  <div
    v-if="shouldDisplay"
    class="sw-adsense-outer"
    data-testid="adsense-slot"
    :data-placement="placement"
    :data-ad-status="liveAdStatus"
  >
    <!-- 1. REAL GOOGLE ADSENSE <ins class="adsbygoogle"> TAG (Always mounted & pushed when Client + Slot ID exist) -->
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

    <!-- 2. DIVERSE GOOGLE DISPLAY NETWORK VISUAL FORMATS (3 Distinct Layouts + 8 Contextual Advertisers) -->
    <v-card
      v-if="liveAdStatus !== 'filled' && showRichVisualAd && !dismissedByUser"
      elevation="0"
      rounded="xl"
      class="sw-gdn-card overflow-hidden position-relative"
      :class="[isDark ? 'sw-gdn-dark' : 'sw-gdn-light']"
    >
      <!-- Tiny Authentic Top-Right Google AdChoices Corner Overlay ([Ad] [i] [x]) -->
      <div class="sw-gdn-corner d-flex align-center">
        <span class="sw-gdn-corner-label">ໂຄສະນາ • AdSense</span>

        <NuxtLink
          v-if="authStore.isAdmin"
          to="/admin/approvals?tab=ADSENSE"
          class="sw-gdn-corner-btn text-decoration-none"
          title="ຕັ້ງຄ່າ Google AdSense"
        >
          ⚙
        </NuxtLink>

        <v-menu location="bottom end" max-width="320">
          <template #activator="{ props: infoProps }">
            <button
              v-bind="infoProps"
              type="button"
              class="sw-gdn-corner-btn"
              title="ຂໍ້ມູນ Google AdSense"
            >
              <svg width="11" height="11" viewBox="0 0 15 15" fill="none">
                <path d="M7.5 1.5a6 6 0 100 12 6 6 0 000-12zm0 2.4a.85.85 0 110 1.7.85.85 0 010-1.7zm1 7.1h-2V9.9h.45V7.1H6.5V6h1.55v3.9h.45V11z" fill="#00aecd" />
              </svg>
            </button>
          </template>
          <v-card class="pa-3 text-body-small" rounded="lg">
            <div class="font-weight-bold text-primary mb-1">
              ✅ Google AdSense ເຊື່ອມຕໍ່ແລ້ວ
            </div>
            <div class="text-medium-emphasis mb-1" style="font-size: 11.5px">
              Publisher: <code>{{ effectiveClientId || 'ຍັງບໍ່ໄດ້ໃສ່' }}</code>
              <span v-if="slotId"> • Slot: <code>{{ slotId }}</code></span>
            </div>
            <div class="text-medium-emphasis" style="font-size: 11.5px">
              ຕອນນີ້ເວັບລັນຢູ່ເຄື່ອງພາຍໃນ (<code>localhost</code> / IP Wi-Fi) ຈຶ່ງສະແດງໂຄສະນາຕົວຢ່າງຫຼາຍຮູບແບບຕາມໝວດຄົ້ນຫາ. ເມື່ອອັບເວັບຂຶ້ນໂດເມນ <code>.com</code> / <code>.la</code> ທີ່ Google ອະນຸມັດແລ້ວ ໂຄສະນາຈິງຈາກຜູ້ລົງໂຄສະນາ Google ຈະປ່ຽນແທນອັດຕະໂນມັດ 100%!
            </div>
          </v-card>
        </v-menu>

        <button
          type="button"
          class="sw-gdn-corner-btn"
          title="ປິດໂຄສະນານີ້"
          @click="dismissedByUser = true"
        >
          ✕
        </button>
      </div>

      <!-- ===================================================================== -->
      <!-- FORMAT A: GOOGLE NATIVE PHOTO-TOP CARD (Like Google's Coffee Ad Demo) -->
      <!-- ===================================================================== -->
      <div v-if="cardFormat === 'photo-card'" class="sw-format-photo">
        <!-- Rich 16:9 Illustrated Scene Cover -->
        <div class="sw-photo-cover position-relative overflow-hidden" :style="{ background: activeAd.gradient }">
          <!-- Decorative SVG Scene Graphics -->
          <svg class="sw-scene-svg" viewBox="0 0 420 140" preserveAspectRatio="xMidYMid slice">
            <defs>
              <radialGradient :id="`glow-${uid}`" cx="75%" cy="30%" r="60%">
                <stop offset="0%" stop-color="#ffffff" stop-opacity="0.34" />
                <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
              </radialGradient>
            </defs>
            <rect width="420" height="140" :fill="`url(#glow-${uid})`" />
            <circle cx="345" cy="34" r="56" fill="rgba(255,255,255,0.12)" />
            <circle cx="370" cy="110" r="74" fill="rgba(0,0,0,0.14)" />
            <path d="M0 108 Q110 78 220 104 T420 92 L420 140 L0 140 Z" fill="rgba(255,255,255,0.12)" />
          </svg>

          <div class="position-relative d-flex align-center justify-space-between h-100 px-4 py-3 text-white" style="z-index: 1">
            <div style="max-width: 68%">
              <span class="sw-photo-badge mb-1">{{ activeAd.promoTag }}</span>
              <div class="font-weight-black" style="font-size: 17px; line-height: 1.22; text-shadow: 0 2px 8px rgba(0,0,0,0.25)">
                {{ activeAd.visualTitle }}
              </div>
              <div style="font-size: 11.5px; opacity: 0.92" class="mt-1">
                {{ activeAd.visualSub }}
              </div>
            </div>

            <div class="sw-hero-emblem d-flex align-center justify-center">
              <v-icon :icon="activeAd.icon" size="34" color="white" />
            </div>
          </div>
        </div>

        <!-- Clean Editorial Copy + Round '>' Action Circle (Authentic Google AdSense Card Style) -->
        <div class="pa-3 d-flex align-center justify-space-between ga-3">
          <div style="min-width: 0; flex: 1">
            <div class="text-title-small font-weight-black mb-1" style="line-height: 1.3">
              {{ activeAd.headline }}
            </div>
            <div class="text-body-small text-medium-emphasis sw-clamp-2 mb-1" style="line-height: 1.38">
              {{ activeAd.description }}
            </div>
            <div class="text-body-small text-medium-emphasis font-weight-medium" style="font-size: 11px">
              {{ activeAd.advertiser }} • <span style="opacity: 0.8">{{ activeAd.domain }}</span>
            </div>
          </div>

          <button
            type="button"
            class="sw-round-arrow-btn flex-shrink-0"
            :style="{ background: activeAd.accentColor }"
            :title="activeAd.cta"
            @click="cycleNextAd"
          >
            <v-icon icon="mdi-chevron-right" color="white" size="22" />
          </button>
        </div>
      </div>

      <!-- ========================================================================= -->
      <!-- FORMAT B: GOOGLE PRODUCT / APP SHOWCASE CARD (Icon + 4.9★ Rating + Pill)  -->
      <!-- ========================================================================= -->
      <div v-else-if="cardFormat === 'showcase-card'" class="pa-3 pt-4">
        <div class="d-flex align-start ga-3">
          <!-- Glossy App/Brand Squircle Emblem -->
          <div
            class="sw-brand-squircle d-flex flex-column align-center justify-center text-white flex-shrink-0"
            :style="{ background: activeAd.gradient }"
          >
            <v-icon :icon="activeAd.icon" size="26" color="white" />
            <span style="font-size: 8.5px; font-weight: 900; margin-top: 2px">{{ activeAd.shortBadge }}</span>
          </div>

          <div style="min-width: 0; flex: 1">
            <div class="d-flex flex-wrap align-center ga-1 mb-1">
              <span class="font-weight-black text-title-small" style="line-height: 1.25">
                {{ activeAd.advertiser }}
              </span>
              <span class="sw-rating-chip">
                ★ {{ activeAd.rating }}
              </span>
              <span class="sw-offer-chip" :style="{ color: activeAd.accentColor, borderColor: activeAd.accentColor }">
                {{ activeAd.promoTag }}
              </span>
            </div>

            <div class="text-body-small font-weight-bold mb-1" style="line-height: 1.35">
              {{ activeAd.headline }}
            </div>

            <div class="text-body-small text-medium-emphasis sw-clamp-2" style="line-height: 1.38">
              {{ activeAd.description }}
            </div>
          </div>
        </div>

        <div class="d-flex align-center justify-space-between mt-3 pt-2 border-t">
          <span class="text-body-small text-medium-emphasis" style="font-size: 11px">
            🌐 {{ activeAd.domain }}
          </span>

          <v-btn
            :color="activeAd.btnColor"
            variant="flat"
            size="small"
            rounded="lg"
            class="font-weight-bold px-4 text-white"
            append-icon="mdi-open-in-new"
            @click="cycleNextAd"
          >
            {{ activeAd.cta }}
          </v-btn>
        </div>
      </div>

      <!-- ============================================================================ -->
      <!-- FORMAT C: PANORAMIC LEADERBOARD BILLBOARD (For Top & Bottom Wide Banners)    -->
      <!-- ============================================================================ -->
      <div v-else class="d-flex flex-column flex-sm-row align-stretch">
        <div
          class="sw-leaderboard-art d-flex align-center justify-center text-white px-4 py-3 position-relative overflow-hidden"
          :style="{ background: activeAd.gradient }"
        >
          <div class="d-flex align-center ga-3 position-relative" style="z-index: 1">
            <div class="sw-leaderboard-icon d-flex align-center justify-center">
              <v-icon :icon="activeAd.icon" size="28" color="white" />
            </div>
            <div>
              <div class="sw-photo-badge mb-1">{{ activeAd.promoTag }}</div>
              <div class="font-weight-black" style="font-size: 14.5px; line-height: 1.2">
                {{ activeAd.visualTitle }}
              </div>
              <div style="font-size: 11px; opacity: 0.9">{{ activeAd.visualSub }}</div>
            </div>
          </div>
        </div>

        <div class="d-flex flex-column flex-sm-row align-start align-sm-center justify-space-between ga-3 pa-3 px-sm-4 flex-grow-1">
          <div style="min-width: 0; flex: 1">
            <div class="d-flex align-center ga-2 mb-1">
              <span class="font-weight-black text-uppercase" :style="{ color: activeAd.accentColor, fontSize: '10.5px', letterSpacing: '0.04em' }">
                {{ activeAd.advertiser }}
              </span>
              <span class="sw-rating-chip">★ {{ activeAd.rating }}</span>
              <span class="text-body-small text-medium-emphasis d-none d-md-inline" style="font-size: 11px">
                • {{ activeAd.domain }}
              </span>
            </div>

            <div class="text-title-small font-weight-black mb-1" style="line-height: 1.28">
              {{ activeAd.headline }}
            </div>

            <div class="text-body-small text-medium-emphasis sw-clamp-1" style="line-height: 1.38">
              {{ activeAd.description }}
            </div>
          </div>

          <v-btn
            :color="activeAd.btnColor"
            variant="flat"
            size="small"
            rounded="pill"
            append-icon="mdi-arrow-right"
            class="font-weight-bold px-5 flex-shrink-0 text-white"
            @click="cycleNextAd"
          >
            {{ activeAd.cta }}
          </v-btn>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { useTheme } from 'vuetify'
import { useAuthStore } from '~/stores/auth'
import { useShopsStore } from '~/stores/shops'

const props = withDefaults(
  defineProps<{
    placement: 'infeed' | 'banner'
    variantIndex?: number
  }>(),
  {
    variantIndex: 0,
  },
)

const uid = Math.random().toString(36).slice(2, 8)
const authStore = useAuthStore()
const shopsStore = useShopsStore()
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
const showRichVisualAd = computed(() => adsenseConfig.value.test_mode)

const shouldDisplay = computed(() => {
  if (!import.meta.client) return false
  if (!adsenseConfig.value.enabled) return false
  if (!isAdAllowedOnRoute.value) return false
  return canMountRealGoogleTag.value || showRichVisualAd.value
})

/**
 * Each slot uses a distinct Google Display Network visual format so ads never look repetitive:
 * - Wide banners use 'leaderboard' (top) or 'showcase-card' (secondary)
 * - In-feed cards alternate between 'photo-card' (16:9 image-top card) and 'showcase-card' (icon + ★ rating card)
 */
const cardFormat = computed<'photo-card' | 'showcase-card' | 'leaderboard'>(() => {
  if (props.placement === 'banner') {
    return 'leaderboard'
  }
  return props.variantIndex % 2 === 0 ? 'photo-card' : 'showcase-card'
})

interface RichAdCreative {
  id: string
  topic: 'auto' | 'tech' | 'home' | 'lifestyle' | 'finance' | 'travel'
  advertiser: string
  domain: string
  rating: string
  shortBadge: string
  promoTag: string
  visualTitle: string
  visualSub: string
  icon: string
  gradient: string
  accentColor: string
  btnColor: string
  headline: string
  description: string
  cta: string
}

const allCreatives: RichAdCreative[] = [
  {
    id: 'supernet-5g',
    topic: 'tech',
    advertiser: 'Lao SuperNet 5G',
    domain: 'supernet5g.la',
    rating: '4.9',
    shortBadge: '5G MAX',
    promoTag: 'ຟຣີ +20GB',
    visualTitle: 'ເນັດ 5G ໄວສຸດທົ່ວລາວ',
    visualSub: 'ໂບນັດ 20GB ສຳລັບລູກຄ້າໃໝ່',
    icon: 'mdi-Signal-5g'.toLowerCase().replace('signal-5g', 'access-point-network'),
    gradient: 'linear-gradient(135deg, #1E3A8A 0%, #0284C7 55%, #38BDF8 100%)',
    accentColor: '#0284C7',
    btnColor: 'primary',
    headline: 'ແພັກເກັດເນັດມືຖື 5G ຄວາມໄວສູງ — ເປີດແຜນທີ່ GPS & ດູໜັງ 4K ບໍ່ສະດຸດ!',
    description: 'ສະໝັກມື້ນີ້ຮັບດາຕ້າໂບນັດຟຣີ 20GB ໃຊ້ໄດ້ທົ່ວນະຄອນຫຼວງວຽງຈັນ ແລະ ທຸກແຂວງ.',
    cta: 'ສະໝັກແພັກເກັດ',
  },
  {
    id: 'bolaven-coffee',
    topic: 'lifestyle',
    advertiser: 'Bolaven Roast Café',
    domain: 'bolavencafe.la',
    rating: '4.9',
    shortBadge: 'CAFE',
    promoTag: 'ຊື້ 1 ແຖມ 1',
    visualTitle: 'ກາເຟສົດ ພູພຽງບໍລະເວນ',
    visualSub: 'ຄົ່ວໃໝ່ທຸກເຊົ້າ • ສົ່ງດ່ວນ 20 ນາທີ',
    icon: 'mdi-coffee',
    gradient: 'linear-gradient(135deg, #451A03 0%, #92400E 55%, #D97706 100%)',
    accentColor: '#B45309',
    btnColor: 'warning',
    headline: 'ຫອມເຂັ້ມກາເຟອາຣາບິກ້າແທ້ 100% — ສັ່ງມື້ນີ້ ຊື້ 1 ແກ້ວ ແຖມຟຣີ 1 ແກ້ວ!',
    description: 'ມີທັງອາເມຣິກາໂນ້ເຢັນ, ລາເຕ້ຄາຣາເມວ ແລະ ເຂົ້າໜົມອົບສົດໃໝ່ ພ້ອມສົ່ງເຖິງຫ້ອງການ.',
    cta: 'ສັ່ງກາເຟເລີຍ',
  },
  {
    id: 'tire-center',
    topic: 'auto',
    advertiser: 'Vientiane AutoTire & Battery',
    domain: 'autotirelaos.com',
    rating: '4.8',
    shortBadge: '0% ຜ່ອນ',
    promoTag: 'ຜ່ອນ 0% • 6 ເດືອນ',
    visualTitle: 'ປ່ຽນຢາງລົດ 4 ເສັ້ນ ຟຣີຕັ້ງສູນ',
    visualSub: 'Michelin • Bridgestone • Yokohama',
    icon: 'mdi-tire',
    gradient: 'linear-gradient(135deg, #0F172A 0%, #1E40AF 60%, #F59E0B 100%)',
    accentColor: '#1D4ED8',
    btnColor: 'primary',
    headline: 'ໂປຣປ່ຽນຢາງລົດໃໝ່ 4 ເສັ້ນ ຜ່ອນ 0% ດອກເບ້ຍ + ແຖມຟຣີກວດເຊັກຊ່ວງລ່າງ 24 ລາຍການ',
    description: 'ຮັບປະກັນຢາງແທ້ຈາກສູນ ພ້ອມບໍລິການປ່ຽນແບັດເຕີຣີ້ລົດນອກສະຖານທີ່ທົ່ວວຽງຈັນ.',
    cta: 'ເຊັກລາຄາຢາງ',
  },
  {
    id: 'safedrive-insure',
    topic: 'auto',
    advertiser: 'Lao SafeDrive Insurance',
    domain: 'safedrive.la',
    rating: '4.9',
    shortBadge: '24/7',
    promoTag: 'ຟຣີລົດລາກ 24 ຊມ.',
    visualTitle: 'ປະກັນໄພລົດຍົນ ຊັ້ນ 1 ອຸ່ນໃຈທຸກເສັ້ນທາງ',
    visualSub: 'ເຄລມໄວພາຍໃນ 15 ນາທີ ຜ່ານມືຖື',
    icon: 'mdi-shield-car',
    gradient: 'linear-gradient(135deg, #064E3B 0%, #059669 58%, #34D399 100%)',
    accentColor: '#059669',
    btnColor: 'success',
    headline: 'ລົດເສຍ ຫຼື ເກີດອຸບັດຕິເຫດກາງທາງ ມີທີມຊ່ວຍເຫຼືອ ແລະ ລົດລາກຟຣີ 24 ຊົ່ວໂມງ!',
    description: 'ເບ້ຍປະກັນເລີ່ມຕົ້ນພຽງມື້ລະ 5,000 ກີບ ຄຸ້ມຄອງຄົບທັງລົດນ້ຳມັນ ແລະ ລົດໄຟຟ້າ EV.',
    cta: 'ຄຳນວນເບ້ຍຟຣີ',
  },
  {
    id: 'galaxy-icenter',
    topic: 'tech',
    advertiser: 'SmartTech Center Vientiane',
    domain: 'smarttech.la',
    rating: '4.9',
    shortBadge: 'TRADE-IN',
    promoTag: 'ເກົ່າແລກໃໝ່ -30%',
    visualTitle: 'ມືຖືຈໍແຕກ ນຳມາເທີນເຄື່ອງໃໝ່ໄດ້!',
    visualSub: 'ຮັບສ່ວນຫຼຸດສູງສຸດ 3,500,000 ກີບ',
    icon: 'mdi-cellphone-screenshot',
    gradient: 'linear-gradient(135deg, #311042 0%, #6D28D9 55%, #EC4899 100%)',
    accentColor: '#7C3AED',
    btnColor: 'secondary',
    headline: 'ຢ່າປ່ອຍມືຖືເກົ່າຖິ້ມລ້າ! ເຄື່ອງຈໍແຕກ-ແບັດເສື່ອມ ນຳມາແລກຊື້ເຄື່ອງໃໝ່ສູນແທ້ໄດ້ທັນທີ',
    description: 'ຜ່ອນສະບາຍ 0% ພ້ອມຮັບປະກັນສູນ 1 ປີເຕັມ ແລະ ຟິມກັນແຕກເກຣດພຣີມຽມຟຣີ.',
    cta: 'ປະເມີນລາຄາເຄື່ອງ',
  },
  {
    id: 'coolhome-aircon',
    topic: 'home',
    advertiser: 'CoolHome Inverter Laos',
    domain: 'coolhome.la',
    rating: '4.8',
    shortBadge: 'INVERTER',
    promoTag: 'ຫຼຸດ 30% + ຕິດຕັ້ງຟຣີ',
    visualTitle: 'ແອອິນເວີເຕີ້ ປະຢັດໄຟສູງສຸດ 50%',
    visualSub: 'ເຢັນໄວ ງຽບສະໜິດ ຮັບປະກັນຄອມເພຣສເຊີ້ 10 ປີ',
    icon: 'mdi-air-conditioner',
    gradient: 'linear-gradient(135deg, #0C4A6E 0%, #0284C7 55%, #2DD4BF 100%)',
    accentColor: '#0284C7',
    btnColor: 'primary',
    headline: 'ອາກາດຮ້ອນແນວນີ້ ປ່ຽນມາໃຊ້ແອ Inverter ເບີ 5 — ຕິດຕັ້ງຟຣີພາຍໃນມື້ດຽວ!',
    description: 'ແຖມຟຣີທໍ່ທອງແດງ 4 ແມັດ ແລະ ບໍລິການລ້າງແອຟຣີ 2 ຄັ້ງທຳອິດ.',
    cta: 'ເບິ່ງລຸ້ນທີ່ຫຼຸດລາຄາ',
  },
  {
    id: 'smartpay-qr',
    topic: 'finance',
    advertiser: 'LaoPay Digital Wallet',
    domain: 'laopay.la',
    rating: '4.9',
    shortBadge: 'CASHBACK',
    promoTag: 'ຄືນເງິນ 10%',
    visualTitle: 'ສະແກນ QR ຈ່າຍຄ່າຊ່າງ ຮັບເງິນຄືນທັນທີ',
    visualSub: 'ໃຊ້ໄດ້ທຸກຮ້ານສ້ອມແປງ ແລະ ຮ້ານຄ້າທົ່ວປະເທດ',
    icon: 'mdi-qrcode-scan',
    gradient: 'linear-gradient(135deg, #7C2D12 0%, #EA580C 55%, #FBBF24 100%)',
    accentColor: '#EA580C',
    btnColor: 'warning',
    headline: 'ຈ່າຍຄ່າສ້ອມແປງລົດ, ຄ່າຢາ ຫຼື ຄ່າກາເຟຜ່ານ QR ຮັບເງິນຄືນ Cashback 10% ທຸກບິນ!',
    description: 'ດາວໂຫຼດຟຣີ ບໍ່ມີຄ່າທຳນຽມລາຍປີ ໂອນໄວປອດໄພຕະຫຼອດ 24 ຊົ່ວໂມງ.',
    cta: 'ຮັບສິດ Cashback',
  },
  {
    id: 'vangvieng-resort',
    topic: 'travel',
    advertiser: 'NamSong Riverside Resort',
    domain: 'namsongresort.la',
    rating: '4.9',
    shortBadge: 'RESORT',
    promoTag: 'ຫຼຸດ 40% ທ້າຍອາທິດ',
    visualTitle: 'ພັກຜ່ອນແຄມນ້ຳຊອງ ວັງວຽງ ວິວພູຜາ',
    visualSub: 'ລວມອາຫານເຊົ້າ 2 ທ່ານ + ສະລອຍນ້ຳວິວພູ',
    icon: 'mdi-island',
    gradient: 'linear-gradient(135deg, #134E4A 0%, #0D9488 55%, #38BDF8 100%)',
    accentColor: '#0D9488',
    btnColor: 'success',
    headline: 'ຂັບລົດທ່ຽວວັງວຽງເສົາ-ອາທິດນີ້! ຫ້ອງພັກວິວແມ່ນ້ຳຊອງ ຫຼຸດພິເສດ 40%',
    description: 'ເດີນທາງຈາກວຽງຈັນພຽງ 1 ຊົ່ວໂມງເຄິ່ງ ຜ່ານທາງດ່ວນ ມີບ່ອນຈອດລົດກວ້າງຂວາງປອດໄພ.',
    cta: 'ຈອງຫ້ອງພັກລາຄາພິເສດ',
  },
]

/**
 * Contextual AdSense Ordering:
 * Just like Google AdSense contextual targeting, prioritize relevant topics when the user searches
 * a specific problem (car/tire, phone/screen, aircon/pipe), while keeping every slot on the page unique!
 */
const orderedPool = computed<RichAdCreative[]>(() => {
  const q = (shopsStore.problemQuery || '').toLowerCase()
  let preferredTopic: RichAdCreative['topic'] | null = null
  if (q.includes('ລົດ') || q.includes('ຢາງ') || q.includes('ເຄື່ອງ') || q.includes('ແບັດ')) {
    preferredTopic = 'auto'
  } else if (q.includes('ຈໍ') || q.includes('ໂທລະສັບ') || q.includes('ຄອມ')) {
    preferredTopic = 'tech'
  } else if (q.includes('ແອ') || q.includes('ນ້ຳ') || q.includes('ໄຟ')) {
    preferredTopic = 'home'
  }

  if (!preferredTopic) return allCreatives
  const matching = allCreatives.filter((c) => c.topic === preferredTopic)
  const rest = allCreatives.filter((c) => c.topic !== preferredTopic)
  return [...matching, ...rest]
})

// Guarantee every slot index starts on a completely different creative!
const slotSeedOffset = computed(() => {
  const base = props.placement === 'banner' ? props.variantIndex * 3 : 1 + props.variantIndex * 2
  return base % orderedPool.value.length
})

const rotationTick = ref(0)

const activeAd = computed(() => {
  const pool = orderedPool.value
  const idx = (slotSeedOffset.value + rotationTick.value) % pool.length
  return pool[idx]!
})

function cycleNextAd() {
  rotationTick.value += 1
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
  // Stagger rotation interval per slot (12s, 15s, 18s...) so slots never switch in lockstep
  const intervalMs = 12000 + (props.variantIndex % 5) * 3200
  rotateTimer = setInterval(() => {
    rotationTick.value += 1
  }, intervalMs)
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

.sw-gdn-card {
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.sw-gdn-light {
  background: #ffffff !important;
  border: 1px solid rgba(15, 23, 42, 0.1) !important;
  box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06) !important;
}

.sw-gdn-dark {
  background: rgba(17, 26, 43, 0.96) !important;
  border: 1px solid rgba(148, 163, 184, 0.2) !important;
  box-shadow: 0 6px 22px rgba(0, 0, 0, 0.35) !important;
}

/* Authentic Google AdChoices top-right corner strip */
.sw-gdn-corner {
  position: absolute;
  top: 0;
  right: 0;
  z-index: 5;
  background: rgba(255, 255, 255, 0.94);
  border-bottom-left-radius: 8px;
  padding: 1px 5px;
  gap: 3px;
  box-shadow: -1px 1px 4px rgba(0, 0, 0, 0.1);
}

.sw-gdn-dark .sw-gdn-corner {
  background: rgba(15, 23, 42, 0.92);
}

.sw-gdn-corner-label {
  font-size: 9.5px;
  font-weight: 700;
  color: #00aecd;
  padding-right: 2px;
}

.sw-gdn-corner-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border: none;
  background: transparent;
  color: #00aecd;
  font-size: 10px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  border-radius: 3px;
}

.sw-gdn-corner-btn:hover {
  background: rgba(0, 174, 205, 0.14);
}

/* Format A: Photo-Top Card */
.sw-photo-cover {
  min-height: 118px;
}

.sw-scene-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.sw-photo-badge {
  display: inline-block;
  font-size: 9.5px;
  font-weight: 900;
  letter-spacing: 0.04em;
  padding: 2px 8px;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.32);
  backdrop-filter: blur(4px);
}

.sw-hero-emblem {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  border: 1.5px solid rgba(255, 255, 255, 0.38);
  backdrop-filter: blur(4px);
  flex-shrink: 0;
}

.sw-round-arrow-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
  transition: transform 0.15s ease;
}

.sw-round-arrow-btn:hover {
  transform: scale(1.06);
}

/* Format B: Product / App Showcase Card */
.sw-brand-squircle {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.sw-rating-chip {
  display: inline-flex;
  align-items: center;
  font-size: 10.5px;
  font-weight: 800;
  color: #d97706;
  background: rgba(245, 158, 11, 0.14);
  padding: 1px 6px;
  border-radius: 5px;
}

.sw-offer-chip {
  display: inline-flex;
  align-items: center;
  font-size: 10px;
  font-weight: 800;
  border: 1px solid currentColor;
  padding: 0 6px;
  border-radius: 5px;
}

/* Format C: Wide Leaderboard */
.sw-leaderboard-art {
  min-width: 265px;
}

@media (max-width: 599px) {
  .sw-leaderboard-art {
    width: 100%;
    min-width: 0;
    justify-content: flex-start !important;
  }
}

.sw-leaderboard-icon {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.32);
  flex-shrink: 0;
}
</style>
