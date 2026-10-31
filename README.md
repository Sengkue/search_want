# Search-Want — Problem-to-Shop Local Finder

A full-stack, responsive (**Mobile + Desktop**) web application built with **Nuxt 4 + Vuetify 4** on the frontend and **Python 3.12 + FastAPI** on the backend.

## Core Features (Phase 1)

1. **"Have a Problem & Don't Know Where to Go?" Discovery (`/`):**
   - Describe any everyday issue in plain language (e.g., *"My car won't start and makes a clicking noise"*, *"Engine smoking"*, *"Flat tire"*, *"Phone screen cracked"*, *"Water pipe leaking"*).
   - Smart symptom-to-category matching suggests the right specialist type and safety advice.
   - Live browser GPS detection (plus manual *"Move My Pin"* map tap fallback) finds **approved** nearby shops sorted by real Haversine distance (`km`), notifies you, and renders interactive map pins with 1-tap **Call** and **Google Maps Directions**.
2. **Self-Service Shop Onboarding (`/shops/add` & `/shops/mine`):**
   - Shop owners register/sign in, describe the problems they solve, and **pin their exact shop location** on the interactive map (or via *"Use My Current GPS"*).
   - Submitted shops enter **`PENDING`** status and notify Admin. Owners can track status and edit/resubmit if changes are requested.
3. **Admin "Approve Only" Moderation Console (`/admin/approvals`):**
   - Inspect pending shop submissions, verify their pinned map coordinates, and click **Approve** (publishes the shop live on the map immediately and notifies the owner) or **Reject** with feedback.
4. **Adaptive Mobile & Desktop UX:**
   - **Mobile:** Thumb-friendly bottom navigation bar, map/list view switcher, 1-tap GPS & phone call buttons.
   - **Desktop:** Top navigation bar, sticky split-screen interactive map + scrollable shop cards, and multi-card Admin queue.

---

## Quick Start

### 1. Start the Python Backend (Port `8000`)

Double-click `start-backend.bat`, or run in a terminal:

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- API Health: http://localhost:8000/api/health
- Interactive Swagger API Docs: http://localhost:8000/docs

### 2. Start the Nuxt 4 + Vuetify 4 Frontend (Port `3000`)

Double-click `start-frontend.bat`, or run in a second terminal:

```powershell
cd frontend
npm.cmd run dev
```

- Desktop Browser: http://localhost:3000
- Mobile Phone / Wi-Fi HTTPS (for live Browser GPS): `npm.cmd run dev:https` -> `https://<your-computer-lan-ip>:3443`

---

## Pre-Seeded Demo Accounts (Also available as 1-Click Buttons on `/login`)

| Role | Email | Password | What to Test |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@searchwant.com` | `admin123` | Open **Admin Approvals** and click **Approve** on pending shops |
| **Shop Owner** | `owner@searchwant.com` | `owner123` | Add a new shop location on the map & track approval notifications |
| **Customer** | `user@searchwant.com` | `user123` | Search car/phone/home problems & find nearby approved shops |


---

## Build the Android APK

The web app is wrapped with **Capacitor 8**, so the same Nuxt code becomes an Android app.

### One-time requirements (on the PC that builds the APK)

| Tool | Version | Notes |
| :--- | :--- | :--- |
| **JDK** | **21 or newer** | Set `JAVA_HOME`. (JDK 17 is not enough for Capacitor 8.) |
| **Android SDK** | Platform **36** + Build-Tools | Install Android Studio, or the command-line tools. Set `ANDROID_HOME`, or create `frontend/android/local.properties` with `sdk.dir=C:\\Users\\you\\AppData\\Local\\Android\\Sdk`. |

### Build

The app talks to your Python backend, and **a phone cannot reach `localhost` on your PC**, so give the build the backend address:

```powershell
cd frontend

# Real phone on the same Wi-Fi: use your PC's LAN IP (run `ipconfig` to find it)
npm run android:apk -- --api http://192.168.1.50:8000

# Backend deployed online (recommended for real users) — use HTTPS
npm run android:apk -- --api https://api.your-domain.com
```

The APK is created at `frontend/android/app/build/outputs/apk/debug/app-debug.apk`. Copy it to the phone and install it (allow "install unknown apps").

Other commands:

| Command | What it does |
| :--- | :--- |
| `npm run android:sync` | Rebuild the web app and copy it into `android/` without running Gradle |
| `npm run android:open` | Open the Android project in Android Studio (run on emulator/device from there) |
| `npm run android:apk -- --api <url> --release` | Unsigned release APK (must be signed before publishing to Google Play) |

You can also save the address once in `frontend/.env.android` as `NUXT_PUBLIC_API_BASE=http://192.168.1.50:8000`.

### Notes

- Start the backend with `--host 0.0.0.0` (already done by `start-backend.bat`) and allow port `8000` through the Windows firewall so the phone can reach it.
- In the Android **emulator**, `http://10.0.2.2:8000` reaches the PC's backend. It is the default when no `--api` is given.
- The app allows plain `http://` for development (`usesCleartextTraffic` in `android/app/src/main/AndroidManifest.xml`). For a published app, use an HTTPS backend and remove that setting.
- Self-hosted Lao variable fonts (`Noto Sans Lao Looped` & `Noto Sans Lao`) are bundled locally inside `frontend/public/fonts/` and `backend/app/static/fonts/` (works offline; OpenStreetMap tiles still require an internet connection).
- GPS: the app asks for location permission the first time you press "use GPS".
