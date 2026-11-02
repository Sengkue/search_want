const backendOrigin = (
  process.env.BACKEND_INTERNAL_URL ||
  process.env.NUXT_PUBLIC_API_BASE ||
  'http://127.0.0.1:8000'
).replace(/\/$/, '')

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2026-10-30',
  // Full SSR enabled by default for instant First Contentful Paint & Google Top Search SEO;
  // Capacitor Android APK builder sets NUXT_SSR=false automatically during `nuxt generate`.
  ssr: process.env.NUXT_SSR !== 'false',
  devtools: { enabled: false },

  modules: ['@pinia/nuxt'],

  // Leaflet CSS moved into ShopMap.client.vue and @mdi/font replaced with tree-shaken @mdi/js SVGs (saves 714 KB!)
  css: [
    '~/assets/css/lao-font.css',
    'vuetify/styles',
    '~/assets/css/main.css',
  ],

  features: {
    // Avoid duplicating 200+ KB of Vuetify styles inline inside SSR HTML when entry.css is already cached
    inlineStyles: false,
  },

  build: {
    transpile: ['vuetify'],
  },

  experimental: {
    payloadExtraction: true,
  },

  vite: {
    build: {
      cssCodeSplit: true,
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules/leaflet')) {
              return 'leaflet-vendor'
            }
          },
        },
      },
    },
  },

  runtimeConfig: {
    public: {
      siteUrl: process.env.NUXT_PUBLIC_SITE_URL || '',
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '',
      httpsPort: process.env.NUXT_PUBLIC_HTTPS_PORT || '3443',
      adsenseClientId: process.env.NUXT_PUBLIC_ADSENSE_CLIENT_ID || 'ca-pub-4990570878383229',
      adsenseSlotInfeed: process.env.NUXT_PUBLIC_ADSENSE_SLOT_INFEED || '6642734194',
      adsenseSlotBanner: process.env.NUXT_PUBLIC_ADSENSE_SLOT_BANNER || '8750022785',
    },
  },

  nitro: {
    compressPublicAssets: {
      gzip: true,
      brotli: true,
    },
    devProxy: {
      '/api': {
        target: `${backendOrigin}/api`,
        changeOrigin: true,
      },
      '/ads.txt': {
        target: `${backendOrigin}/ads.txt`,
        changeOrigin: true,
      },
    },
    routeRules: {
      '/api/**': {
        proxy: `${backendOrigin}/api/**`,
      },
      '/ads.txt': {
        proxy: `${backendOrigin}/ads.txt`,
      },
      '/_nuxt/**': {
        headers: {
          'Cache-Control': 'public, max-age=31536000, immutable',
        },
      },
      '/fonts/**': {
        headers: {
          'Cache-Control': 'public, max-age=31536000, immutable',
        },
      },
      '/app-icon-96.webp': {
        headers: {
          'Cache-Control': 'public, max-age=31536000, immutable',
        },
      },
      '/app-icon.png': {
        headers: {
          'Cache-Control': 'public, max-age=604800',
        },
      },
      '/admin/**': {
        headers: {
          'X-Robots-Tag': 'noindex, nofollow',
        },
      },
      '/shops/mine': {
        headers: {
          'X-Robots-Tag': 'noindex, nofollow',
        },
      },
      '/login': {
        headers: {
          'X-Robots-Tag': 'noindex, nofollow',
        },
      },
    },
  },

  app: {
    head: {
      htmlAttrs: { lang: 'lo' },
      title: 'Search-Want — ຄົ້ນຫາຮ້ານສ້ອມແປງ ແລະ ຊ່າງໃກ້ຄຽງຈາກບັນຫາຂອງທ່ານ',
      meta: [
        { charset: 'utf-8' },
        {
          name: 'viewport',
          content: 'width=device-width, initial-scale=1, viewport-fit=cover',
        },
        {
          name: 'description',
          content:
            'ມີບັນຫາລົດເສຍ, ລົດສະຕາດບໍ່ຕິດ, ຢາງລົດແບນ, ໂທລະສັບຈໍແຕກ, ທໍ່ນ້ຳຮົ່ວ ຫຼື ແອບໍ່ເຢັນ? ຄົ້ນຫາຊ່າງ ແລະ ຮ້ານສ້ອມແປງທີ່ອະນຸມັດແລ້ວໃກ້ຕົວທ່ານເທິງແຜນທີ່ GPS ທັນທີ.',
        },
        { name: 'theme-color', content: '#1A73E8' },
        { name: 'format-detection', content: 'telephone=no' },
        { name: 'geo.region', content: 'LA-VT' },
        { name: 'geo.placename', content: 'Vientiane, Laos' },
        { property: 'og:site_name', content: 'Search-Want' },
        { property: 'og:locale', content: 'lo_LA' },
        { name: 'mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-title', content: 'Search-Want' },
      ],
      link: [
        { rel: 'manifest', href: '/manifest.webmanifest' },
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
        { rel: 'shortcut icon', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
        {
          rel: 'preload',
          as: 'font',
          type: 'font/woff2',
          href: '/fonts/NotoSansLaoLooped-lao.woff2',
          crossorigin: 'anonymous',
        },
        {
          rel: 'preload',
          as: 'font',
          type: 'font/woff2',
          href: '/fonts/NotoSansLaoLooped-latin.woff2',
          crossorigin: 'anonymous',
        },
      ],
    },
  },
})
