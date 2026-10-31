<template>
  <v-dialog v-model="gpsSecureDialogOpen" max-width="390">
    <v-card rounded="xl" class="sw-hero-card pa-4">
      <div class="d-flex align-center justify-space-between mb-2">
        <div class="d-flex align-center ga-2">
          <v-avatar color="primary" size="38" rounded="lg" variant="tonal">
            <v-icon icon="mdi-shield-lock-outline" size="21" />
          </v-avatar>
          <div>
            <div class="text-title-small font-weight-black" style="line-height: 1.2">
              ເປີດໂໝດປອດໄພເພື່ອໃຊ້ GPS
            </div>
            <div class="text-body-small text-primary font-weight-bold">
              ບຣາວເຊີຕ້ອງການ HTTPS ຫຼື localhost
            </div>
          </div>
        </div>
        <v-btn icon="mdi-close" variant="text" size="x-small" @click="gpsSecureDialogOpen = false" />
      </div>

      <p class="text-body-small text-medium-emphasis mb-3">
        ຕອນນີ້ທ່ານເປີດເວັບຜ່ານ <code>{{ currentOrigin }}</code> (HTTP ທຳມະດາ) ເຊິ່ງ Chrome / Safari ຈະບລັອກ GPS ອັດຕະໂນມັດ. ເລືອກ 1 ວິທີດ້ານລຸ່ມເພື່ອໃຊ້ຕຳແໜ່ງທັນທີ:
      </p>

      <!-- Option 1: 1-Tap Switch to HTTPS (:3443) — Works on Phones & PCs over Wi-Fi! -->
      <v-btn
        :href="httpsUrl"
        color="primary"
        variant="flat"
        block
        prepend-icon="mdi-lock-check-outline"
        class="mb-1"
      >
        ເປີດຜ່ານ HTTPS ເພື່ອໃຊ້ GPS ທັນທີ
      </v-btn>
      <div class="text-body-small text-medium-emphasis text-center mb-3" style="font-size: 11px">
        (ຄັ້ງທຳອິດຖ້າບຣາວເຊີຖາມໃບຮັບຮອງ ໃຫ້ກົດ <strong>Advanced &rarr; Proceed</strong>)
      </div>

      <!-- Option 2: 1-Tap Switch to localhost (Instant on the host computer with 0 cert prompt) -->
      <v-btn
        :href="localhostUrl"
        color="secondary"
        variant="tonal"
        size="small"
        block
        prepend-icon="mdi-laptop"
        class="mb-2"
      >
        ເປີດຜ່ານ localhost (ຖ້າໃຊ້ຄອມເຄື່ອງນີ້)
      </v-btn>

      <!-- Option 3: Pick or Drag Pin Directly on Map Right Now (Works Everywhere!) -->
      <v-btn
        color="warning"
        variant="tonal"
        size="small"
        block
        prepend-icon="mdi-map-marker-radius"
        @click="onPickOnMap"
      >
        ແຕະ ຫຼື ລາກໝຸດເທິງແຜນທີ່ເອງດຽວນີ້
      </v-btn>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
const {
  gpsSecureDialogOpen,
  buildSecureHttpsUrl,
  buildLocalhostUrl,
  triggerManualMapPick,
} = useGps()

const currentOrigin = computed(() => {
  if (!import.meta.client) return 'http://...'
  return window.location.origin
})

const httpsUrl = computed(() => buildSecureHttpsUrl())
const localhostUrl = computed(() => buildLocalhostUrl())

function onPickOnMap() {
  triggerManualMapPick()
}
</script>

