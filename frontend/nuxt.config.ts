// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2026-10-30',
  ssr: false,
  devtools: { enabled: false },

  modules: ['@pinia/nuxt'],

  css: [
    '~/assets/css/lao-font.css',
    'vuetify/styles',
    '@mdi/font/css/materialdesignicons.css',
    'leaflet/dist/leaflet.css',
    '~/assets/css/main.css',
  ],

  build: {
    transpile: ['vuetify'],
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || '',
      httpsPort: process.env.NUXT_PUBLIC_HTTPS_PORT || '3443',
      adsenseClientId: process.env.NUXT_PUBLIC_ADSENSE_CLIENT_ID || 'ca-pub-4990570878383229',
      adsenseSlotInfeed: process.env.NUXT_PUBLIC_ADSENSE_SLOT_INFEED || '6642734194',
      adsenseSlotBanner: process.env.NUXT_PUBLIC_ADSENSE_SLOT_BANNER || '8750022785',
    },
  },

  nitro: {
    devProxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/api',
        changeOrigin: true,
      },
      '/ads.txt': {
        target: 'http://127.0.0.1:8000/ads.txt',
        changeOrigin: true,
      },
    },
    routeRules: {
      '/api/**': {
        proxy: 'http://127.0.0.1:8000/api/**',
      },
      '/ads.txt': {
        proxy: 'http://127.0.0.1:8000/ads.txt',
      },
    },
  },

  app: {
    head: {
      htmlAttrs: { lang: 'lo' },
      title: 'Search-Want — ຄົ້ນຫາຮ້ານໃກ້ຄຽງຈາກບັນຫາຂອງທ່ານ',
      meta: [
        { charset: 'utf-8' },
        {
          name: 'viewport',
          content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no',
        },
        {
          name: 'description',
          content:
            'ມີບັນຫາກັບລົດ, ໂທລະສັບ ຫຼື ເຮືອນ ແລະ ບໍ່ຮູ້ຈະໄປໃສ? ຄົ້ນຫາຮ້ານທີ່ອະນຸມັດແລ້ວໃກ້ຄຽງເທິງແຜນທີ່ ຫຼື ປັກໝຸດຮ້ານຂອງທ່ານເອງ.',
        },
        { name: 'theme-color', content: '#1A73E8' },
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
