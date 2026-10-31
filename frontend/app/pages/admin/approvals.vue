<template>
  <v-container class="py-3 py-md-6 px-3" style="max-width: 1280px">
    <!-- Compact Friendly Header -->
    <div class="d-flex flex-wrap align-center justify-space-between ga-2 mb-3">
      <div class="d-flex align-center ga-2">
        <v-avatar color="warning" size="34" rounded="lg" variant="tonal">
          <v-icon icon="mdi-shield-check" size="19" />
        </v-avatar>
        <div>
          <h1 class="text-title-medium text-md-title-large font-weight-black" style="line-height: 1.2">
            ໜ້າຄວບຄຸມການອະນຸມັດຮ້ານ
          </h1>
          <p class="text-body-small text-medium-emphasis mb-0">
            ກວດຕຳແໜ່ງໝຸດທີ່ເຈົ້າຂອງຮ້ານສົ່ງມາ ແລ້ວກົດອະນຸມັດເພື່ອເປີດສະແດງເທິງແຜນທີ່
          </p>
        </div>
      </div>

      <v-btn
        variant="tonal"
        color="primary"
        size="small"
        prepend-icon="mdi-refresh"
        :loading="loading"
        @click="refreshAll"
      >
        ໂຫຼດໃໝ່
      </v-btn>
    </div>

    <!-- Admin Access Guard -->
    <v-card v-if="!authStore.isAdmin" class="pa-6 text-center">
      <v-avatar color="warning" variant="tonal" size="48" class="mb-2">
        <v-icon icon="mdi-shield-lock-outline" size="26" />
      </v-avatar>
      <h2 class="text-title-medium font-weight-bold mb-1">ສະເພາະຜູ້ດູແລລະບົບເທົ່ານັ້ນ</h2>
      <p class="text-body-small text-medium-emphasis mb-3">
        ກະລຸນາເຂົ້າສູ່ລະບົບດ້ວຍບັນຊີຜູ້ດູແລລະບົບ ເພື່ອອະນຸມັດຮ້ານທີ່ລໍຖ້າກວດສອບ
      </p>
      <v-btn to="/login?redirect=/admin/approvals" color="warning" variant="flat" prepend-icon="mdi-login">
        ເຂົ້າສູ່ລະບົບຜູ້ດູແລ
      </v-btn>
    </v-card>

    <template v-else>
      <!-- Compact 4-Card KPI Strip (Fits cleanly without dominating phone screens) -->
      <v-row density="compact" class="mb-3">
        <v-col cols="6" sm="3">
          <v-card class="pa-2 px-3" style="border-left: 4px solid #EA580C !important">
            <div class="text-body-small text-medium-emphasis">ລໍຖ້າອະນຸມັດ</div>
            <div class="text-title-large font-weight-black text-warning">{{ stats.pending_count }}</div>
          </v-card>
        </v-col>
        <v-col cols="6" sm="3">
          <v-card class="pa-2 px-3" style="border-left: 4px solid #16A34A !important">
            <div class="text-body-small text-medium-emphasis">ອະນຸມັດແລ້ວ</div>
            <div class="text-title-large font-weight-black text-success">{{ stats.approved_count }}</div>
          </v-card>
        </v-col>
        <v-col cols="6" sm="3">
          <v-card class="pa-2 px-3" style="border-left: 4px solid #DC2626 !important">
            <div class="text-body-small text-medium-emphasis">ປະຕິເສດ / ຢຸດ</div>
            <div class="text-title-large font-weight-black text-error">
              {{ stats.rejected_count + stats.suspended_count }}
            </div>
          </v-card>
        </v-col>
        <v-col cols="6" sm="3">
          <v-card class="pa-2 px-3" style="border-left: 4px solid #1A73E8 !important">
            <div class="text-body-small text-medium-emphasis">ຜູ້ໃຊ້ທັງໝົດ</div>
            <div class="text-title-large font-weight-black text-primary">{{ stats.total_users }}</div>
          </v-card>
        </v-col>
      </v-row>

      <!-- Compact Moderation Filter Tabs -->
      <v-tabs
        v-model="activeFilter"
        color="primary"
        density="compact"
        show-arrows
        class="mb-3"
        @update:model-value="fetchShopsByFilter"
      >
        <v-tab value="PENDING">
          ລໍຖ້າການກວດສອບ
          <v-chip
            v-if="stats.pending_count > 0"
            size="x-small"
            color="warning"
            variant="flat"
            class="ml-1 font-weight-bold"
          >
            {{ stats.pending_count }}
          </v-chip>
        </v-tab>
        <v-tab value="APPROVED">ອະນຸມັດແລ້ວ ({{ stats.approved_count }})</v-tab>
        <v-tab value="REJECTED">ຖືກປະຕິເສດ ({{ stats.rejected_count }})</v-tab>
        <v-tab value="ALL">ທັງໝົດ</v-tab>
        <v-tab value="LOGS">ປະຫວັດການອະນຸມັດ</v-tab>
      </v-tabs>

      <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-3" />

      <!-- Audit Logs Tab -->
      <v-card v-if="activeFilter === 'LOGS'" class="pa-3 pa-md-4">
        <div class="text-title-small font-weight-bold mb-2">ປະຫວັດການກວດສອບຫຼ້າສຸດ</div>
        <v-list v-if="logs.length > 0" density="compact" lines="two" class="py-0">
          <v-list-item v-for="log in logs" :key="log.id" class="px-1">
            <template #prepend>
              <v-avatar
                :color="log.action === 'APPROVED' ? 'success' : log.action === 'RESUBMITTED' ? 'info' : 'error'"
                size="30"
                variant="tonal"
              >
                <v-icon
                  :icon="log.action === 'APPROVED' ? 'mdi-check-bold' : log.action === 'RESUBMITTED' ? 'mdi-refresh' : 'mdi-close-thick'"
                  size="16"
                />
              </v-avatar>
            </template>
            <v-list-item-title class="text-body-small font-weight-bold">
              ຮ້ານ #{{ log.shop_id }} — {{ logActionLabel(log.action) }} ໂດຍ {{ log.admin_name }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-body-small">
              {{ log.note || 'ບໍ່ມີໝາຍເຫດເພີ່ມເຕີມ' }} • {{ formatDateTime(log.created_at) }}
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>
        <div v-else class="pa-5 text-center text-medium-emphasis text-body-small">
          ຍັງບໍ່ມີປະຫວັດການອະນຸມັດ
        </div>
      </v-card>

      <!-- Shop Review Cards -->
      <template v-else>
        <v-row v-if="adminShops.length > 0" density="compact">
          <v-col v-for="shop in adminShops" :key="shop.id" cols="12" md="6">
            <v-card class="pa-3 pa-md-4 h-100 d-flex flex-column justify-space-between mb-1">
              <div>
                <div class="d-flex align-start justify-space-between ga-2 mb-2">
                  <div class="d-flex align-center ga-2" style="min-width: 0; flex: 1">
                    <v-avatar :color="shop.category_color" size="36" rounded="lg" class="flex-shrink-0">
                      <v-icon :icon="shop.category_icon" color="white" size="18" />
                    </v-avatar>
                    <div style="min-width: 0">
                      <div class="text-title-small font-weight-bold text-truncate">{{ shop.name }}</div>
                      <div class="text-body-small text-medium-emphasis text-truncate">
                        {{ shop.category_name }} • <strong>{{ shop.owner_name }}</strong>
                      </div>
                    </div>
                  </div>

                  <v-chip
                    :color="shop.status === 'APPROVED' ? 'success' : shop.status === 'PENDING' ? 'warning' : 'error'"
                    size="x-small"
                    variant="tonal"
                    class="font-weight-bold flex-shrink-0"
                  >
                    {{ statusLabel(shop.status) }}
                  </v-chip>
                </div>

                <p class="text-body-small sw-clamp-2 mb-2">{{ shop.description }}</p>

                <div class="text-body-small text-medium-emphasis mb-1">
                  📍 {{ shop.address }} ({{ shop.latitude.toFixed(4) }}, {{ shop.longitude.toFixed(4) }})
                </div>
                <div class="text-body-small text-medium-emphasis mb-2">
                  📞 {{ shop.phone }} • 🕒 {{ shop.opening_hours }}
                  <v-chip v-if="shop.is_emergency_24h" size="x-small" color="error" variant="tonal" class="ml-1">
                    24 ຊມ.
                  </v-chip>
                </div>

                <div v-if="shop.problem_tags" class="d-flex flex-wrap ga-1 mb-2">
                  <v-chip
                    v-for="tag in shop.problem_tags.split(',').map((t) => t.trim()).filter(Boolean).slice(0, 4)"
                    :key="tag"
                    size="x-small"
                    variant="tonal"
                    color="secondary"
                  >
                    {{ tag }}
                  </v-chip>
                </div>

                <v-alert
                  v-if="shop.rejection_reason"
                  type="error"
                  variant="tonal"
                  density="compact"
                  class="text-body-small py-1 mb-2"
                >
                  ໝາຍເຫດ: {{ shop.rejection_reason }}
                </v-alert>
              </div>

              <!-- Clean 1-Tap Moderation Footer -->
              <div class="d-flex flex-wrap align-center justify-space-between ga-2 pt-2 border-t">
                <v-btn
                  variant="tonal"
                  color="primary"
                  size="small"
                  prepend-icon="mdi-map-search"
                  @click="openMapPreview(shop)"
                >
                  ເບິ່ງໝຸດແຜນທີ່
                </v-btn>

                <div class="d-flex flex-wrap ga-1">
                  <v-btn
                    v-if="shop.status !== 'APPROVED'"
                    color="success"
                    variant="flat"
                    size="small"
                    prepend-icon="mdi-check-bold"
                    :loading="processingId === shop.id"
                    @click="approveShopNow(shop)"
                  >
                    ອະນຸມັດ
                  </v-btn>

                  <v-btn
                    v-if="shop.status === 'PENDING'"
                    color="error"
                    variant="tonal"
                    size="small"
                    prepend-icon="mdi-close-thick"
                    @click="openRejectDialog(shop, 'REJECT')"
                  >
                    ປະຕິເສດ
                  </v-btn>

                  <v-btn
                    v-if="shop.status === 'APPROVED'"
                    color="warning"
                    variant="tonal"
                    size="small"
                    prepend-icon="mdi-pause-circle-outline"
                    @click="openRejectDialog(shop, 'SUSPEND')"
                  >
                    ຢຸດຊົ່ວຄາວ
                  </v-btn>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-else-if="!loading" class="pa-6 text-center">
          <v-avatar color="success" variant="tonal" size="48" class="mb-2">
            <v-icon icon="mdi-check-all" size="26" />
          </v-avatar>
          <div class="text-title-medium font-weight-bold">ຈັດການຄົບໝົດແລ້ວ!</div>
          <p class="text-body-small text-medium-emphasis mb-0">
            ບໍ່ມີຮ້ານໃນຄິວ <strong>{{ filterLabel(activeFilter) }}</strong> ຕອນນີ້
          </p>
        </v-card>
      </template>
    </template>

    <!-- Map Pin Verification Dialog -->
    <v-dialog v-model="previewDialog" max-width="620">
      <v-card v-if="previewShop" class="pa-4">
        <div class="d-flex align-center justify-space-between mb-2">
          <div style="min-width: 0">
            <div class="text-title-small font-weight-bold text-truncate">{{ previewShop.name }}</div>
            <div class="text-body-small text-medium-emphasis text-truncate">
              {{ previewShop.address }} ({{ previewShop.latitude }}, {{ previewShop.longitude }})
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="x-small" @click="previewDialog = false" />
        </div>

        <div style="height: 300px" class="mb-3">
          <ShopMap
            mode="preview"
            :picker-lat="previewShop.latitude"
            :picker-lng="previewShop.longitude"
            height="300px"
          />
        </div>

        <div class="d-flex flex-wrap justify-space-between align-center ga-2">
          <v-btn
            variant="text"
            color="primary"
            size="small"
            prepend-icon="mdi-open-in-new"
            :href="`https://www.google.com/maps/search/?api=1&query=${previewShop.latitude},${previewShop.longitude}`"
            target="_blank"
          >
            ເປີດໃນ Google Maps
          </v-btn>

          <v-btn
            v-if="previewShop.status !== 'APPROVED'"
            color="success"
            variant="flat"
            size="small"
            prepend-icon="mdi-check-bold"
            :loading="processingId === previewShop.id"
            @click="approveFromPreview"
          >
            ອະນຸມັດຕຳແໜ່ງນີ້
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Reject / Suspend Note Dialog -->
    <v-dialog v-model="rejectDialog" max-width="440">
      <v-card v-if="rejectTargetShop" class="pa-4">
        <div class="text-title-medium font-weight-bold mb-1">
          {{ rejectAction === 'REJECT' ? 'ຂໍໃຫ້ແກ້ໄຂ / ປະຕິເສດຮ້ານ' : 'ຢຸດຊົ່ວຄາວຮ້ານທີ່ເປີດໃຊ້ງານ' }}
        </div>
        <p class="text-body-small text-medium-emphasis mb-3">
          ສົ່ງໝາຍເຫດສັ້ນໆຫາ <strong>{{ rejectTargetShop.owner_name }}</strong> ສຳລັບ <strong>{{ rejectTargetShop.name }}</strong>:
        </p>

        <v-textarea
          v-model="rejectNote"
          label="ໝາຍເຫດເຖິງເຈົ້າຂອງຮ້ານ"
          placeholder="ຕົວຢ່າງ: ກະລຸນາກວດຕຳແໜ່ງໝຸດ ຫຼື ເພີ່ມຈຸດສັງເກດໃຫ້ຊັດເຈນ..."
          rows="2"
        />

        <div class="d-flex justify-end ga-2 mt-1">
          <v-btn variant="text" size="small" @click="rejectDialog = false">ຍົກເລີກ</v-btn>
          <v-btn
            color="error"
            variant="flat"
            size="small"
            :loading="processingId === rejectTargetShop.id"
            @click="confirmRejectOrSuspend"
          >
            ຢືນຢັນ
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
import type { AdminStatsOut, ApprovalLogOut, ShopOut } from '~/types/api'
import { useAuthStore } from '~/stores/auth'
import { useShopsStore } from '~/stores/shops'

const { apiFetch } = useApi()
const { statusLabel, logActionLabel, formatDateTime } = useLabels()
const authStore = useAuthStore()
const shopsStore = useShopsStore()

const loading = ref(false)
const processingId = ref<number | null>(null)
const activeFilter = ref<'PENDING' | 'APPROVED' | 'REJECTED' | 'ALL' | 'LOGS'>('PENDING')

const stats = reactive<AdminStatsOut>({
  pending_count: 0,
  approved_count: 0,
  rejected_count: 0,
  suspended_count: 0,
  total_users: 0,
})

const adminShops = ref<ShopOut[]>([])
const logs = ref<ApprovalLogOut[]>([])

const previewDialog = ref(false)
const previewShop = ref<ShopOut | null>(null)

const rejectDialog = ref(false)
const rejectTargetShop = ref<ShopOut | null>(null)
const rejectAction = ref<'REJECT' | 'SUSPEND'>('REJECT')
const rejectNote = ref('')

function filterLabel(filter: string): string {
  if (filter === 'PENDING') return 'ລໍຖ້າການກວດສອບ'
  if (filter === 'APPROVED') return 'ອະນຸມັດແລ້ວ'
  if (filter === 'REJECTED') return 'ຖືກປະຕິເສດ'
  return 'ທັງໝົດ'
}

async function fetchStats() {
  if (!authStore.isAdmin) return
  const res = await apiFetch<AdminStatsOut>('/api/admin/stats')
  Object.assign(stats, res)
}

async function fetchShopsByFilter() {
  if (!authStore.isAdmin) return
  loading.value = true
  try {
    if (activeFilter.value === 'LOGS') {
      logs.value = await apiFetch<ApprovalLogOut[]>('/api/admin/logs')
    } else {
      const statusParam = activeFilter.value === 'ALL' ? undefined : activeFilter.value
      adminShops.value = await apiFetch<ShopOut[]>('/api/admin/shops', {
        params: { status: statusParam },
      })
    }
  } finally {
    loading.value = false
  }
}

async function refreshAll() {
  await Promise.all([fetchStats(), fetchShopsByFilter(), authStore.fetchNotifications()])
}

function openMapPreview(shop: ShopOut) {
  previewShop.value = shop
  previewDialog.value = true
}

async function approveShopNow(shop: ShopOut) {
  processingId.value = shop.id
  try {
    await apiFetch<ShopOut>(`/api/admin/shops/${shop.id}/decision`, {
      method: 'POST',
      body: {
        action: 'APPROVE',
        note: 'ກວດສອບຕຳແໜ່ງໝຸດ ແລະ ຂໍ້ມູນຮ້ານແລ້ວ.',
      },
    })
    authStore.showToast(
      `ອະນຸມັດ "${shop.name}" ແລ້ວ! ສະແດງເທິງແຜນທີ່ສາທາລະນະທັນທີ.`,
      'success',
      'mdi-check-decagram',
    )
    await shopsStore.loadCategoriesAndSymptoms()
    await refreshAll()
  } catch (err: any) {
    authStore.showToast(err?.data?.detail || 'ການອະນຸມັດບໍ່ສຳເລັດ.', 'error')
  } finally {
    processingId.value = null
  }
}

async function approveFromPreview() {
  if (!previewShop.value) return
  const target = previewShop.value
  await approveShopNow(target)
  previewDialog.value = false
}

function openRejectDialog(shop: ShopOut, action: 'REJECT' | 'SUSPEND') {
  rejectTargetShop.value = shop
  rejectAction.value = action
  rejectNote.value = ''
  rejectDialog.value = true
}

async function confirmRejectOrSuspend() {
  if (!rejectTargetShop.value) return
  const target = rejectTargetShop.value
  processingId.value = target.id
  try {
    await apiFetch<ShopOut>(`/api/admin/shops/${target.id}/decision`, {
      method: 'POST',
      body: {
        action: rejectAction.value,
        note: rejectNote.value.trim() || undefined,
      },
    })
    authStore.showToast(
      rejectAction.value === 'REJECT'
        ? `ສົ່ງຄຳແນະນຳໃຫ້ແກ້ໄຂສຳລັບ "${target.name}" ແລ້ວ.`
        : `ຢຸດຊົ່ວຄາວ "${target.name}" ແລ້ວ.`,
      'info',
    )
    rejectDialog.value = false
    await shopsStore.loadCategoriesAndSymptoms()
    await refreshAll()
  } catch (err: any) {
    authStore.showToast(err?.data?.detail || 'ການດຳເນີນການບໍ່ສຳເລັດ.', 'error')
  } finally {
    processingId.value = null
  }
}

onMounted(async () => {
  await authStore.initAuth()
  if (authStore.isAdmin) {
    await refreshAll()
  }
})
</script>
