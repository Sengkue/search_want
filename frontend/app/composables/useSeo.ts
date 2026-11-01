import { toValue, type MaybeRefOrGetter } from 'vue'

export interface PageSeoOptions {
  title: MaybeRefOrGetter<string>
  description: MaybeRefOrGetter<string>
  path?: MaybeRefOrGetter<string>
  keywords?: MaybeRefOrGetter<string>
  ogType?: 'website' | 'article' | 'profile'
  noindex?: boolean
  jsonLd?: MaybeRefOrGetter<Record<string, any> | Array<Record<string, any>> | null>
}

export function useSeo() {
  const config = useRuntimeConfig()
  const reqUrl = useRequestURL()

  const siteOrigin = computed(() => {
    const explicit = String(config.public.siteUrl || '').trim().replace(/\/$/, '')
    if (explicit) return explicit
    return `${reqUrl.protocol}//${reqUrl.host}`
  })

  function usePageSeo(options: PageSeoOptions) {
    const resolvedTitle = computed(() => toValue(options.title))
    const resolvedDescription = computed(() => toValue(options.description))
    const resolvedKeywords = computed(() => (options.keywords ? toValue(options.keywords) : ''))
    const resolvedCanonical = computed(() => {
      const rawPath = options.path ? toValue(options.path) : reqUrl.pathname
      const cleanPath = rawPath.startsWith('/') ? rawPath : `/${rawPath}`
      return `${siteOrigin.value}${cleanPath}`
    })
    const ogImageUrl = computed(() => `${siteOrigin.value}/icon-512.png`)
    const robotsDirective = options.noindex
      ? 'noindex, nofollow'
      : 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1'

    useSeoMeta({
      title: resolvedTitle,
      description: resolvedDescription,
      keywords: () => resolvedKeywords.value || undefined,
      robots: robotsDirective,
      ogTitle: resolvedTitle,
      ogDescription: resolvedDescription,
      ogType: options.ogType || 'website',
      ogUrl: resolvedCanonical,
      ogImage: ogImageUrl,
      ogSiteName: 'Search-Want',
      ogLocale: 'lo_LA',
      twitterCard: 'summary_large_image',
      twitterTitle: resolvedTitle,
      twitterDescription: resolvedDescription,
      twitterImage: ogImageUrl,
    })

    useHead(() => {
      const ld = options.jsonLd ? toValue(options.jsonLd) : null
      const ldItems = Array.isArray(ld) ? ld.filter(Boolean) : ld ? [ld] : []
      return {
        link: [
          {
            key: 'canonical',
            rel: 'canonical',
            href: resolvedCanonical.value,
          },
        ],
        script: ldItems.map((schemaObj, idx) => ({
          key: `ld-json-${idx}`,
          type: 'application/ld+json',
          innerHTML: JSON.stringify(schemaObj),
        })),
      }
    })
  }

  return {
    siteOrigin,
    usePageSeo,
  }
}

