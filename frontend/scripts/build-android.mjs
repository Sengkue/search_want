#!/usr/bin/env node
/**
 * Build the Search-Want web app into an Android APK (Capacitor).
 *
 * Usage (from the frontend/ folder):
 *   npm run android:apk -- --api http://192.168.1.50:8000        debug APK
 *   npm run android:apk -- --api https://api.example.com --release   release APK (unsigned)
 *   npm run android:sync                                          only rebuild web + sync into android/
 *
 * The backend URL is baked into the app. Resolution order:
 *   --api <url>  >  NUXT_PUBLIC_API_BASE env var  >  .env.android file  >  http://10.0.2.2:8000 (emulator only)
 */
import { spawnSync } from 'node:child_process'
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync } from 'node:fs'
import { homedir } from 'node:os'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const androidDir = join(root, 'android')
const isWin = process.platform === 'win32'

const args = process.argv.slice(2)
const flag = (name) => args.includes(name)
const option = (name) => {
  const i = args.indexOf(name)
  return i !== -1 ? args[i + 1] : undefined
}

const syncOnly = flag('--sync-only')
const release = flag('--release')

const log = (msg) => console.log(`\n\x1b[36m▶ ${msg}\x1b[0m`)
const fail = (msg) => {
  console.error(`\n\x1b[31m✖ ${msg}\x1b[0m`)
  process.exit(1)
}

function run(cmd, cmdArgs, opts = {}) {
  const res = spawnSync(cmd, cmdArgs, { stdio: 'inherit', shell: isWin, cwd: root, ...opts })
  if (res.status !== 0) fail(`Command failed: ${cmd} ${cmdArgs.join(' ')}`)
}

// ---------- 1. Backend URL ----------
function readEnvFile() {
  const file = join(root, '.env.android')
  if (!existsSync(file)) return undefined
  const line = readFileSync(file, 'utf8')
    .split(/\r?\n/)
    .find((l) => l.trim().startsWith('NUXT_PUBLIC_API_BASE='))
  return line?.split('=').slice(1).join('=').trim().replace(/^["']|["']$/g, '')
}

const apiBase = (option('--api') || process.env.NUXT_PUBLIC_API_BASE || readEnvFile() || '').replace(/\/$/, '')
if (apiBase) {
  log(`Backend URL baked into the app: ${apiBase}`)
  if (/localhost|127\.0\.0\.1/.test(apiBase)) {
    console.warn('\x1b[33m⚠ "localhost" points at the phone itself. Use your PC LAN IP (e.g. http://192.168.1.50:8000) or a public URL.\x1b[0m')
  }
} else {
  console.warn(
    '\x1b[33m⚠ No backend URL given. The app will use http://10.0.2.2:8000, which only works in the Android EMULATOR.\n' +
      '  For a real phone pass --api http://<your-pc-lan-ip>:8000 (or an https:// URL).\x1b[0m',
  )
}

// ---------- 2. Build the static web app ----------
log('Building web app (nuxt generate)…')
run('npm', ['run', 'generate'], { env: { ...process.env, NUXT_PUBLIC_API_BASE: apiBase } })

// ---------- 3. Sync into the Android project ----------
log('Syncing web assets into the Android project (cap sync)…')
run('npx', ['cap', 'sync', 'android'])

if (syncOnly) {
  log('Done. Open android/ in Android Studio, or run: npm run android:apk')
  process.exit(0)
}

// ---------- 4. Check toolchain, then run Gradle ----------
function javaMajor(javaBin = 'java') {
  const res = spawnSync(`"${javaBin}"`, ['-version'], { encoding: 'utf8', shell: true })
  const out = `${res.stderr || ''}${res.stdout || ''}`
  const m = out.match(/version "(\d+)(?:\.(\d+))?/)
  if (!m) return undefined
  return m[1] === '1' ? Number(m[2]) : Number(m[1])
}

/** Find a JDK >= 21: JAVA_HOME, then ~/tools/jdk-21*, Program Files, then whatever `java` is on PATH. */
function findJdk() {
  const homes = [process.env.JAVA_HOME]
  const userTools = join(homedir(), 'tools')
  for (const base of [userTools, 'C:\\Program Files\\Eclipse Adoptium', 'C:\\Program Files\\Java']) {
    if (!existsSync(base)) continue
    for (const d of readdirSync(base)) if (/jdk-?2\d|jdk-?[3-9]\d/i.test(d)) homes.push(join(base, d))
  }
  for (const home of homes.filter(Boolean)) {
    const bin = join(home, 'bin', isWin ? 'java.exe' : 'java')
    if (existsSync(bin) && (javaMajor(bin) ?? 0) >= 21) return { home, major: javaMajor(bin) }
  }
  const major = javaMajor()
  return major && major >= 21 ? { home: undefined, major } : { home: undefined, major }
}

function findSdk() {
  const candidates = [process.env.ANDROID_HOME, process.env.ANDROID_SDK_ROOT]
  const lp = join(androidDir, 'local.properties')
  if (existsSync(lp)) {
    const m = readFileSync(lp, 'utf8').match(/^sdk\.dir=(.+)$/m)
    if (m) candidates.push(m[1].trim().replace(/\\\\/g, '\\').replace(/\\:/g, ':'))
  }
  if (process.env.LOCALAPPDATA) candidates.push(join(process.env.LOCALAPPDATA, 'Android', 'Sdk'))
  return candidates.filter(Boolean).find((p) => existsSync(p))
}

const jdk = findJdk()
if (!jdk.major || jdk.major < 21) {
  fail(
    `Capacitor 8 needs JDK 21 or newer (found: ${jdk.major ?? 'none'}).\n` +
      '  Install e.g. Eclipse Temurin 21 and set JAVA_HOME (or unzip it to ~/tools/jdk-21), then run this again.',
  )
}
log(`Using JDK ${jdk.major}${jdk.home ? ` (${jdk.home})` : ''}`)
const sdk = findSdk()
if (!sdk) {
  fail(
    'Android SDK not found.\n' +
      '  Install Android Studio (or the command-line tools) and set ANDROID_HOME,\n' +
      '  or create frontend/android/local.properties containing:  sdk.dir=C:\\\\path\\\\to\\\\Android\\\\Sdk',
  )
}
log(`Using Android SDK: ${sdk}`)

const task = release ? 'assembleRelease' : 'assembleDebug'
log(`Building APK (gradle ${task})…`)
const gradle = join(androidDir, isWin ? 'gradlew.bat' : 'gradlew')
run(gradle, [task], {
  cwd: androidDir,
  env: { ...process.env, ANDROID_HOME: sdk, ...(jdk.home ? { JAVA_HOME: jdk.home } : {}) },
})

const apk = release
  ? join(androidDir, 'app', 'build', 'outputs', 'apk', 'release', 'app-release-unsigned.apk')
  : join(androidDir, 'app', 'build', 'outputs', 'apk', 'debug', 'app-debug.apk')
if (existsSync(apk)) {
  const distDir = resolve(root, '..', 'dist')
  mkdirSync(distDir, { recursive: true })
  const destApk = join(distDir, release ? 'SearchWant-release-unsigned.apk' : 'SearchWant-debug.apk')
  copyFileSync(apk, destApk)
  log(`APK ready: ${apk}\n  Copied for web download: ${destApk}`)
} else {
  log(`Build finished. Look for the APK under ${join(androidDir, 'app', 'build', 'outputs', 'apk')}`)
}
if (release) console.log('Release APKs must be signed before they can be installed/published.')

