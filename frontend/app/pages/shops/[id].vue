<template>
  <v-container class="py-3 py-md-6 px-3" style="max-width: 1020px">
    <!-- SEO Breadcrumb Navigation -->
    <nav aria-label="Breadcrumb" class="d-flex flex-wrap align-center ga-1 text-body-small text-medium-emphasis mb-3">
      <NuxtLink to="/" class="text-primary text-decoration-none font-weight-medium">
        ໜ້າຫຼັກ Search-Want
      </NuxtLink>
      <v-icon icon="mdi-chevron-right" size="14" />
      <template v-if="shop">
        <NuxtLink
          :to="`/?category=${shop.category_id}`"
          class="text-primary text-decoration-none font-weight-medium"
        >
          {{ shop.category_name }}
        </NuxtLink>
        <v-icon icon="mdi-chevron-right" size="14" />
        <span class="text-high-emphasis font-weight-bold text-truncate">{{ shop.name }}</span>
      </template>
      <span v-else>ລາຍລະອຽດຮ້ານ</span>
    </nav>

    <v-progress-linear v-if="pending" indeterminate color="primary" rounded class="mb-3" />

    <!-- Main Semantic LocalBusiness Profile Article -->
    <v-card v-if="shop" tag="article" class="sw-hero-card pa-4 pa-md-6 mb-4">
      <div class="d-flex flex-wrap align-start justify-space-between ga-3 mb-3">
        <div class="d-flex align-start ga-3" style="min-width: 0; flex: 1">
          <v-avatar :color="shop.category_color || 'primary'" size="52" rounded="xl" class="flex-shrink-0">
            <v-icon :icon="shop.category_icon || 'mdi-store-marker'" color="white" size="26" />
          </v-avatar>

          <div style="min-width: 0">
            <div class="d-flex flex-wrap align-center ga-2 mb-1">
              <v-chip
                size="small"
                :color="shop.category_color || 'primary'"
                variant="flat"
                :prepend-icon="shop.category_icon"
                class="text-white font-weight-bold"
              >
                {{ shop.category_name }}
              </v-chip>
              <v-chip
                v-if="shop.is_emergency_24h"
                color="error"
                size="small"
                variant="flat"
                prepend-icon="mdi-alarm-light-outline"
                class="font-weight-bold"
              >
                ບໍລິການສຸກເສີນ 24 ຊົ່ວໂມງ
              </v-chip>
              <v-chip
                color="success"
                size="small"
                variant="tonal"
                prepend-icon="mdi-check-decagram"
                class="font-weight-bold"
              >
                ຮ້ານຜ່ານການອະນຸມັດແລ້ວ
              </v-chip>
            </div>

            <h1 class="text-headline-small text-md-headline-medium font-weight-black mb-1" style="line-height: 1.3">
              {{ shop.name }}
            </h1>
            <div class="text-body-medium text-medium-emphasis">
              ເວລາເປີດບໍລິການ: <strong>{{ shop.opening_hours }}</strong>
            </div>
          </div>
        </div>

        <!-- Primary 1-Tap Call & Directions Actions -->
        <div class="d-flex flex-wrap ga-2">
          <v-btn
            color="success"
            variant="flat"
            prepend-icon="mdi-phone"
            :href="`tel:${shop.phone}`"
          >
            ໂທ {{ shop.phone }}
          </v-btn>
          <v-btn
            color="primary"
            variant="flat"
            prepend-icon="mdi-directions"
            :href="directionsUrl"
            target="_blank"
            rel="noopener"
          >
            ນຳທາງ Google Maps
          </v-btn>
        </div>
      </div>

      <v-divider class="my-3" />

      <v-row density="comfortable">
        <v-col cols="12" md="6">
          <h2 class="text-title-medium font-weight-bold mb-2">
            ລາຍລະອຽດບໍລິການ ແລະ ການສ້ອມແປງ
          </h2>
          <p class="text-body-medium mb-3" style="line-height: 1.65">
            {{ shop.description }}
          </p>

          <v-sheet rounded="lg" class="pa-3 mb-3 border" color="background">
            <div class="d-flex align-start ga-2 mb-2">
              <v-icon icon="mdi-map-marker" color="error" size="18" class="mt-1 flex-shrink-0" />
              <div>
                <div class="text-body-small text-medium-emphasis">ທີ່ຢູ່ຮ້ານ</div>
                <div class="text-body-medium font-weight-bold">{{ shop.address }}</div>
                <div class="text-body-small text-medium-emphasis">
                  ພິກັດ GPS: {{ shop.latitude.toFixed(5) }}, {{ shop.longitude.toFixed(5) }}
                </div>
              </div>
            </div>

            <div class="d-flex align-start ga-2">
              <v-icon icon="mdi-phone-in-talk-outline" color="success" size="18" class="mt-1 flex-shrink-0" />
              <div>
                <div class="text-body-small text-medium-emphasis">ເບີໂທຕິດຕໍ່ໂດຍກົງ</div>
                <a :href="`tel:${shop.phone}`" class="text-body-medium font-weight-bold text-primary text-decoration-none">
                  {{ shop.phone }}
                </a>
              </div>
            </div>
          </v-sheet>

          <!-- Crawlable Internal Topic Links for Every Problem Tag -->
          <div v-if="allTags.length" class="mb-2">
            <h2 class="text-title-small font-weight-bold mb-2">
              ອາການ ແລະ ບັນຫາທີ່ຮ້ານນີ້ຮັບແກ້ໄຂ:
            </h2>
            <div class="d-flex flex-wrap ga-1">
              <v-chip
                v-for="tag in allTags"
                :key="tag"
                size="small"
                color="primary"
                variant="tonal"
                :to="`/?q=${encodeURIComponent(tag)}`"
                prepend-icon="mdi-wrench-check-outline"
              >
                {{ tag }}
              </v-chip>
            </div>
          </div>
        </v-col>

        <v-col cols="12" md="6">
          <h2 class="text-title-medium font-weight-bold mb-2">
            ແຜນທີ່ຕຳແໜ່ງຮ້ານ
          </h2>
          <v-card class="pa-1 border" style="height: 295px">
            <ClientOnly>
              <ShopMap
                mode="preview"
                :picker-lat="shop.latitude"
                :picker-lng="shop.longitude"
                height="100%"
              />
              <template #fallback>
                <div class="d-flex align-center justify-center h-100 text-body-small text-medium-emphasis">
                  ກຳລັງໂຫຼດແຜນທີ່ {{ shop.name }}...
                </div>
              </template>
            </ClientOnly>
          </v-card>
        </v-col>
      </v-row>

      <div class="d-flex flex-wrap align-center justify-space-between ga-2 mt-4 pt-3 border-t">
        <v-btn
          :to="`/?category=${shop.category_id}`"
          variant="tonal"
          color="primary"
          size="small"
          :prepend-icon="shop.category_icon || 'mdi-magnify'"
        >
          ເບິ່ງຮ້ານອື່ນໃນໝວດ {{ shop.category_name }}
        </v-btn>

        <v-btn
          to="/"
          variant="text"
          color="primary"
          size="small"
          prepend-icon="mdi-arrow-left"
        >
          ກັບໄປໜ້າຄົ້ນຫາຮ້ານໃກ້ຄຽງ
        </v-btn>
      </div>
    </v-card>

    <!-- Not Found Fallback -->
    <v-card v-else-if="!pending" class="pa-6 text-center">
      <v-avatar color="warning" variant="tonal" size="52" class="mb-2">
        <v-icon icon="mdi-store-alert-outline" size="28" />
      </v-avatar>
      <h1 class="text-title-large font-weight-bold mb-1">
        ບໍ່ພົບຂໍ້ມູນຮ້ານນີ້ ຫຼື ກຳລັງລໍຖ້າການອະນຸມັດ
      </h1>
      <p class="text-body-medium text-medium-emphasis mb-4">
        ກະລຸນາກັບໄປໜ້າຫຼັກ ເພື່ອຄົ້ນຫາຮ້ານສ້ອມແປງທີ່ອະນຸມັດແລ້ວໃກ້ຕົວທ່ານ.
      </p>
      <v-btn to="/" color="primary" variant="flat" prepend-icon="mdi-compass-outline">
        ຄົ້ນຫາຮ້ານໃກ້ຄຽງທັງໝົດ
      </v-btn>
    </v-card>

    <ClientOnly>
      <LazyAdSenseSlot placement="banner" :variant-index="1" class="mt-3" />
    </ClientOnly>
  </v-container>
</template>

<script setup lang="ts">
import type { ShopOut } from '~/types/api'

const route = useRoute()
const { apiFetch } = useApi()
const { siteOrigin, usePageSeo } = useSeo()

const shopId = computed(() => String(route.params.id || '').trim())

const { data: shop, pending } = await useAsyncData<ShopOut | null>(
  () => `sw-shop-detail-${shopId.value}`,
  async () => {
    if (!shopId.value || !/^\d+$/.test(shopId.value)) return null
    try {
      return await apiFetch<ShopOut>(`/api/shops/${shopId.value}`)
    } catch {
      return null
    }
  },
  { watch: [shopId] },
)

const allTags = computed(() =>
  (shop.value?.problem_tags || '')
    .split(',')
    .map((t) => t.trim())
    .filter(Boolean),
)

const directionsUrl = computed(() => {
  if (!shop.value) return 'https://www.google.com/maps'
  return `https://www.google.com/maps/dir/?api=1&destination=${shop.value.latitude},${shop.value.longitude}`
})

usePageSeo({
  title: () =>
    shop.value
      ? `${shop.value.name} (${shop.value.category_name}) — ໂທ ${shop.value.phone} | Search-Want`
      : 'ລາຍລະອຽດຮ້ານສ້ອມແປງ — Search-Want',
  description: () =>
    shop.value
      ? `${shop.value.name} — ${shop.value.category_name} ທີ່ ${shop.value.address}. ${shop.value.description} ເປີດ ${shop.value.opening_hours}${shop.value.is_emergency_24h ? ' (ບໍລິການສຸກເສີນ 24 ຊມ.)' : ''} ໂທ: ${shop.value.phone}.`
      : 'ຄົ້ນຫາຮ້ານສ້ອມແປງ ແລະ ຊ່າງທີ່ອະນຸມັດແລ້ວໃກ້ຕົວທ່ານເທິງແຜນທີ່ Search-Want.',
  path: () => `/shops/${shopId.value}`,
  keywords: () =>
    shop.value
      ? [shop.value.name, shop.value.category_name, shop.value.address, ...allTags.value].join(', ')
      : 'ຮ້ານສ້ອມແປງ, Search-Want',
  ogType: 'article',
  jsonLd: () => {
    if (!shop.value) return null
    const s = shop.value
    const shopUrl = `${siteOrigin.value}/shops/${s.id}`
    return [
      {
        '@context': 'https://schema.org',
        '@type': 'LocalBusiness',
        '@id': `${shopUrl}#business`,
        name: s.name,
        description: s.description,
        url: shopUrl,
        telephone: s.phone,
        openingHours: s.opening_hours,
        image: `${siteOrigin.value}/icon-512.png`,
        address: {
          '@type': 'PostalAddress',
          streetAddress: s.address,
          addressLocality: 'Vientiane',
          addressCountry: 'LA',
        },
        geo: {
          '@type': 'GeoCoordinates',
          latitude: s.latitude,
          longitude: s.longitude,
        },
        knowsAbout: allTags.value,
      },
      {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        itemListElement: [
          {
            '@type': 'ListItem',
            position: 1,
            name: 'ໜ້າຫຼັກ Search-Want',
            item: `${siteOrigin.value}/`,
          },
          {
            '@type': 'ListItem',
            position: 2,
            name: s.category_name,
            item: `${siteOrigin.value}/?category=${s.category_id}`,
          },
          {
            '@type': 'ListItem',
            position: 3,
            name: s.name,
            item: shopUrl,
          },
        ],
      },
    ]
  },
})
</script>

