<template>
  <v-card
    tag="article"
    class="sw-card-hover sw-shop-card pa-3 pa-md-4 mb-2"
    :style="{
      border: selected ? '1.8px solid #1A73E8' : undefined,
      cursor: 'pointer',
    }"
    @click="$emit('select', shop.id)"
  >
    <!-- Top Row: Icon + Semantic H2 Crawl Link + Distance Pill -->
    <div class="d-flex align-start justify-space-between ga-2">
      <div class="d-flex align-center ga-2" style="min-width: 0; flex: 1">
        <v-avatar
          :color="shop.category_color || 'primary'"
          size="36"
          rounded="lg"
          class="flex-shrink-0"
        >
          <v-icon :icon="shop.category_icon || 'mdi-store-marker'" color="white" size="18" />
        </v-avatar>

        <div style="min-width: 0">
          <div class="d-flex flex-wrap align-center ga-1">
            <h2 class="text-title-small font-weight-bold text-truncate mb-0" style="line-height: 1.35">
              <NuxtLink
                :to="`/shops/${shop.id}`"
                class="sw-shop-title-link"
                @click.stop
              >
                {{ shop.name }}
              </NuxtLink>
            </h2>
            <v-chip
              v-if="shop.is_emergency_24h"
              color="error"
              size="x-small"
              variant="flat"
              class="font-weight-bold"
            >
              24 ຊມ. ສຸກເສີນ
            </v-chip>
          </div>
          <div class="text-body-small text-medium-emphasis text-truncate">
            {{ shop.category_name }} • {{ shop.opening_hours }}
          </div>
        </div>
      </div>

      <v-chip
        v-if="shop.distance_km !== null && shop.distance_km !== undefined"
        color="primary"
        variant="tonal"
        size="x-small"
        prepend-icon="mdi-map-marker-distance"
        class="font-weight-bold flex-shrink-0"
      >
        {{ shop.distance_km }} ກມ.
      </v-chip>
    </div>

    <!-- Matched Symptom Badges (only when problem search matched) -->
    <div v-if="shop.matched_reasons?.length" class="d-flex flex-wrap ga-1 mt-2">
      <v-chip
        v-for="(reason, idx) in shop.matched_reasons.slice(0, 2)"
        :key="idx"
        color="success"
        variant="tonal"
        size="x-small"
        prepend-icon="mdi-check-circle-outline"
      >
        {{ reason }}
      </v-chip>
    </div>

    <!-- Clamped 2-line Description + Address -->
    <p class="text-body-small text-medium-emphasis sw-clamp-2 mt-2 mb-1">
      {{ shop.description }}
    </p>

    <div class="text-body-small d-flex align-center ga-1 text-medium-emphasis mb-2">
      <v-icon icon="mdi-map-marker-outline" size="14" color="error" class="flex-shrink-0" />
      <span class="text-truncate">{{ shop.address }}</span>
    </div>

    <!-- Compact Problem Tags (top 4) -->
    <div v-if="tagList.length" class="d-flex flex-wrap ga-1 mb-2">
      <v-chip
        v-for="tag in tagList"
        :key="tag"
        size="x-small"
        variant="tonal"
        color="secondary"
      >
        {{ tag }}
      </v-chip>
    </div>

    <!-- Clean Action Footer -->
    <div class="d-flex align-center justify-space-between ga-1 pt-2 border-t" @click.stop>
      <div class="d-flex align-center ga-1">
        <v-btn
          variant="text"
          color="primary"
          size="small"
          prepend-icon="mdi-crosshairs-gps"
          class="px-2"
          @click="$emit('focus-map', shop.id)"
        >
          ເບິ່ງແຜນທີ່
        </v-btn>
        <v-btn
          variant="text"
          color="secondary"
          size="small"
          :to="`/shops/${shop.id}`"
          class="px-2"
        >
          ລາຍລະອຽດ
        </v-btn>
      </div>

      <div class="d-flex ga-1">
        <v-btn
          variant="tonal"
          color="success"
          size="small"
          prepend-icon="mdi-phone"
          :href="`tel:${shop.phone}`"
        >
          ໂທ
        </v-btn>
        <v-btn
          variant="flat"
          color="primary"
          size="small"
          prepend-icon="mdi-directions"
          :href="directionsUrl"
          target="_blank"
          rel="noopener"
        >
          ນຳທາງ
        </v-btn>
      </div>
    </div>
  </v-card>
</template>

<script setup lang="ts">
import type { ShopOut } from '~/types/api'

const props = defineProps<{
  shop: ShopOut
  selected?: boolean
  userLat?: number
  userLng?: number
}>()

defineEmits<{
  (e: 'select', shopId: number): void
  (e: 'focus-map', shopId: number): void
}>()

const tagList = computed(() =>
  (props.shop.problem_tags || '')
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean)
    .slice(0, 4),
)

const directionsUrl = computed(() => {
  const dest = `${props.shop.latitude},${props.shop.longitude}`
  if (props.userLat !== undefined && props.userLng !== undefined) {
    return `https://www.google.com/maps/dir/?api=1&origin=${props.userLat},${props.userLng}&destination=${dest}`
  }
  return `https://www.google.com/maps/dir/?api=1&destination=${dest}`
})
</script>
