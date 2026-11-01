<template>
  <v-container fluid class="pa-2 pa-sm-3 pa-md-5" style="max-width: 1520px">
    <!-- Compact, Friendly Problem Search Header with Signature Brand Icon & Ambient Surface -->
    <v-card class="sw-hero-card sw-hero-search-card pa-3 pa-md-4 mb-3">
      <!-- Top Title + 1-Tap GPS Pill -->
      <div class="d-flex align-center justify-space-between ga-2 mb-2">
        <div class="d-flex align-center ga-2" style="min-width: 0">
          <BrandLogo :size="smAndDown ? 32 : 38" />
          <div style="min-width: 0">
            <h1 class="text-title-medium text-md-title-large font-weight-black text-truncate" style="line-height: 1.25">
              ມີບັນຫາ ແຕ່ບໍ່ຮູ້ຈະໄປໃສ?
            </h1>
            <p class="text-body-small text-medium-emphasis d-none d-sm-block mb-0">
              ບອກບັນຫາຂອງທ່ານ ເຮົາຊ່ວຍຈັບຄູ່ຊ່າງ ແລະ ຮ້ານທີ່ອະນຸມັດແລ້ວໃກ້ຕົວທ່ານທັນທີ 
            </p>
          </div>
        </div>

        <v-btn
          color="primary"
          :variant="shopsStore.hasLiveGps ? 'flat' : 'tonal'"
          size="small"
          prepend-icon="mdi-crosshairs-gps"
          :loading="shopsStore.locatingGps"
          class="flex-shrink-0"
          @click="handleLocateMe"
        >
          {{ shopsStore.hasLiveGps ? 'ໂຫຼດ GPS ໃໝ່' : 'ໃຊ້ GPS ປັດຈຸບັນ' }}
        </v-btn>
      </div>

      <!-- Native-Grade Pill Search Capsule + Perfect Mobile Search Button + Smart Keyboard Autocomplete -->
      <div ref="searchWrapperRef" class="sw-search-wrapper mb-2">
        <form
          class="sw-search-capsule"
          :class="{
            'is-focused': isSearchFocused,
            'has-query': Boolean(trimmedProblemQuery),
          }"
          role="search"
          @submit.prevent="submitSearchFromUi"
        >
          <!-- Leading Search Icon Pill (Intentionally focuses input when tapped) -->
          <button
            type="button"
            class="sw-search-lead-icon"
            tabindex="-1"
            aria-label="ແຕະເພື່ອພິມຄຳຄົ້ນຫາ"
            @click="focusSearchInput"
          >
            <v-icon icon="mdi-magnify" :size="smAndDown ? 18 : 20" />
          </button>

          <!-- Native Search Input (16px font = zero mobile browser zoom; enterkeyhint="search" = native Search key) -->
          <input
            ref="searchInputRef"
            v-model="shopsStore.problemQuery"
            type="search"
            inputmode="search"
            enterkeyhint="search"
            autocomplete="off"
            autocorrect="off"
            autocapitalize="off"
            spellcheck="false"
            class="sw-search-input"
            :placeholder="
              smAndDown
                ? 'ພິມອາການ ເຊັ່ນ: ລົດສະຕາດບໍ່ຕິດ, ຢາງຮົ່ວ...'
                : 'ພິມອາການ ຫຼື ບັນຫາ ເຊັ່ນ: ລົດສະຕາດບໍ່ຕິດ, ຢາງລົດແບນ, ທໍ່ນ້ຳຮົ່ວ, ແອບໍ່ເຢັນ...'
            "
            aria-label="ຄົ້ນຫາບັນຫາ ຫຼື ອາການເປ່ເພ"
            @focus="handleSearchFocus"
            @blur="handleInputBlur"
            @keydown.esc.prevent="dismissMobileKeyboard"
          />

          <!-- Clean 1-Tap Clear Button (Never triggers unwanted mobile keyboard popup) -->
          <button
            v-if="shopsStore.problemQuery.length > 0"
            type="button"
            class="sw-search-clear-btn"
            aria-label="ລ້າງຄຳຄົ້ນຫາ"
            title="ລ້າງຄຳຄົ້ນຫາ"
            @mousedown.prevent
            @click.stop="clearProblemAndSearch"
          >
            <v-icon icon="mdi-close-circle" :size="smAndDown ? 18 : 19" />
          </button>

          <!-- Signature Gradient Pill Search Button (Never focuses input; immediately dismisses mobile keyboard!) -->
          <button
            type="submit"
            class="sw-search-submit-btn"
            :disabled="shopsStore.loadingNearby"
            aria-label="ຄົ້ນຫາຮ້ານໃກ້ຄຽງ"
            @mousedown.prevent
          >
            <v-progress-circular
              v-if="shopsStore.loadingNearby"
              indeterminate
              :size="smAndDown ? 15 : 16"
              :width="2.2"
              color="white"
            />
            <v-icon v-else icon="mdi-magnify" :size="smAndDown ? 16 : 18" />
            <span>ຄົ້ນຫາ</span>
          </button>
        </form>

        <!-- Smart Floating Symptom & Quick-Search Panel while Keyboard / Input is Focused -->
        <div
          v-if="isSearchFocused"
          class="sw-search-dropdown"
          role="listbox"
          aria-label="ຄຳແນະນຳການຄົ້ນຫາອາການ"
        >
          <div class="sw-search-dropdown-header">
            <span class="text-body-small font-weight-bold text-medium-emphasis d-flex align-center ga-1">
              <v-icon
                :icon="trimmedProblemQuery ? 'mdi-Creation' : 'mdi-lightning-bolt-outline'"
                size="15"
                color="primary"
              />
              <span>
                {{
                  trimmedProblemQuery
                    ? 'ອາການທີ່ກ່ຽວຂ້ອງ — ແຕະເພື່ອຄົ້ນຫາທັນທີ'
                    : 'ອາການຍອດນິຍົມ — ແຕະເພື່ອຄົ້ນຫາໂດຍບໍ່ຕ້ອງພິມ'
                }}
              </span>
            </span>

            <button
              type="button"
              class="sw-keyboard-dismiss-pill"
              @mousedown.prevent
              @click.stop="dismissMobileKeyboard"
            >
              <v-icon icon="mdi-keyboard-close" size="14" />
              <span>ປິດ</span>
            </button>
          </div>

          <!-- Recent Searches Strip (when input is empty and user has prior searches) -->
          <div
            v-if="!trimmedProblemQuery && recentSearches.length > 0"
            class="px-3 pt-2 pb-1 border-b"
          >
            <div class="d-flex align-center justify-space-between mb-1">
              <span class="text-body-small text-medium-emphasis font-weight-medium" style="font-size: 11px">
                ຄົ້ນຫາຫຼ້າສຸດ
              </span>
              <button
                type="button"
                class="text-body-small text-primary font-weight-bold bg-transparent border-0 pa-0"
                style="font-size: 11px; cursor: pointer"
                @mousedown.prevent
                @click.stop="clearRecentSearches"
              >
                ລ້າງປະຫວັດ
              </button>
            </div>
            <div class="sw-chip-rail pb-1">
              <v-chip
                v-for="recent in recentSearches"
                :key="recent"
                size="x-small"
                variant="tonal"
                color="primary"
                prepend-icon="mdi-history"
                @mousedown.prevent
                @click.stop="selectSuggestion(recent)"
              >
                {{ recent }}
              </v-chip>
            </div>
          </div>

          <div class="sw-search-suggest-list">
            <!-- Direct Submit Row for User's Custom Typed Text -->
            <button
              v-if="trimmedProblemQuery"
              type="button"
              class="sw-search-suggest-item"
              @mousedown.prevent
              @click.stop="submitSearchFromUi"
            >
              <span
                class="sw-suggest-icon-badge"
                style="background: rgba(26, 115, 232, 0.14); color: #1a73e8"
              >
                <v-icon icon="mdi-magnify" size="18" />
              </span>
              <span class="flex-grow-1" style="min-width: 0">
                <span class="d-block text-body-medium font-weight-bold text-primary text-truncate">
                  ຄົ້ນຫາ "{{ trimmedProblemQuery }}" ທັນທີ
                </span>
                <span class="d-block text-body-small text-medium-emphasis">
                  ຈັບຄູ່ຊ່າງ ແລະ ຮ້ານສ້ອມແປງໃກ້ຕົວທ່ານ
                </span>
              </span>
              <v-icon icon="mdi-arrow-right-circle" color="primary" size="18" />
            </button>

            <!-- Live Matched Symptoms & Curated Quick Problems -->
            <button
              v-for="item in liveSuggestions"
              :key="item.key"
              type="button"
              class="sw-search-suggest-item"
              @mousedown.prevent
              @click.stop="selectSuggestion(item.query)"
            >
              <span
                class="sw-suggest-icon-badge"
                :style="{ backgroundColor: `${item.color}1c`, color: item.color }"
              >
                <v-icon :icon="item.icon" size="17" />
              </span>
              <span class="flex-grow-1" style="min-width: 0">
                <span class="d-block text-body-medium font-weight-bold text-truncate">
                  {{ item.title }}
                </span>
                <span class="d-block text-body-small text-medium-emphasis text-truncate">
                  {{ item.subtitle }}
                </span>
              </span>
              <v-icon icon="mdi-north-west" size="15" class="text-medium-emphasis flex-shrink-0" />
            </button>
          </div>
        </div>
      </div>

      <!-- Single-Row Swipeable Filter & Quick-Problem Chips -->
      <div class="sw-chip-rail mb-2">
        <!-- Distance Menu Chip -->
        <v-menu location="bottom start">
          <template #activator="{ props: menuProps }">
            <v-chip
              v-bind="menuProps"
              size="small"
              color="primary"
              variant="tonal"
              prepend-icon="mdi-map-marker-radius"
              append-icon="mdi-chevron-down"
              class="font-weight-bold"
            >
              {{ currentRadiusLabel }}
            </v-chip>
          </template>
          <v-list density="compact" min-width="160">
            <v-list-item
              v-for="opt in radiusOptions"
              :key="String(opt.value)"
              :active="shopsStore.radiusKm === opt.value"
              color="primary"
              @click="selectRadius(opt.value)"
            >
              <v-list-item-title class="text-body-small font-weight-medium">
                {{ opt.label }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <!-- 24h Emergency Filter Pill -->
        <v-chip
          size="small"
          :color="shopsStore.emergencyOnly ? 'error' : undefined"
          :variant="shopsStore.emergencyOnly ? 'flat' : 'outlined'"
          prepend-icon="mdi-alarm-light-outline"
          class="font-weight-bold"
          @click="toggleEmergencyOnly"
        >
          24 ຊມ.
        </v-chip>

        <v-divider vertical class="mx-1 my-1" />

        <!-- Quick Common Problem Chips (1 horizontal row, zero wrapping clutter) -->
        <v-chip
          v-for="preset in quickProblems"
          :key="preset.query"
          size="small"
          :color="shopsStore.problemQuery === preset.query ? 'primary' : undefined"
          :variant="shopsStore.problemQuery === preset.query ? 'flat' : 'tonal'"
          :prepend-icon="preset.icon"
          @click="applyQuickProblem(preset.query)"
        >
          {{ preset.label }}
        </v-chip>
      </div>

      <!-- Single-Row Swipeable Category Strip -->
      <div class="sw-chip-rail">
        <v-chip
          size="small"
          :color="shopsStore.selectedCategoryId === null ? 'primary' : undefined"
          :variant="shopsStore.selectedCategoryId === null ? 'flat' : 'outlined'"
          prepend-icon="mdi-apps"
          @click="selectCategory(null)"
        >
          ທຸກຮ້ານ
        </v-chip>

        <v-chip
          v-for="cat in shopsStore.categories"
          :key="cat.id"
          size="small"
          :color="shopsStore.selectedCategoryId === cat.id ? cat.color : undefined"
          :variant="shopsStore.selectedCategoryId === cat.id ? 'flat' : 'outlined'"
          :prepend-icon="cat.icon"
          :class="shopsStore.selectedCategoryId === cat.id ? 'text-white' : ''"
          @click="selectCategory(cat.id)"
        >
          {{ cat.name }} ({{ cat.shop_count }})
        </v-chip>
      </div>
    </v-card>

    <!-- Top Responsive Google AdSense Leaderboard Banner (Immediately visible above the fold) -->
    <AdSenseSlot placement="banner" :variant-index="0" class="mb-3" />

    <!-- Smart Problem Diagnosis Banner (Shown cleanly when user searches a symptom/problem) -->
    <v-alert
      v-if="diagnosis && (shopsStore.problemQuery.trim() || diagnosis.matched_categories.length > 0)"
      :type="nearbyShops.length > 0 ? 'info' : 'warning'"
      variant="tonal"
      border="start"
      rounded="xl"
      density="compact"
      class="mb-3"
    >
      <div class="font-weight-bold text-body-medium">
        {{ diagnosis.notification_summary }}
      </div>

      <div v-if="diagnosis.matched_categories.length" class="d-flex flex-wrap align-center ga-1 mt-1">
        <span class="text-body-small font-weight-bold mr-1">ຊ່າງທີ່ແນະນຳ:</span>
        <v-chip
          v-for="mc in diagnosis.matched_categories"
          :key="mc.id"
          size="x-small"
          :color="mc.color"
          variant="flat"
          :prepend-icon="mc.icon"
          class="text-white"
        >
          {{ mc.name }}
        </v-chip>
      </div>

      <ul v-if="diagnosis.advice_hints.length" class="text-body-small mt-1 pl-4 mb-0">
        <li v-for="(hint, idx) in diagnosis.advice_hints" :key="idx">
          {{ hint }}
        </li>
      </ul>
    </v-alert>

    <!-- Compact Results Summary + Mobile View Switcher Bar -->
    <div class="d-flex flex-wrap align-center justify-space-between ga-2 mb-2 px-1">
      <div class="d-flex align-center flex-wrap ga-2">
        <span class="text-title-small font-weight-bold">
          ຮ້ານທີ່ອະນຸມັດແລ້ວໃກ້ຄຽງ ({{ nearbyShops.length }})
        </span>
        <v-chip size="x-small" color="primary" variant="tonal" prepend-icon="mdi-map-marker">
          {{ shopsStore.locationLabel }}
        </v-chip>
      </div>

      <!-- Mobile Segmented View Pill -->
      <v-btn-toggle
        v-if="smAndDown"
        v-model="mobileViewMode"
        mandatory
        color="primary"
        density="compact"
        rounded="pill"
        variant="outlined"
        style="height: 28px"
      >
        <v-btn value="split" size="x-small" prepend-icon="mdi-view-agenda-outline">
          ທັງສອງ
        </v-btn>
        <v-btn value="map" size="x-small" prepend-icon="mdi-map-outline">
          ແຜນທີ່ເຕັມຈໍ
        </v-btn>
        <v-btn value="list" size="x-small" prepend-icon="mdi-format-list-bulleted">
          ລາຍການ ({{ nearbyShops.length }})
        </v-btn>
      </v-btn-toggle>
    </div>

    <!-- Responsive Split Content: Map + Distance-Sorted Shop Cards -->
    <v-row density="compact">
      <!-- Interactive Map Column (Compact 240px on mobile split view so cards appear right below!) -->
      <v-col
        v-if="!smAndDown || mobileViewMode !== 'list'"
        cols="12"
        md="7"
        order="1"
        order-md="2"
      >
        <v-card
          class="pa-1 pa-md-2 mb-2 mb-md-0"
          :style="
            smAndDown
              ? { height: mobileViewMode === 'map' ? 'calc(100vh - 255px)' : '235px' }
              : { height: 'calc(100vh - 235px)', minHeight: '520px', position: 'sticky', top: '72px' }
          "
        >
          <ShopMap
            mode="discover"
            :user-lat="shopsStore.userLat"
            :user-lng="shopsStore.userLng"
            :radius-km="shopsStore.radiusKm"
            :shops="nearbyShops"
            :selected-shop-id="shopsStore.selectedShopId"
            height="100%"
            @select-shop="handleSelectShop"
            @update:user-location="handleManualUserPin"
          />
        </v-card>
      </v-col>

      <!-- Nearby Matched Shops List Column -->
      <v-col
        v-if="!smAndDown || mobileViewMode !== 'map'"
        cols="12"
        md="5"
        order="2"
        order-md="1"
      >
        <v-progress-linear
          v-if="shopsStore.loadingNearby"
          indeterminate
          color="primary"
          rounded
          class="mb-2"
        />

        <template v-if="nearbyShops.length > 0">
          <template v-for="(shop, idx) in nearbyShops" :key="shop.id">
            <ShopCard
              :shop="shop"
              :selected="shop.id === shopsStore.selectedShopId"
              :user-lat="shopsStore.userLat"
              :user-lng="shopsStore.userLng"
              @select="handleSelectShop"
              @focus-map="handleFocusOnMap"
            />
            <AdSenseSlot
              v-if="idx === 0 || (idx > 0 && idx % 5 === 0)"
              placement="infeed"
              :variant-index="Math.floor(idx / 5)"
              class="mb-2"
            />
          </template>
        </template>

        <v-card v-else-if="!shopsStore.loadingNearby" class="pa-5 text-center">
          <v-avatar color="warning" variant="tonal" size="48" class="mb-2">
            <v-icon icon="mdi-map-marker-question-outline" size="26" />
          </v-avatar>
          <div class="text-title-medium font-weight-bold mb-1">
            ບໍ່ມີຮ້ານທີ່ອະນຸມັດແລ້ວໃນໄລຍະນີ້
          </div>
          <p class="text-body-small text-medium-emphasis mb-3">
            ລອງຂະຫຍາຍໄລຍະທາງເປັນທຸກໄລຍະທາງ ຫຼື ເລືອກໝວດໝູ່ບໍລິການອື່ນ.
          </p>
          <div class="d-flex flex-wrap justify-center ga-2">
            <v-btn
              color="primary"
              variant="flat"
              size="small"
              prepend-icon="mdi-earth"
              @click="expandToAllDistances"
            >
              ສະແດງທຸກໄລຍະທາງ
            </v-btn>
            <v-btn
              v-if="authStore.publicConfig.demo_mode && authStore.isAdmin"
              color="secondary"
              variant="tonal"
              size="small"
              prepend-icon="mdi-magic-staff"
              @click="shopsStore.seedDemoShopsNearCurrentLocation()"
            >
              ສ້າງຮ້ານທົດລອງໃກ້ຂ້ອຍ (Admin)
            </v-btn>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- Bottom Responsive Google AdSense Banner -->
    <AdSenseSlot placement="banner" :variant-index="2" class="mt-3" />
  </v-container>
</template>

<script setup lang="ts">
import { useDisplay } from 'vuetify'
import { useAuthStore } from '~/stores/auth'
import { useShopsStore } from '~/stores/shops'

const authStore = useAuthStore()
const shopsStore = useShopsStore()
const { requestMapPinPickCount } = useGps()
const route = useRoute()
const router = useRouter()
const { smAndDown } = useDisplay()

const mobileViewMode = ref<'split' | 'map' | 'list'>('split')

const radiusOptions = [
  { label: 'ພາຍໃນ 5 ກມ.', value: 5 },
  { label: 'ພາຍໃນ 15 ກມ.', value: 15 },
  { label: 'ພາຍໃນ 50 ກມ.', value: 50 },
  { label: 'ທຸກໄລຍະທາງ', value: null },
]

const currentRadiusLabel = computed(() => {
  const found = radiusOptions.find((o) => o.value === shopsStore.radiusKm)
  return found ? found.label : 'ທຸກໄລຍະທາງ'
})

const quickProblems = [
  { label: 'ລົດສະຕາດບໍ່ຕິດ', query: 'ລົດຂອງຂ້ອຍສະຕາດບໍ່ຕິດ ແລະ ບໍ່ຮູ້ຈະແກ້ແນວໃດ', icon: 'mdi-car-off' },
  { label: 'ຢາງລົດແບນ', query: 'ຢາງລົດແບນ ຖືກແທງເທິງທາງ', icon: 'mdi-car-tire-alert' },
  { label: 'ຕ້ອງການລົດລາກ', query: 'ລົດເສຍກາງທາງ ຕ້ອງການລົດລາກດ່ວນ', icon: 'mdi-tow-truck' },
  { label: 'ເຄື່ອງມີຄວັນ', query: 'ເຄື່ອງຍົນມີຄວັນ ແລະ ຮ້ອນເກີນ', icon: 'mdi-alert-octagon-outline' },
  { label: 'ໜ້າຈໍແຕກ', query: 'ໜ້າຈໍໂທລະສັບແຕກ', icon: 'mdi-cellphone-off' },
  { label: 'ທໍ່ນ້ຳຮົ່ວ', query: 'ທໍ່ນ້ຳໃນຫ້ອງນ້ຳຮົ່ວ ນ້ຳຮົ່ວ', icon: 'mdi-pipe-leak' },
  { label: 'ແອບໍ່ເຢັນ', query: 'ແອເຢັນບໍ່ເຢັນ ລົມອຸ່ນ', icon: 'mdi-air-conditioner' },
]

const nearbyShops = computed(() => shopsStore.nearbyData?.shops ?? [])
const diagnosis = computed(() => shopsStore.nearbyData?.diagnosis ?? null)

async function runProblemSearch() {
  await shopsStore.searchNearby(true)
}

async function clearProblemAndSearch() {
  shopsStore.problemQuery = ''
  await shopsStore.searchNearby(false)
}

async function selectRadius(val: number | null) {
  shopsStore.radiusKm = val
  await shopsStore.searchNearby(false)
}

async function toggleEmergencyOnly() {
  shopsStore.emergencyOnly = !shopsStore.emergencyOnly
  await shopsStore.searchNearby(false)
}

async function selectCategory(catId: number | null) {
  shopsStore.selectedCategoryId = shopsStore.selectedCategoryId === catId ? null : catId
  await shopsStore.searchNearby(false)
}

async function applyQuickProblem(q: string) {
  shopsStore.problemQuery = q
  shopsStore.selectedCategoryId = null
  await shopsStore.searchNearby(true)
}

async function handleLocateMe() {
  await shopsStore.detectBrowserGps(true)
}

async function handleManualUserPin(coords: { lat: number; lng: number }) {
  await shopsStore.setManualUserLocation(coords.lat, coords.lng, 'ໝຸດທີ່ເລືອກ')
}

function handleSelectShop(shopId: number) {
  shopsStore.selectedShopId = shopId
}

function handleFocusOnMap(shopId: number) {
  shopsStore.selectedShopId = shopId
  if (smAndDown.value && mobileViewMode.value === 'list') {
    mobileViewMode.value = 'map'
  }
}

async function expandToAllDistances() {
  shopsStore.radiusKm = null
  await shopsStore.searchNearby(true)
}

watch(requestMapPinPickCount, () => {
  if (smAndDown.value && mobileViewMode.value === 'list') {
    mobileViewMode.value = 'split'
  }
  nextTick(() => {
    document.querySelector('.sw-map-container')?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  })
  authStore.showToast(
    'ແຕະເທິງແຜນທີ່ ຫຼື ລາກໝຸດສີຟ້າເພື່ອກຳນົດຕຳແໜ່ງຂອງທ່ານ!',
    'info',
    'mdi-gesture-tap',
  )
})

onMounted(async () => {
  await shopsStore.loadCategoriesAndSymptoms()
  await shopsStore.searchNearby(false)
  if (route.query.autoGps === '1') {
    router.replace({ query: { ...route.query, autoGps: undefined } })
    await handleLocateMe()
  }
})
</script>
