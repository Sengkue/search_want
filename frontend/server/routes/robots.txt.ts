import { defineEventHandler, getRequestHeader, getRequestURL, setResponseHeader } from 'h3'

export default defineEventHandler((event) => {
  const config = useRuntimeConfig(event)
  const reqUrl = getRequestURL(event)
  const fwdProto = getRequestHeader(event, 'x-forwarded-proto')?.split(',')[0]?.trim()
  const fwdHost = getRequestHeader(event, 'x-forwarded-host')?.split(',')[0]?.trim()

  const configuredSiteUrl = String(config.public.siteUrl || '').trim().replace(/\/$/, '')
  const origin =
    configuredSiteUrl ||
    (fwdHost ? `${fwdProto || reqUrl.protocol.replace(':', '')}://${fwdHost}` : reqUrl.origin)

  const body = [
    '# Search-Want Robots & Google AdSense Crawler Policy',
    'User-agent: Mediapartners-Google',
    'Allow: /',
    '',
    'User-agent: Googlebot',
    'Allow: /',
    'Disallow: /admin/',
    'Disallow: /shops/mine',
    'Disallow: /login',
    'Disallow: /api/',
    '',
    'User-agent: *',
    'Allow: /',
    'Disallow: /admin/',
    'Disallow: /shops/mine',
    'Disallow: /login',
    'Disallow: /api/',
    '',
    `Sitemap: ${origin}/sitemap.xml`,
    '',
  ].join('\n')

  setResponseHeader(event, 'Content-Type', 'text/plain; charset=utf-8')
  setResponseHeader(event, 'Cache-Control', 'public, max-age=86400')
  return body
})

