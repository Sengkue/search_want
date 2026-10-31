#!/usr/bin/env node
/**
 * Local & Wi-Fi LAN HTTPS Reverse Proxy (https://0.0.0.0:3443 -> http://127.0.0.1:3000)
 *
 * Browsers block `navigator.geolocation` on plain `http://<LAN-IP>:3000` ("Only secure origins are allowed").
 * Running this lightweight HTTPS gateway alongside `npm run dev` gives phones & laptops on Wi-Fi
 * a true Secure Context (`window.isSecureContext === true`) at `https://<LAN-IP>:3443` while Nuxt
 * proxies `/api/**` -> FastAPI `:8000` on the same origin (zero Mixed-Content errors!).
 */
import { spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import http from 'node:http'
import https from 'node:https'
import net from 'node:net'
import os from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const certDir = join(root, '.certs')
const keyPath = join(certDir, 'dev-key.pem')
const certPath = join(certDir, 'dev-cert.pem')
const metaPath = join(certDir, 'san-ips.txt')

const HTTPS_PORT = Number(process.env.HTTPS_PORT || 3443)
const TARGET_HOST = '127.0.0.1'
const TARGET_PORT = Number(process.env.TARGET_PORT || 3000)

function getLanIps() {
  const ips = new Set(['127.0.0.1'])
  const nets = os.networkInterfaces()
  for (const list of Object.values(nets)) {
    for (const iface of list || []) {
      if (iface.family === 'IPv4' && !iface.internal) {
        ips.add(iface.address)
      }
    }
  }
  return Array.from(ips).sort()
}

function findOpenSsl() {
  const candidates = [
    'C:\\Program Files\\Git\\usr\\bin\\openssl.exe',
    'C:\\Program Files (x86)\\Git\\usr\\bin\\openssl.exe',
    'openssl',
  ]
  for (const bin of candidates) {
    if (bin === 'openssl' || existsSync(bin)) {
      const check = spawnSync(bin, ['version'], { encoding: 'utf8' })
      if (check.status === 0) return bin
    }
  }
  throw new Error('OpenSSL binary not found to generate local HTTPS certificate.')
}

function ensureCertificate(ips) {
  mkdirSync(certDir, { recursive: true })
  const sanSignature = ips.join(',')
  if (
    existsSync(keyPath) &&
    existsSync(certPath) &&
    existsSync(metaPath) &&
    readFileSync(metaPath, 'utf8').trim() === sanSignature
  ) {
    return
  }

  const openssl = findOpenSsl()
  const sanEntries = ['DNS:localhost', ...ips.map((ip) => `IP:${ip}`)].join(',')
  const cnfPath = join(certDir, 'openssl-san.cnf')
  writeFileSync(
    cnfPath,
    [
      '[req]',
      'distinguished_name = req_distinguished_name',
      'x509_extensions = v3_req',
      'prompt = no',
      '[req_distinguished_name]',
      'CN = Search-Want Local HTTPS',
      'O = Search-Want Dev',
      '[v3_req]',
      'keyUsage = critical, digitalSignature, keyEncipherment',
      'extendedKeyUsage = serverAuth',
      `subjectAltName = ${sanEntries}`,
      '',
    ].join('\n'),
    'utf8',
  )

  const res = spawnSync(
    openssl,
    [
      'req',
      '-x509',
      '-nodes',
      '-days',
      '825',
      '-newkey',
      'rsa:2048',
      '-keyout',
      keyPath,
      '-out',
      certPath,
      '-config',
      cnfPath,
    ],
    { stdio: 'inherit' },
  )
  if (res.status !== 0) {
    throw new Error('Failed to generate self-signed HTTPS certificate via OpenSSL.')
  }
  writeFileSync(metaPath, sanSignature, 'utf8')
}

const ips = getLanIps()
ensureCertificate(ips)

const server = https.createServer(
  {
    key: readFileSync(keyPath),
    cert: readFileSync(certPath),
  },
  (clientReq, clientRes) => {
    const proxyReq = http.request(
      {
        hostname: TARGET_HOST,
        port: TARGET_PORT,
        path: clientReq.url,
        method: clientReq.method,
        headers: {
          ...clientReq.headers,
          'x-forwarded-proto': 'https',
          'x-forwarded-host': clientReq.headers.host || '',
        },
      },
      (proxyRes) => {
        clientRes.writeHead(proxyRes.statusCode || 502, proxyRes.headers)
        proxyRes.pipe(clientRes, { end: true })
      },
    )

    proxyReq.on('error', (err) => {
      if (!clientRes.headersSent) {
        clientRes.writeHead(502, { 'Content-Type': 'text/plain; charset=utf-8' })
      }
      clientRes.end(`Nuxt dev server on port ${TARGET_PORT} is starting up (${err.message}). Please refresh in a moment.`)
    })

    clientReq.pipe(proxyReq, { end: true })
  },
)

// Forward Vite HMR & WebSocket upgrades cleanly
server.on('upgrade', (req, clientSocket, head) => {
  const targetSocket = net.connect(TARGET_PORT, TARGET_HOST, () => {
    const reqLines = [`${req.method} ${req.url} HTTP/${req.httpVersion}`]
    for (let i = 0; i < req.rawHeaders.length; i += 2) {
      reqLines.push(`${req.rawHeaders[i]}: ${req.rawHeaders[i + 1]}`)
    }
    reqLines.push('', '')
    targetSocket.write(reqLines.join('\r\n'))
    if (head && head.length) targetSocket.write(head)
    clientSocket.pipe(targetSocket)
    targetSocket.pipe(clientSocket)
  })

  targetSocket.on('error', () => clientSocket.destroy())
  clientSocket.on('error', () => targetSocket.destroy())
})

server.listen(HTTPS_PORT, '0.0.0.0', () => {
  console.log(`\n🔒 Search-Want Secure HTTPS Gateway Ready (GPS Enabled on All Devices!):`)
  console.log(`  ➜ Local HTTPS:   https://localhost:${HTTPS_PORT}/`)
  for (const ip of ips.filter((i) => i !== '127.0.0.1')) {
    console.log(`  ➜ Wi-Fi HTTPS:   https://${ip}:${HTTPS_PORT}/`)
  }
})

