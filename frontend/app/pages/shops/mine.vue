<template>
  <v-container class="py-3 py-md-6 px-3" style="max-width: 1120px">
    <div class="d-flex flex-wrap align-center justify-space-between ga-2 mb-3">
      <div class="d-flex align-center ga-2">
        <v-avatar color="primary" size="34" rounded="lg" variant="tonal">
          <v-icon icon="mdi-storefront-outline" size="19" />
        </v-avatar>
        <div>
          <h1 class="text-title-medium text-md-title-large font-weight-black" style="line-height: 1.2">
            ຮ້ານຂອງຂ້ອຍທີ່ສົ່ງແລ້ວ
          </h1>
          <p class="text-body-small text-medium-emphasis mb-0">
            ກວດເບິ່ງສະຖານະອະນຸມັດ ຫຼື ແກ້ໄຂຂໍ້ມູນ ແລະ ຕຳແໜ່ງໝຸດຮ້ານຂອງທ່ານ
          </p>
        </div>
      </div>

      <v-btn to="/shops/add" color="primary" variant="flat" size="small" prepend-icon="mdi-plus">
        ເພີ່ມຮ້ານໃໝ່
      </v-btn>
    </div>

    <v-card v-if="!authStore.isLoggedIn" class="pa-6 text-center">
      <p class="text-body-medium mb-3">ກະລຸນາເຂົ້າສູ່ລະບົບເພື່ອເບິ່ງຮ້ານຂອງທ່ານ</p>
      <v-btn to="/login?redirect=/shops/mine" color="primary" variant="flat" prepend-icon="mdi-login">
        ເຂົ້າສູ່ລະບົບ
      </v-btn>
    </v-card>

    <template v-else>
      <v-progress-linear v-if="shopsStore.loadingMyShops" indeterminate color="primary" class="mb-3" />

      <v-row v-if="shopsStore.myShops.length > 0" density="compact">
        <v-col v-for="shop in shopsStore.myShops" :key="shop.id" cols="12" md="6">
          <v-card class="pa-3 pa-md-4 h-100 d-flex flex-column justify-space-between mb-1">
            <div>
              <div class="d-flex align-start justify-space-between ga-2 mb-2">
                <div class="d-flex align-center ga-2" style="min-width: 0; flex: 1">
                  <v-avatar :color="shop.category_color" size="36" rounded="lg" class="flex-shrink-0">
                    <v-icon :icon="shop.category_icon" color="white" size="18" />
                  </v-avatar>
                  <div style="min-width: 0">
                    <div class="text-title-small font-weight-bold text-truncate">{{ shop.name }}</div>
                    <div class="text-body-small text-medium-emphasis text-truncate">{{ shop.category_name }}</div>
                  </div>
                </div>

                <v-chip
                  :color="statusColor(shop.status)"
                  variant="tonal"
                  size="x-small"
                  :prepend-icon="statusIcon(shop.status)"
                  class="font-weight-bold flex-shrink-0"
                >
                  {{ statusLabel(shop.status) }}
                </v-chip>
              </div>

              <v-alert
                v-if="shop.status === 'PENDING'"
                type="warning"
                variant="tonal"
                density="compact"
                class="mb-2 text-body-small py-1"
              >
                ກຳລັງລໍຖ້າຜູ້ດູແລລະບົບອະນຸມັດ — ເມື່ອອະນຸມັດແລ້ວຈະຂຶ້ນແຜນທີ່ທັນທີ
              </v-alert>

              <v-alert
                v-else-if="shop.status === 'APPROVED'"
                type="success"
                variant="tonal"
                density="compact"
                class="mb-2 text-body-small py-1"
              >
                ເປີດສະແດງເທິງແຜນທີ່ສາທາລະນະແລ້ວ!
              </v-alert>

              <v-alert
                v-else-if="shop.status === 'REJECTED' || shop.status === 'SUSPENDED'"
                type="error"
                variant="tonal"
                density="compact"
                class="mb-2 text-body-small py-1"
              >
                <strong>ຄຳແນະນຳຈາກຜູ້ດູແລລະບົບ:</strong>
                {{ shop.rejection_reason || 'ກະລຸນາກວດສອບຂໍ້ມູນແລ້ວສົ່ງຄືນໃໝ່.' }}
              </v-alert>

              <p class="text-body-small text-medium-emphasis sw-clamp-2 mb-1">{{ shop.description }}</p>

              <div class="text-body-small text-medium-emphasis text-truncate">
                📍 {{ shop.address }} • 📞 {{ shop.phone }}
              </div>
            </div>

            <div class="d-flex flex-wrap justify-end ga-2 pt-2 mt-2 border-t">
              <v-btn
                v-if="shop.status === 'APPROVED'"
                to="/"
                variant="text"
                color="primary"
                size="small"
                prepend-icon="mdi-compass-outline"
              >
                ເບິ່ງແຜນທີ່
              </v-btn>
              <v-btn
                v-if="shop.status === 'PENDING' || shop.status === 'REJECTED'"
                variant="text"
                color="error"
                size="small"
                prepend-icon="mdi-delete-outline"
                :loading="deletingId === shop.id"
                @click="confirmDeleteDraftShop(shop)"
              >
                ລຶບຮ້ານ
              </v-btn>
              <v-chip
                v-if="shop.status === 'SUSPENDED' && !authStore.isAdmin"
                color="error"
                variant="tonal"
                size="small"
                prepend-icon="mdi-lock-outline"
              >
                ຖືກລະງັບໂດຍຜູ້ດູແລ
              </v-chip>
              <v-btn
                v-else
                variant="tonal"
                color="primary"
                size="small"
                prepend-icon="mdi-pencil-outline"
                @click="openEditDialog(shop)"
              >
                {{ shop.status === 'REJECTED' ? 'ແກ້ໄຂ ແລະ ສົ່ງຄືນໃໝ່' : 'ແກ້ໄຂຮ້ານ / ໝຸດ' }}
              </v-btn>
            </div>
          </v-card>
        </v-col>
      </v-row>

      <v-card v-else-if="!shopsStore.loadingMyShops" class="pa-6 text-center">
        <v-avatar color="primary" variant="tonal" size="48" class="mb-2">
          <v-icon icon="mdi-store-plus-outline" size="26" />
        </v-avatar>
        <div class="text-title-medium font-weight-bold mb-1">ຍັງບໍ່ມີຮ້ານທີ່ທ່ານສົ່ງ</div>
        <p class="text-body-small text-medium-emphasis mb-3">
          ເພີ່ມຮ້ານ ຫຼື ອູ່ສ້ອມແປງຂອງທ່ານເທິງແຜນທີ່ ເພື່ອໃຫ້ລູກຄ້າໃກ້ຄຽງຄົ້ນຫາພົບ
        </p>
        <v-btn to="/shops/add" color="primary" variant="flat" size="small" prepend-icon="mdi-store-plus">
          ເພີ່ມຮ້ານທຳອິດຂອງຂ້ອຍ
        </v-btn>
      </v-card>
    </template>

    <!-- Responsive Google AdSense Banner for Public/Owner Directory Footer -->
    <AdSenseSlot placement="banner" class="mt-4" />

    <!-- Edit & Resubmit Dialog -->
    <v-dialog v-model="editDialog" max-width="680" scrollable>
      <v-card v-if="editingShop" class="pa-4 pa-md-5">
        <div class="d-flex align-center justify-space-between mb-3">
          <div class="text-title-medium font-weight-bold">ແກ້ໄຂຂໍ້ມູນຮ້ານ &amp; ໝຸດແຜນທີ່</div>
          <v-btn icon="mdi-close" variant="text" size="x-small" @click="editDialog = false" />
        </div>

        <v-card-text class="pa-0">
          <v-text-field v-model="editForm.name" label="ຊື່ຮ້ານ" class="mb-2" />
          <v-select
            v-model="editForm.category_id"
            :items="shopsStore.categories"
            item-title="name"
            item-value="id"
            label="ໝວດໝູ່"
            class="mb-2"
          />
          <v-textarea v-model="editForm.description" label="ລາຍລະອຽດ" rows="2" class="mb-2" />
          <v-text-field
            v-model="editForm.problem_tags"
            label="ບັນຫາ / ອາການທີ່ແກ້ໄຂໄດ້ (ແຍກດ້ວຍເຄື່ອງໝາຍ ,)"
            class="mb-2"
          />
          <v-row density="compact">
            <v-col cols="12" sm="6">
              <v-text-field v-model="editForm.phone" label="ເບີໂທ" />
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="editForm.opening_hours" label="ເວລາເປີດ-ປິດ" />
            </v-col>
          </v-row>
          <v-text-field v-model="editForm.address" label="ທີ່ຢູ່" class="mb-2" />
          <v-switch
            v-model="editForm.is_emergency_24h"
            color="error"
            density="compact"
            label="ບໍລິການສຸກເສີນ 24 ຊມ."
            hide-details
            class="mb-2"
          />

          <div class="mb-2" style="height: 230px">
            <ShopMap
              mode="picker"
              :picker-lat="editForm.latitude"
              :picker-lng="editForm.longitude"
              height="230px"
              @update:picker-location="(c) => { editForm.latitude = c.lat; editForm.longitude = c.lng }"
            />
          </div>
        </v-card-text>

        <v-card-actions class="justify-end pt-2 px-0">
          <v-btn variant="text" size="small" @click="editDialog = false">ຍົກເລີກ</v-btn>
          <v-btn
            color="primary"
            variant="flat"
            size="small"
            :loading="savingEdit"
            prepend-icon="mdi-content-save-check"
            @click="saveEditedShop"
          >
            ບັນທຶກ ແລະ ສົ່ງເພື່ອອະນຸມັດ
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import type { ShopOut } from '~/types/api'
import { useAuthStore } from '~/stores/auth'
import { useShopsStore } from '~/stores/shops'

const { statusLabel } = useLabels()
const authStore = useAuthStore()
const shopsStore = useShopsStore()

const editDialog = ref(false)
const savingEdit = ref(false)
const deletingId = ref<number | null>(null)
const editingShop = ref<ShopOut | null>(null)

const editForm = reactive({
  category_id: 1,
  name: '',
  description: '',
  problem_tags: '',
  phone: '',
  address: '',
  latitude: 17.9757,
  longitude: 102.6331,
  opening_hours: '08:00 - 18:00',
  is_emergency_24h: false,
})

function statusColor(status: string): string {
  if (status === 'APPROVED') return 'success'
  if (status === 'PENDING') return 'warning'
  return 'error'
}

function statusIcon(status: string): string {
  if (status === 'APPROVED') return 'mdi-check-decagram'
  if (status === 'PENDING') return 'mdi-clock-outline'
  return 'mdi-alert-circle-outline'
}

function openEditDialog(shop: ShopOut) {
  editingShop.value = shop
  editForm.category_id = shop.category_id
  editForm.name = shop.name
  editForm.description = shop.description
  editForm.problem_tags = shop.problem_tags
  editForm.phone = shop.phone
  editForm.address = shop.address
  editForm.latitude = shop.latitude
  editForm.longitude = shop.longitude
  editForm.opening_hours = shop.opening_hours
  editForm.is_emergency_24h = shop.is_emergency_24h
  editDialog.value = true
}

async function saveEditedShop() {
  if (!editingShop.value) return
  savingEdit.value = true
  try {
    await shopsStore.updateShop(editingShop.value.id, { ...editForm })
    authStore.showToast(
      authStore.isAdmin
        ? 'ອັບເດດຮ້ານແລ້ວ!'
        : 'ອັບເດດຮ້ານ ແລະ ສົ່ງຄືນເພື່ອຂໍການອະນຸມັດແລ້ວ!',
      'success',
    )
    editDialog.value = false
    await shopsStore.fetchMyShops()
  } catch (err: any) {
    authStore.showToast(err?.data?.detail || 'ອັບເດດຮ້ານບໍ່ສຳເລັດ.', 'error')
  } finally {
    savingEdit.value = false
  }
}

onMounted(async () => {
  await authStore.initAuth()
  if (shopsStore.categories.length === 0) {
    await shopsStore.loadCategoriesAndSymptoms()
  }
  if (authStore.isLoggedIn) {
    await shopsStore.fetchMyShops()
  }
})
</script>
