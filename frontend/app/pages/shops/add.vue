<template>
  <v-container class="py-3 py-md-6 px-3" style="max-width: 1180px">
    <!-- Compact Page Header -->
    <div class="d-flex flex-wrap align-center justify-space-between ga-2 mb-3">
      <div class="d-flex align-center ga-2">
        <v-avatar color="primary" size="34" rounded="lg" variant="tonal">
          <v-icon icon="mdi-store-plus" size="19" />
        </v-avatar>
        <div>
          <h1 class="text-title-medium text-md-title-large font-weight-black" style="line-height: 1.2">
            ເພີ່ມຮ້ານຂອງທ່ານ ແລະ ປັກໝຸດທີ່ຕັ້ງ
          </h1>
          <p class="text-body-small text-medium-emphasis mb-0">
            ເພີ່ມຂໍ້ມູນຮ້ານດ້ວຍຕົນເອງ — ຜູ້ດູແລລະບົບພຽງແຕ່ກົດອະນຸມັດ ແລ້ວຮ້ານຈະຂຶ້ນແຜນທີ່ທັນທີ
          </p>
        </div>
      </div>

      <v-btn
        v-if="authStore.isLoggedIn"
        to="/shops/mine"
        variant="tonal"
        color="secondary"
        size="small"
        prepend-icon="mdi-storefront-outline"
      >
        ຮ້ານຂອງຂ້ອຍ
      </v-btn>
    </div>

    <!-- Visual 3-Step Friendly Guide Strip -->
    <div class="sw-chip-rail mb-3">
      <v-chip size="small" color="primary" variant="tonal" prepend-icon="mdi-numeric-1-circle">
        ປ້ອນຂໍ້ມູນຮ້ານ
      </v-chip>
      <v-icon icon="mdi-chevron-right" size="16" class="text-medium-emphasis" />
      <v-chip size="small" color="error" variant="tonal" prepend-icon="mdi-numeric-2-circle">
        ປັກໝຸດເທິງແຜນທີ່
      </v-chip>
      <v-icon icon="mdi-chevron-right" size="16" class="text-medium-emphasis" />
      <v-chip size="small" color="success" variant="tonal" prepend-icon="mdi-numeric-3-circle">
        ລໍຖ້າຜູ້ດູແລກົດອະນຸມັດ
      </v-chip>
    </div>

    <!-- Guest Sign-In Card -->
    <v-card v-if="!authStore.isLoggedIn" class="sw-hero-card pa-6 text-center">
      <div class="d-flex justify-center mb-2">
        <BrandLogo :size="50" />
      </div>
      <h2 class="text-title-medium font-weight-bold mb-1">ເຂົ້າສູ່ລະບົບເພື່ອເພີ່ມຮ້ານຂອງທ່ານ</h2>
      <p class="text-body-small text-medium-emphasis mb-4" style="max-width: 400px; margin: 0 auto">
        ເພື່ອໃຫ້ລະບົບສາມາດແຈ້ງເຕືອນທ່ານທັນທີ ເມື່ອຜູ້ດູແລລະບົບອະນຸມັດທີ່ຕັ້ງຮ້ານຂອງທ່ານ
      </p>
      <v-btn to="/login?redirect=/shops/add" color="primary" variant="flat" prepend-icon="mdi-login">
        ເຂົ້າສູ່ລະບົບ / ສ້າງບັນຊີ
      </v-btn>
    </v-card>

    <!-- Authenticated Shop Submission Form -->
    <v-form v-else @submit.prevent="handleSubmitShop">
      <v-alert v-if="errorMsg" type="error" variant="tonal" density="compact" class="mb-3 text-body-small">
        {{ errorMsg }}
      </v-alert>

      <v-row density="compact">
        <!-- Step 1: Shop Info -->
        <v-col cols="12" md="6">
          <v-card class="pa-3 pa-md-4 mb-2 mb-md-0">
            <div class="text-title-small font-weight-bold mb-3 d-flex align-center ga-1">
              <v-icon icon="mdi-numeric-1-circle" color="primary" size="18" />
              ຂໍ້ມູນຮ້ານ ແລະ ບັນຫາທີ່ແກ້ໄຂໄດ້
            </div>

            <v-text-field
              v-model="form.name"
              label="ຊື່ຮ້ານ / ອູ່ສ້ອມແປງ / ທຸລະກິດ *"
              placeholder="ເຊັ່ນ: ອູ່ສົມໃຈ ສ້ອມແປງລົດ"
              prepend-inner-icon="mdi-store-outline"
              required
              class="mb-2"
            />

            <v-select
              v-model="form.category_id"
              :items="shopsStore.categories"
              item-title="name"
              item-value="id"
              label="ໝວດໝູ່ບໍລິການ *"
              prepend-inner-icon="mdi-shape-outline"
              required
              class="mb-2"
            />

            <v-textarea
              v-model="form.description"
              label="ລາຍລະອຽດຮ້ານ ແລະ ບໍລິການ *"
              placeholder="ອະທິບາຍສິ່ງທີ່ທ່ານສ້ອມແປງ ເພື່ອໃຫ້ລູກຄ້າເຂົ້າໃຈງ່າຍ..."
              rows="2"
              required
              class="mb-2"
            />

            <v-text-field
              v-model="form.problem_tags"
              label="ບັນຫາ / ອາການທີ່ທ່ານແກ້ໄຂໄດ້ (ແຍກດ້ວຍເຄື່ອງໝາຍ ,)"
              placeholder="ເຊັ່ນ: ລົດສະຕາດບໍ່ຕິດ, ຢາງລົດແບນ"
              prepend-inner-icon="mdi-tag-multiple-outline"
              hide-details
              class="mb-2"
            />

            <!-- Single-Row Swipeable Quick Tag Chips -->
            <div class="sw-chip-rail mb-3">
              <span class="text-body-small text-medium-emphasis">ແຕະເພີ່ມ:</span>
              <v-chip
                v-for="tag in suggestedTags"
                :key="tag"
                size="x-small"
                variant="tonal"
                color="secondary"
                prepend-icon="mdi-plus"
                @click="appendTag(tag)"
              >
                {{ tag }}
              </v-chip>
            </div>

            <v-row density="compact">
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.phone"
                  label="ເບີໂທຕິດຕໍ່ *"
                  placeholder="+856 20 5555 1234"
                  prepend-inner-icon="mdi-phone-outline"
                  required
                />
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="form.opening_hours"
                  label="ເວລາເປີດ-ປິດ *"
                  placeholder="08:00 - 18:00"
                  prepend-inner-icon="mdi-clock-outline"
                  required
                />
              </v-col>
            </v-row>

            <v-text-field
              v-model="form.address"
              label="ທີ່ຢູ່ / ຈຸດສັງເກດ *"
              placeholder="ເຊັ່ນ: ຖະໜົນສາມແສນໄທ, ກົງກັນຂ້າມປັ໊ມນ້ຳມັນ"
              prepend-inner-icon="mdi-map-marker-outline"
              required
              hide-details
              class="mb-2"
            />

            <v-switch
              v-model="form.is_emergency_24h"
              color="error"
              density="compact"
              label="ຮັບສ້ອມແປງ / ຊ່ວຍເຫຼືອສຸກເສີນ 24 ຊມ."
              hide-details
            />
          </v-card>
        </v-col>

        <!-- Step 2: Interactive Map Pin Picker -->
        <v-col cols="12" md="6">
          <v-card class="pa-3 pa-md-4 h-100 d-flex flex-column">
            <div class="d-flex align-center justify-space-between ga-2 mb-2">
              <div class="text-title-small font-weight-bold d-flex align-center ga-1">
                <v-icon icon="mdi-numeric-2-circle" color="error" size="18" />
                ປັກໝຸດທີ່ຕັ້ງຮ້ານເທິງແຜນທີ່
              </div>

              <v-btn
                color="primary"
                variant="tonal"
                size="x-small"
                prepend-icon="mdi-crosshairs-gps"
                :loading="locatingPin"
                @click="pinAtMyCurrentGps"
              >
                ດຶງ GPS ຂອງຂ້ອຍ
              </v-btn>
            </div>

            <div class="flex-grow-1 mb-3" style="min-height: 270px">
              <ShopMap
                mode="picker"
                :picker-lat="form.latitude"
                :picker-lng="form.longitude"
                height="285px"
                @update:picker-location="updatePickedCoords"
              />
            </div>

            <v-row density="compact" class="mb-3">
              <v-col cols="6">
                <v-text-field
                  v-model.number="form.latitude"
                  label="ລະຕິຈູດ"
                  type="number"
                  step="0.000001"
                  hide-details
                />
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model.number="form.longitude"
                  label="ລອງຕິຈູດ"
                  type="number"
                  step="0.000001"
                  hide-details
                />
              </v-col>
            </v-row>

            <v-btn
              type="submit"
              color="primary"
              variant="flat"
              block
              prepend-icon="mdi-send-check"
              :loading="submitting"
            >
              ສົ່ງຮ້ານເພື່ອຂໍອະນຸມັດ
            </v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'
import { useShopsStore } from '~/stores/shops'

const authStore = useAuthStore()
const shopsStore = useShopsStore()
const { getCurrentCoordinates } = useGps()
const route = useRoute()
const router = useRouter()

const submitting = ref(false)
const locatingPin = ref(false)
const errorMsg = ref('')

const { usePageSeo } = useSeo()
usePageSeo({
  title: 'ເພີ່ມຮ້ານສ້ອມແປງ ແລະ ປັກໝຸດທີ່ຕັ້ງຮ້ານຟຣີເທິງແຜນທີ່ — Search-Want',
  description:
    'ເຈົ້າຂອງອູ່ລົດ, ຮ້ານສ້ອມແປງ ຫຼື ຊ່າງບໍລິການ ສາມາດລົງທະບຽນເພີ່ມຮ້ານ ແລະ ປັກໝຸດ GPS ເທິງແຜນທີ່ Search-Want ຟຣີ ເພື່ອໃຫ້ລູກຄ້າໃກ້ຄຽງຄົ້ນຫາພົບ ແລະ ໂທຫາໄດ້ທັນທີ.',
  path: '/shops/add',
  keywords: 'ເພີ່ມຮ້ານຟຣີ, ປັກໝຸດຮ້ານເທິງແຜນທີ່, ລົງທະບຽນຮ້ານສ້ອມແປງ, Search-Want',
})

const form = reactive({
  category_id: 1,
  name: '',
  description: '',
  problem_tags: '',
  phone: '',
  address: '',
  latitude: shopsStore.userLat,
  longitude: shopsStore.userLng,
  opening_hours: '08:00 - 18:00',
  is_emergency_24h: false,
})

const suggestedTags = [
  'ລົດສະຕາດບໍ່ຕິດ',
  'ເຄື່ອງຈັກມີສຽງດັງ',
  'ຢາງລົດແບນ',
  'ແບັດເຕີຣີ້ໝົດ',
  'ຕ້ອງການລົດລາກດ່ວນ',
  'ໜ້າຈໍແຕກ',
  'ທໍ່ນ້ຳຮົ່ວ',
  'ແອເຢັນບໍ່ເຢັນ',
]

function appendTag(tag: string) {
  const existing = form.problem_tags
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
  if (!existing.includes(tag)) {
    existing.push(tag)
    form.problem_tags = existing.join(', ')
  }
}

function updatePickedCoords(coords: { lat: number; lng: number }) {
  form.latitude = coords.lat
  form.longitude = coords.lng
}

async function pinAtMyCurrentGps() {
  locatingPin.value = true
  try {
    const res = await getCurrentCoordinates()
    if (res.ok && res.lat !== undefined && res.lng !== undefined) {
      form.latitude = res.lat
      form.longitude = res.lng
      authStore.showToast('ປັກໝຸດຕາມ GPS ປັດຈຸບັນແລ້ວ!', 'success', 'mdi-crosshairs-gps')
    } else if (res.reason !== 'insecure_origin' && res.messageLao) {
      authStore.showToast(res.messageLao, 'warning', 'mdi-map-marker-alert-outline')
    }
  } finally {
    locatingPin.value = false
  }
}

async function handleSubmitShop() {
  errorMsg.value = ''
  if (!form.name.trim() || !form.description.trim() || !form.phone.trim() || !form.address.trim()) {
    errorMsg.value = 'ກະລຸນາຕື່ມຂໍ້ມູນຮ້ານທີ່ມີເຄື່ອງໝາຍ * ໃຫ້ຄົບຖ້ວນ.'
    return
  }
  submitting.value = true
  try {
    const created = await shopsStore.submitShop({ ...form })
    authStore.showToast(
      `ສົ່ງ "${created.name}" ແລ້ວ! ລໍຖ້າການອະນຸມັດຈາກຜູ້ດູແລລະບົບ.`,
      'success',
      'mdi-clock-check-outline',
    )
    router.push('/shops/mine')
  } catch (err: any) {
    errorMsg.value = err?.data?.detail || 'ສົ່ງຮ້ານບໍ່ສຳເລັດ. ກະລຸນາກວດສອບຂໍ້ມູນ.'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  if (shopsStore.categories.length === 0) {
    await shopsStore.loadCategoriesAndSymptoms()
  }
  if (shopsStore.categories.length > 0) {
    form.category_id = shopsStore.categories[0].id
  }
  form.latitude = shopsStore.userLat
  form.longitude = shopsStore.userLng
  if (route.query.autoGps === '1') {
    router.replace({ query: { ...route.query, autoGps: undefined } })
    await pinAtMyCurrentGps()
  }
})
</script>
