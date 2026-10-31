// PWA service worker with pre-cached local Lao fonts (/fonts/*.woff2) for instant offline & mobile rendering.
const CACHE_NAME = 'search-want-pwa-v2'
const PRECACHE_FONTS = [
  '/fonts/NotoSansLaoLooped-lao.woff2',
  '/fonts/NotoSansLaoLooped-latin.woff2',
  '/fonts/NotoSansLaoLooped-latin-ext.woff2',
  '/fonts/NotoSansLao-lao.woff2',
  '/fonts/NotoSansLao-latin.woff2',
  '/fonts/NotoSansLao-latin-ext.woff2',
]

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_FONTS))
      .catch(() => {})
      .then(() => self.skipWaiting()),
  )
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  )
})

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return
  const url = new URL(event.request.url)

  // Serve self-hosted Lao fonts cache-first so typography loads in 0ms offline or on slow mobile networks
  if (url.pathname.startsWith('/fonts/')) {
    event.respondWith(
      caches.match(event.request).then(
        (cached) =>
          cached ||
          fetch(event.request).then((resp) => {
            const copy = resp.clone()
            caches.open(CACHE_NAME).then((c) => c.put(event.request, copy))
            return resp
          }),
      ),
    )
    return
  }

  if (url.pathname.startsWith('/_nuxt/') || url.pathname.startsWith('/api/')) return
})
