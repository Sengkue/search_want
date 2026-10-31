<template>
  <v-sheet
    v-if="shouldDisplay"
    rounded="xl"
    class="sw-adsense-card pa-3"
    :class="[
      placement === 'banner' ? 'sw-adsense-banner' : 'sw-adsense-infeed',
      isDark ? 'sw-adsense-dark' : 'sw-adsense-light',
    ]"
    data-testid="adsense-slot"
    :data-placement="placement"
  >
    <!-- Mandatory Clear Ad Disclosure Bar (Google AdSense Policy Compliant) -->
    <div class="d-flex align-center justify-space-between ga-2 mb-2">
      <div class="d-flex align-center ga-1">
        <span class="sw-ad-badge">ໂຄສະນາ</span>
        <span class="text-body-small text-medium-emphasis" style="font-size: 11px">
          • Google AdSense
        </span>
        <v-chip
          v-if="showPreviewCard"
          size="x-small"
          color="warning"
          variant="tonal"
          class="ml-1"
          style="height: 18px; font-size: 10px"
        >
          ໂໝດທົດລອງ
        </v-chip>
      </div>

      <NuxtLink
        v-if="authStore.isAdmin"
        to="/admin/approvals?tab=ADSENSE"
        class="text-body-small text-primary text-decoration-none d-flex align-center ga-1 font-weight-bold"
        style="font-size: 11px"
      >
        <v-icon icon="mdi-cog-outline" size="13" />
        <span>ຕັ້ງຄ່າ AdSense</span>
      </NuxtLink>
    </div>

    <!-- LIVE GOOGLE ADSENSE UNIT (<ins class="adsbygoogle">) -->
    <div v-if="renderLiveGoogleIns" class="sw-adsense-live-wrap">
      <ins
        ref="insEl"
        class="adsbygoogle"
        style="display: block; min-height: 90px"
        :data-ad-client="effectiveClientId"
        :data-ad-slot="slotId"
        data-ad-format="auto"
        data-full-width-responsive="true"
        :data-adtest="adsenseConfig.test_mode ? 'on' : undefined"
      />
    </div>

    <!-- FRIENDLY PREVIEW / TEST MODE UNIT (For localhost / LAN or before slot approval) -->
    <div
      v-else-if="showPreviewCard"
      class="d-flex flex-wrap flex-sm-nowrap align-center justify-space-between ga-3"
    >
      <div class="d-flex align-center ga-3" style="min-width: 0; flex: 1">
        <v-avatar
          :color="previewCreative.color"
          :size="placement === 'banner' ? 38 : 36"
          rounded="lg"
          variant="tonal"
          class="flex-shrink-0"
        >
          <v-icon :icon="previewCreative.icon" size="19" />
        </v-avatar>

        <div style="min-width: 0">
          <div class="text-title-small font-weight-bold text-truncate">
            {{ previewCreative.title }}
          </div>
          <div class="text-body-small text-medium-emphasis sw-clamp-2">
            {{ previewCreative.subtitle }}
          </div>
          <div
            v-if="hasValidClientId"
            class="text-body-small text-primary mt-1"
            style="font-size: 10.5px"
          >
            ເຊື່ອມຕໍ່ແລ້ວ: {{ effectiveClientId }}
            <span v-if="slotId">• Slot {{ slotId }}</span>
          </div>
        </div>
      </div>

      <v-btn
        :to="previewCreative.to"
        color="primary"
        variant="tonal"
        size="small"
        :append-icon="previewCreative.ctaIcon"
        class="flex-shrink-0"
      >
        {{ previewCreative.cta }}
      </v-btn>
    </div>
  </v-sheet>
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
  isLocalOrPrivateHost,
} = useAdSense()

const insEl = ref<HTMLElement | null>(null)
const pushedKey = ref('')

const slotId = computed(() =>
  props.placement === 'infeed' ? effectiveSlotInfeed.value : effectiveSlotBanner.value,
)

/**
 * Show local preview card when Test Mode is ON and either:
 * 1) Admin has not entered a production ca-pub-XXXXXXXXXXXXXXXX / Slot ID yet, OR
 * 2) Running on localhost / private LAN IP where Google AdSense servers do not serve live creatives.
 */
const showPreviewCard = computed(() => {
  if (!adsenseConfig.value.test_mode) return false
  if (!hasValidClientId.value || !slotId.value) return true
  return isLocalOrPrivateHost.value
})

const renderLiveGoogleIns = computed(
  () => hasValidClientId.value && Boolean(slotId.value) && !showPreviewCard.value,
)

const shouldDisplay = computed(() => {
  if (!import.meta.client) return false
  if (!adsenseConfig.value.enabled) return false
  if (!isAdAllowedOnRoute.value) return false
  return renderLiveGoogleIns.value || showPreviewCard.value
})

const previewCreatives = [
  {
    icon: 'mdi-store-check-outline',
    color: 'primary',
    title: 'ເປັນເຈົ້າຂອງຮ້ານ ຫຼື ຊ່າງສ້ອມແປງບໍ? ເພີ່ມຮ້ານເທິງແຜນທີ່ຟຣີ!',
    subtitle: 'ໃຫ້ລູກຄ້າໃກ້ຄຽງທີ່ກຳລັງມີບັນຫາ ຄົ້ນຫາຮ້ານຂອງທ່ານພົບ ແລະ ໂທຫາໄດ້ທັນທີ.',
    cta: 'ເພີ່ມຮ້ານຟຣີ',
    ctaIcon: 'mdi-arrow-right',
    to: '/shops/add',
  },
  {
    icon: 'mdi-shield-car',
    color: 'success',
    title: 'ບໍລິການຊ່ວຍເຫຼືອສຸກເສີນ & ປະກັນໄພລົດຍົນ 24 ຊົ່ວໂມງ',
    subtitle: 'ພື້ນທີ່ໂຄສະນາ Google AdSense ສຳລັບທຸລະກິດທ້ອງຖິ່ນ, ອາໄຫຼ່ລົດ ແລະ ບໍລິການສ້ອມແປງ.',
    cta: 'ເບິ່ງບໍລິການ',
    ctaIcon: 'mdi-open-in-new',
    to: '/shops/add',
  },
  {
    icon: 'mdi-bullhorn-outline',
    color: 'secondary',
    title: 'ພື້ນທີ່ໂຄສະນາ Google AdSense (ແບນເນີອັດຕະໂນມັດ)',
    subtitle: 'ຮອງຮັບທັງມືຖື ແລະ ຄອມພິວເຕີ — ປ່ຽນເປັນໂຄສະນາຈິງທັນທີເມື່ອໃສ່ Publisher ID ໃນໜ້າຜູ້ດູແລ.',
    cta: 'ລົງຮ້ານຂອງທ່ານ',
    ctaIcon: 'mdi-store-plus-outline',
    to: '/shops/add',
  },
]

const previewCreative = computed(() => {
  if (props.placement === 'banner') {
    return previewCreatives[2]!
  }
  return previewCreatives[props.variantIndex % 2]!
})

function tryPushAdSense() {
  if (!import.meta.client || !renderLiveGoogleIns.value || !insEl.value) return
  const key = `${effectiveClientId.value}:${slotId.value}:${props.placement}`
  if (pushedKey.value === key) return
  try {
    const w = window as any
    w.adsbygoogle = w.adsbygoogle || []
    w.adsbygoogle.push({})
    pushedKey.value = key
  } catch {
    // Ignore duplicate push or adblocker errors gracefully
  }
}

watch([renderLiveGoogleIns, effectiveClientId, slotId], () => {
  nextTick(() => tryPushAdSense())
})

onMounted(() => {
  nextTick(() => tryPushAdSense())
})
</script>

<style scoped>
.sw-adsense-card {
  position: relative;
  transition: border-color 0.2s ease, background-color 0.2s ease;
}

.sw-adsense-light {
  background: linear-gradient(135deg, rgba(248, 250, 252, 0.96) 0%, rgba(239, 246, 255, 0.88) 100%) !important;
  border: 1px dashed rgba(37, 99, 235, 0.28) !important;
}

.sw-adsense-dark {
  background: linear-gradient(135deg, rgba(17, 28, 46, 0.95) 0%, rgba(24, 38, 64, 0.9) 100%) !important;
  border: 1px dashed rgba(96, 165, 250, 0.3) !important;
}

.sw-ad-badge {
  display: inline-flex;
  align-items: center;
  padding: 1px 6px;
  border-radius: 5px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.02em;
  color: #1d4ed8;
  background: rgba(37, 99, 235, 0.12);
}

.sw-adsense-dark .sw-ad-badge {
  color: #93c5fd;
  background: rgba(96, 165, 250, 0.18);
}

.sw-adsense-live-wrap {
  width: 100%;
  overflow: hidden;
  border-radius: 10px;
}
</style>
