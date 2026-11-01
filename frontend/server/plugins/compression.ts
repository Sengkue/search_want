import { brotliCompressSync, constants, gzipSync } from 'node:zlib'
import { getRequestHeader, setResponseHeader } from 'h3'

/**
 * Compresses dynamic SSR HTML responses with Brotli or Gzip on Nitro Node Server,
 * reducing initial HTML transfer over mobile Slow 4G by ~85% (e.g. 230 KB -> ~26 KB).
 */
export default defineNitroPlugin((nitroApp) => {
  nitroApp.hooks.hook('render:response', (response, { event }) => {
    const body = response.body
    if (typeof body !== 'string' || body.length < 1024) return

    const existingEncoding = response.headers?.['content-encoding'] || response.headers?.['Content-Encoding']
    if (existingEncoding) return

    const acceptEncoding = getRequestHeader(event, 'accept-encoding') || ''
    if (!acceptEncoding) return

    setResponseHeader(event, 'Vary', 'Accept-Encoding')

    if (acceptEncoding.includes('br')) {
      const compressed = brotliCompressSync(Buffer.from(body, 'utf-8'), {
        params: {
          [constants.BROTLI_PARAM_QUALITY]: 4,
        },
      })
      setResponseHeader(event, 'Content-Encoding', 'br')
      setResponseHeader(event, 'Content-Length', compressed.byteLength)
      response.body = compressed
    } else if (acceptEncoding.includes('gzip')) {
      const compressed = gzipSync(Buffer.from(body, 'utf-8'), { level: 6 })
      setResponseHeader(event, 'Content-Encoding', 'gzip')
      setResponseHeader(event, 'Content-Length', compressed.byteLength)
      response.body = compressed
    }
  })
})

