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
        <v-tab value="ADSENSE">
          <v-icon icon="mdi-bullhorn-outline" size="16" class="mr-1" />
          ໂຄສະນາ AdSense
        </v-tab>
      </v-tabs>

      <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-3" />

      <!-- Google AdSense Management Tab -->
      <v-card v-if="activeFilter === 'ADSENSE'" class="pa-4 pa-md-5">
        <div class="d-flex flex-wrap align-center justify-space-between ga-2 mb-3">
          <div class="d-flex align-center ga-2">
            <v-avatar color="primary" size="36" rounded="lg" variant="tonal">
              <v-icon icon="mdi-google" size="19" />
            </v-avatar>
            <div>
              <div class="text-title-medium font-weight-bold">ຕັ້ງຄ່າ Google AdSense</div>
              <div class="text-body-small text-medium-emphasis">
                ຈັດການລະຫັດ Publisher ID, Ad Slots ແລະ ໄຟລ໌ /ads.txt ສຳລັບສ້າງລາຍຮັບຈາກໂຄສະນາ
              </div>
            </div>
          </div>

          <v-chip
            :color="!adForm.enabled ? 'default' : adForm.test_mode ? 'warning' : 'success'"
            variant="tonal"
            size="small"
            class="font-weight-bold"
            :prepend-icon="!adForm.enabled ? 'mdi-eye-off-outline' : adForm.test_mode ? 'mdi-flask-outline' : 'mdi-check-decagram'"
          >
            {{
              !adForm.enabled
                ? 'ປິດສະແດງໂຄສະນາຢູ່'
                : adForm.test_mode
                  ? 'ເປີດຢູ່ (ໂໝດທົດລອງ Preview)'
                  : 'ເປີດສະແດງໂຄສະນາຈິງ'
            }}
          </v-chip>
        </div>

        <v-alert
          type="info"
          variant="tonal"
          density="compact"
          rounded="lg"
          class="mb-4 text-body-small"
        >
          <div class="font-weight-bold mb-1">ວິທີເຊື່ອມຕໍ່ Google AdSense 3 ຂັ້ນຕອນງ່າຍໆ:</div>
          <ol class="pl-4 mb-0">
            <li>ສະໝັກບັນຊີທີ່ <strong>google.com/adsense</strong> ແລ້ວສຳເນົາລະຫັດ <code>ca-pub-XXXXXXXXXXXXXXXX</code> ມາໃສ່ລຸ່ມນີ້.</li>
            <li>ສ້າງໜ່ວຍໂຄສະນາ (Display / In-feed Ad Unit) ເພື່ອເອົາເລກ <strong>Slot ID</strong> ມາໃສ່ (ຫຼື ເປີດ Auto Ads).</li>
            <li>ເມື່ອເວັບໄຊອອນລາຍເທິງໂດເມນຈິງ ແລະ Google ອະນຸມັດແລ້ວ ໃຫ້ປິດ <strong>ໂໝດທົດລອງ</strong> ເພື່ອສະແດງໂຄສະນາຈິງທັນທີ! (ໃນແອັບ APK ມືຖື ລະບົບຈະປິດ Web AdSense ອັດຕະໂນມັດຕາມກົດຂອງ Google).</li>
          </ol>
        </v-alert>

        <v-form @submit.prevent="saveAdSenseSettings">
          <v-row density="compact" class="mb-2">
            <v-col cols="12" md="4">
              <v-sheet rounded="lg" border class="pa-3 h-100">
                <v-switch
                  v-model="adForm.enabled"
                  color="success"
                  density="compact"
                  hide-details
                  label="ເປີດໃຊ້ງານ Google AdSense"
                  class="font-weight-bold"
                />
                <div class="text-body-small text-medium-emphasis mt-1">
                  ເປີດ ຫຼື ປິດການສະແດງກ່ອງໂຄສະນາທັງໝົດໃນເວັບໄຊດ້ວຍປຸ່ມດຽວ
                </div>
              </v-sheet>
            </v-col>

            <v-col cols="12" md="4">
              <v-sheet rounded="lg" border class="pa-3 h-100">
                <v-switch
                  v-model="adForm.test_mode"
                  color="warning"
                  density="compact"
                  hide-details
                  label="ໂໝດທົດລອງ (Preview Mode)"
                  class="font-weight-bold"
                />
                <div class="text-body-small text-medium-emphasis mt-1">
                  ສະແດງຕົວຢ່າງກ່ອງໂຄສະນາໃນ localhost / LAN ກ່ອນໂດເມນຈິງອະນຸມັດ
                </div>
              </v-sheet>
            </v-col>

            <v-col cols="12" md="4">
              <v-sheet rounded="lg" border class="pa-3 h-100">
                <v-switch
                  v-model="adForm.auto_ads"
                  color="primary"
                  density="compact"
                  hide-details
                  label="ໂຄສະນາອັດຕະໂນມັດ (Auto Ads)"
                  class="font-weight-bold"
                />
                <div class="text-body-small text-medium-emphasis mt-1">
                  ໂຫຼດສະຄຣິບ AdSense ເພື່ອໃຫ້ Google ຈັດວາງໂຄສະນາອັດຕະໂນມັດ
                </div>
              </v-sheet>
            </v-col>
          </v-row>

          <v-row density="compact" class="mt-1">
            <v-col cols="12" md="4">
              <v-text-field
                v-model="adForm.client_id"
                label="ລະຫັດ Publisher ID"
                placeholder="ca-pub-1234567890123456"
                prepend-inner-icon="mdi-identifier"
                hint="ຮູບແບບ: ca-pub- ຕາມດ້ວຍຕົວເລກ 16 ຫຼັກ (ປະວ່າງໄວ້ໄດ້ໃນໂໝດທົດລອງ)"
                persistent-hint
                clearable
              />
            </v-col>

            <v-col cols="12" md="4">
              <v-text-field
                v-model="adForm.slot_infeed"
                label="In-Feed Ad Slot ID (ແຊກໃນລາຍການຮ້ານ)"
                placeholder="1122334455"
                prepend-inner-icon="mdi-view-stream-outline"
                hint="ສະແດງຫຼັງຮ້ານທີ 2 ແລະ ທຸກໆ 6 ຮ້ານ"
                persistent-hint
                clearable
              />
            </v-col>

            <v-col cols="12" md="4">
              <v-text-field
                v-model="adForm.slot_banner"
                label="Banner Ad Slot ID (ແບນເນີລຸ່ມໜ້າເວັບ)"
                placeholder="6677889900"
                prepend-inner-icon="mdi-page-layout-footer"
                hint="ສະແດງຢູ່ສ່ວນລຸ່ມຂອງໜ້າຄົ້ນຫາ ແລະ ໜ້າຮ້ານຂອງຂ້ອຍ"
                persistent-hint
                clearable
              />
            </v-col>
          </v-row>

          <!-- Automatic /ads.txt Verification Line -->
          <v-sheet rounded="lg" border class="pa-3 mt-3 bg-surface-light">
            <div class="d-flex flex-wrap align-center justify-space-between ga-2 mb-1">
              <div class="text-body-small font-weight-bold d-flex align-center ga-1">
                <v-icon icon="mdi-file-check-outline" size="16" color="primary" />
                <span>ໄຟລ໌ຢືນຢັນໂດເມນອັດຕະໂນມັດ (<code>/ads.txt</code>):</span>
              </div>
              <div class="d-flex ga-1">
                <v-btn
                  size="x-small"
                  variant="tonal"
                  color="primary"
                  prepend-icon="mdi-content-copy"
                  @click="copyAdsTxtLine"
                >
                  ສຳເນົາ
                </v-btn>
                <v-btn
                  size="x-small"
                  variant="text"
                  color="primary"
                  prepend-icon="mdi-open-in-new"
                  href="/ads.txt"
                  target="_blank"
                >
                  ເປີດ /ads.txt
                </v-btn>
              </div>
            </div>
            <code class="text-body-small d-block text-break">{{ previewAdsTxtLine }}</code>
          </v-sheet>

          <div class="d-flex flex-wrap justify-end ga-2 mt-4">
            <v-btn
              to="/"
              variant="tonal"
              color="secondary"
              size="small"
              prepend-icon="mdi-eye-outline"
            >
              ເບິ່ງຕຳແໜ່ງໂຄສະນາໜ້າຫຼັກ
            </v-btn>
            <v-btn
              type="submit"
              color="primary"
              variant="flat"
              size="small"
              :loading="savingAdSense"
              prepend-icon="mdi-content-save-check"
            >
              ບັນທຶກການຕັ້ງຄ່າ AdSense
            </v-btn>
          </div>
        </v-form>
      </v-card>

      <!-- Audit Logs Tab -->
      <v-card v-else-if="activeFilter === 'LOGS'" class="pa-3 pa-md-4">
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
const { adsenseConfig, loadAdSenseConfig, updateAdSenseConfig } = useAdSense()
const authStore = useAuthStore()
const shopsStore = useShopsStore()
const route = useRoute()

const loading = ref(false)
const savingAdSense = ref(false)
const processingId = ref<number | null>(null)
const activeFilter = ref<'PENDING' | 'APPROVED' | 'REJECTED' | 'ALL' | 'LOGS' | 'ADSENSE'>('PENDING')

const adForm = reactive({
  enabled: true,
  client_id: '',
  slot_infeed: '',
  slot_banner: '',
  auto_ads: true,
  test_mode: true,
})

const previewAdsTxtLine = computed(() => {
  const raw = (adForm.client_id || '').trim()
  const pubMatch = raw.match(/^(?:ca-)?(pub-\d{16})$/)
  if (pubMatch) {
    return `google.com, ${pubMatch[1]}, DIRECT, f08c47fec0942fa0`
  }
  return adsenseConfig.value.ads_txt_line || '# Configure Google AdSense Publisher ID (ca-pub-XXXXXXXXXXXXXXXX) in Search-Want Admin Console'
})

function syncAdFormFromConfig() {
  adForm.enabled = adsenseConfig.value.enabled
  adForm.client_id = adsenseConfig.value.client_id || ''
  adForm.slot_infeed = adsenseConfig.value.slot_infeed || ''
  adForm.slot_banner = adsenseConfig.value.slot_banner || ''
  adForm.auto_ads = adsenseConfig.value.auto_ads
  adForm.test_mode = adsenseConfig.value.test_mode
}

async function saveAdSenseSettings() {
  savingAdSense.value = true
  try {
    await updateAdSenseConfig({
      enabled: adForm.enabled,
      client_id: (adForm.client_id || '').trim(),
      slot_infeed: (adForm.slot_infeed || '').trim(),
      slot_banner: (adForm.slot_banner || '').trim(),
      auto_ads: adForm.auto_ads,
      test_mode: adForm.test_mode,
    })
    syncAdFormFromConfig()
    authStore.showToast(
      'ບັນທຶກການຕັ້ງຄ່າ Google AdSense ສຳເລັດແລ້ວ!',
      'success',
      'mdi-check-decagram',
    )
  } catch (err: any) {
    const detail = err?.data?.detail
    const msg = Array.isArray(detail)
      ? detail[0]?.msg || 'ຂໍ້ມູນລະຫັດ AdSense ບໍ່ຖືກຕ້ອງ.'
      : detail || 'ບັນທຶກການຕັ້ງຄ່າ AdSense ບໍ່ສຳເລັດ.'
    authStore.showToast(msg, 'error')
  } finally {
    savingAdSense.value = false
  }
}

async function copyAdsTxtLine() {
  try {
    await navigator.clipboard.writeText(previewAdsTxtLine.value)
    authStore.showToast('ສຳເນົາແຖວ ads.txt ແລ້ວ!', 'success', 'mdi-content-copy')
  } catch {
    authStore.showToast('ບໍ່ສາມາດສຳເນົາອັດຕະໂນມັດໄດ້ ກະລຸນາລາກເລືອກຂໍ້ຄວາມ.', 'warning')
  }
}

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
    if (activeFilter.value === 'ADSENSE') {
      await loadAdSenseConfig(true)
      syncAdFormFromConfig()
    } else if (activeFilter.value === 'LOGS') {
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
  if (route.query.tab === 'ADSENSE') {
    activeFilter.value = 'ADSENSE'
  }
  if (authStore.isAdmin) {
    await loadAdSenseConfig(true)
    syncAdFormFromConfig()
    await refreshAll()
  }
})
</script>
