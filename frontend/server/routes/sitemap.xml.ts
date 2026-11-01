import { defineEventHandler, getRequestHeader, getRequestURL, setResponseHeader } from 'h3'

function escapeXml(raw: string): string {
  return raw
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;')
}

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const reqUrl = getRequestURL(event)
  const fwdProto = getRequestHeader(event, 'x-forwarded-proto')?.split(',')[0]?.trim()
  const fwdHost = getRequestHeader(event, 'x-forwarded-host')?.split(',')[0]?.trim()

  const configuredSiteUrl = String(config.public.siteUrl || '').trim().replace(/\/$/, '')
  const origin =
    configuredSiteUrl ||
    (fwdHost ? `${fwdProto || reqUrl.protocol.replace(':', '')}://${fwdHost}` : reqUrl.origin)

  const apiOrigin = String(config.public.apiBase || 'http://127.0.0.1:8000').replace(/\/$/, '')
  const today = new Date().toISOString().slice(0, 10)

  const entries: Array<{ loc: string; lastmod: string; changefreq: string; priority: string }> = [
    { loc: `${origin}/`, lastmod: today, changefreq: 'daily', priority: '1.0' },
    { loc: `${origin}/shops/add`, lastmod: today, changefreq: 'monthly', priority: '0.75' },
    { loc: `${origin}/privacy`, lastmod: today, changefreq: 'yearly', priority: '0.40' },
  ]

  try {
    const [categories, nearby] = await Promise.all([
      $fetch<Array<{ id: number }>>(`${apiOrigin}/api/categories`),
      $fetch<{ shops: Array<{ id: number; updated_at?: string }> }>(
        `${apiOrigin}/api/shops/nearby?radius_km=0`,
      ),
    ])

    for (const cat of categories || []) {
      entries.push({
        loc: `${origin}/?category=${cat.id}`,
        lastmod: today,
        changefreq: 'daily',
        priority: '0.85',
      })
    }

    for (const shop of nearby?.shops || []) {
      const lastmod = shop.updated_at ? String(shop.updated_at).slice(0, 10) : today
      entries.push({
        loc: `${origin}/shops/${shop.id}`,
        lastmod,
        changefreq: 'weekly',
        priority: '0.90',
      })
    }
  } catch {
    // Keep core static routes in sitemap even if backend is temporarily restarting
  }

  const xmlItems = entries
    .map(
      (u) =>
        `  <url>\n    <loc>${escapeXml(u.loc)}</loc>\n    <lastmod>${u.lastmod}</lastmod>\n    <changefreq>${u.changefreq}</changefreq>\n    <priority>${u.priority}</priority>\n  </url>`,
    )
    .join('\n')

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${xmlItems}\n</urlset>\n`

  setResponseHeader(event, 'Content-Type', 'application/xml; charset=utf-8')
  setResponseHeader(event, 'Cache-Control', 'public, max-age=1800, s-maxage=1800')
  return xml
})

