# Search-Want — ຄົ້ນຫາຮ້ານສ້ອມແປງ ແລະ ບໍລິການໃກ້ຄຽງຈາກບັນຫາຂອງທ່ານ

ລະບົບເວັບແອັບພລິເຄຊັນ (SSR + SEO ຄວາມໄວສູງ) ແລະ ແອັບມືຖື Android APK ແບບ Full-Stack (ຮອງຮັບທັງ **ມືຖື ແລະ ຄອມພິວເຕີ**) ພາສາລາວ 100%, ພັດທະນາດ້ວຍ **Nuxt 4 + Vuetify 4 (Tree-Shaken) + Pinia + Leaflet + Capacitor 8** ໃນຝັ່ງ Frontend ແລະ **Python 3.12 + FastAPI + SQLAlchemy + PostgreSQL** ໃນຝັ່ງ Backend.

---

## ຄຸນສົມບັດຫຼັກ

1. **ຄົ້ນຫາຮ້ານຈາກອາການ ຫຼື ບັນຫາທີ່ກຳລັງພົບ (`/`):**
   - **ຊ່ອງຄົ້ນຫາແບບ Pill Capsule & ປຸ່ມ `🔍 ຄົ້ນຫາ` Gradient ລະດັບ Native App:** ພິມອາການດ້ວຍພາສາທຳມະດາ (ເຊັ່ນ: *"ລົດສະຕາດບໍ່ຕິດ"*, *"ເຄື່ອງຍົນມີຄວັນ"*, *"ຢາງລົດແບນ"*, *"ໜ້າຈໍໂທລະສັບແຕກ"*, *"ທໍ່ນ້ຳຮົ່ວ"*, *"ແອບໍ່ເຢັນ"*).
   - **ຈັດການແປ້ນພິມມືຖືອັດສະລິຍະ (Smart Mobile Keyboard UX):**
     - ກົດປຸ່ມ `ຄົ້ນຫາ` ຫຼື ປຸ່ມລ້າງ `✕` ໂດຍແປ້ນພິມມືຖືບໍ່ເດັ້ງຂຶ້ນມາລົບກວນເອງ ແລະ ພັບເກັບແປ້ນພິມລົງທັນທີ (`blur()`) ເມື່ອກົດຄົ້ນຫາ ຫຼື ກົດປຸ່ມ `Search` ເທິງແປ້ນພິມໂທລະສັບ.
     - ສະແດງກ່ອງແນະນຳອາການພາສາລາວແບບ Real-time + ປະຫວັດຄົ້ນຫາຫຼ້າສຸດ + ປຸ່ມ `⌨ ປິດ` ແປ້ນພິມ ພ້ອມຕົວອັກສອນ `16px` ປ້ອງກັນໜ້າຈໍມືຖືຊູມເອງ ແລະ ເລື່ອນເຊື່ອງແຖບເມນູລຸ່ມອັດຕະໂນມັດຂະນະກຳລັງພິມ.
   - **ວິເຄາະອາການ & ຄຳນວນໄລຍະທາງ GPS ຈິງ:** ແນະນຳປະເພດຊ່າງທີ່ກົງຈຸດ ພ້ອມດຶງພິກັດ GPS ສົດ (ຫຼື ລາກໝຸດເທິງແຜນທີ່) ເພື່ອຈັດລຽງຮ້ານທີ່ **ຜ່ານການອະນຸມັດແລ້ວ** ຕາມໄລຍະທາງຈິງ (`ກມ.`), ພ້ອມປຸ່ມ **ໂທຫາຮ້ານ** ແລະ **ນຳທາງ Google Maps** ໃນ 1 ແຕະ.

2. **ໜ້າໂປຣໄຟລ໌ຮ້ານຄ້າສາທາລະນະສຳລັບ SEO (`/shops/[id]`):**
   - ທຸກຮ້ານທີ່ຜ່ານການອະນຸມັດແລ້ວຈະມີໜ້າເວັບສະເພາະຂອງຕົນເອງ (ເຊັ່ນ `/shops/1`) ສະແດງລາຍລະອຽດບໍລິການຄົບຖ້ວນ, ເວລາເປີດ-ປິດ, ປ້າຍສຸກເສີນ 24 ຊມ., ເບີໂທຕິດຕໍ່, ພິກັດແຜນທີ່ ແລະ ປຸ່ມ Tag ອາການທີ່ຮັບແກ້ໄຂ ເພື່ອໃຫ້ລູກຄ້າຄົ້ນຫາພົບຜ່ານ Google Search ໂດຍກົງ.

3. **ເຈົ້າຂອງຮ້ານເພີ່ມຮ້ານຂຶ້ນແຜນທີ່ໄດ້ເອງຟຣີ (`/shops/add` ແລະ `/shops/mine`):**
   - ເຈົ້າຂອງຮ້ານ ຫຼື ຊ່າງສ້ອມແປງ ສາມາດລົງທະບຽນ/ເຂົ້າສູ່ລະບົບ, ລະບຸບັນຫາທີ່ຮັບແກ້ໄຂ ແລະ **ປັກໝຸດຕຳແໜ່ງຮ້ານທີ່ຊັດເຈນ** ເທິງແຜນທີ່ (ຫຼື ກົດປຸ່ມ *"ດຶງ GPS ຂອງຂ້ອຍ"*).
   - ຮ້ານທີ່ສົ່ງເຂົ້າມາຈະຢູ່ໃນສະຖານະ **`PENDING` (ລໍຖ້າອະນຸມັດ)** ແລະ ແຈ້ງເຕືອນຫາຜູ້ດູແລລະບົບທັນທີ. ເຈົ້າຂອງຮ້ານສາມາດຕິດຕາມສະຖານະ ແລະ ແກ້ໄຂຂໍ້ມູນເພື່ອສົ່ງກວດຄືນໃໝ່ໄດ້.

4. **ໜ້າຜູ້ດູແລລະບົບກວດສອບ, ອະນຸມັດຮ້ານ ແລະ ຈັດການສິດ (`/admin/approvals`):**
   - ກວດສອບລາຍລະອຽດຮ້ານທີ່ສົ່ງເຂົ້າມາ, ກວດພິກັດໝຸດເທິງແຜນທີ່ ແລ້ວກົດ **ອະນຸມັດ (`Approve`)** ເພື່ອເຜີຍແຜ່ຮ້ານຂຶ້ນແຜນທີ່ ແລະ ເພີ່ມເຂົ້າ `/sitemap.xml` ທັນທີ ຫຼື **ປະຕິເສດ (`Reject`)** / **ຢຸດຊົ່ວຄາວ (`Suspend`)** ພ້ອມລະບຸເຫດຜົນແຈ້ງເຕືອນເຈົ້າຂອງຮ້ານ.

5. **ດີໄຊນ໌ຮອງຮັບທັງມືຖື ແລະ ຄອມພິວເຕີ + ຟອນພາສາລາວຝັງໃນໂຕ 100%:**
   - **ມືຖື (Mobile):** ແຖບເມນູລຸ່ມສຸດ (Footer Navigation) ກົດງ່າຍດ້ວຍມືດຽວ (ບໍ່ມີແຖບເມນູເທິງບັງໜ້າຈໍ ແລະ ເຊື່ອງອັດຕະໂນມັດເມື່ອແປ້ນພິມເປີດ), ສະຫຼັບມຸມມອງ ທັງສອງ / ແຜນທີ່ເຕັມຈໍ / ລາຍການ, ຮອງຮັບໂໝດແຈ້ງ ແລະ ໂໝດມືດ.
   - **ຄອມພິວເຕີ (Desktop):** ແຖບເມນູດ້ານເທິງແບບ Frosted Glass, ໜ້າຈໍແບ່ງຊ້າຍ-ຂວາ (ລາຍຊື່ຮ້ານ + ແຜນທີ່ໂຕ້ຕອບແບບ Sticky).
   - **ຟອນພາສາລາວໃນໂຕ (Self-Hosted Lao Fonts):** ຝັງໄຟລ໌ຟອນ `Noto Sans Lao Looped` ແລະ `Noto Sans Lao` ໄວ້ໃນໂປຣເຈັກໂດຍກົງ (`frontend/public/fonts/` ແລະ `backend/app/static/fonts/`) ຄົມຊັດທຸກໜ້າຈໍໂດຍບໍ່ຕ້ອງເພິ່ງ CDN ພາຍນອກ.

6. **ລະບົບສ້າງລາຍຮັບ Google AdSense (`/admin/approvals?tab=ADSENSE`, `/ads.txt`, `/privacy`):**
   - ຕິດຕັ້ງຊ່ອງໂຄສະນາ **In-Feed** ແລະ **Responsive Banner** ແບບ Lazy Client-Hydrated (ບໍ່ກະທົບຄວາມໄວ SSR ແລະ ບໍ່ປົນເປື້ອນເນື້ອຫາ SEO ທີ່ Googlebot ອ່ານ).
   - ຈັດການລະຫັດ Publisher ID (`ca-pub-4990570878383229`), Slot IDs (`6642734194`, `8750022785`), Auto Ads ແລະ **ໂໝດທົດລອງ** ສະເພາະສິດ `SUPER_ADMIN` ພ້ອມສ້າງ `/ads.txt` ແລະ `/privacy` ອັດຕະໂນມັດ.

---

## ສະຖາປັດຕະຍະກຳ Frontend ເບົາ, ໄວ ແລະ ຕິດອັນດັບ Top Search SEO

ໂປຣເຈັກໄດ້ຖືກປັບຈູນລະດັບ Production ເພື່ອໃຫ້ໂຫຼດເບົາທີ່ສຸດ, ສະແດງຜົນໄວທີ່ສຸດ ແລະ ຮອງຮັບການຈັດອັນດັບເທິງ Google Search ສູງສຸດ:

### 1. ເບົາ (`Lightweight Bundle & Assets`)
- **Vuetify 4 Tree-Shaking (`frontend/app/plugins/vuetify.ts`):** Import ສະເພາະ 35 Component ທີ່ໃຊ້ງານຈິງເທົ່ານັ້ນ (ຕັດ Component ສ່ວນເກີນ 60+ ໂຕອອກຈາກ JavaScript Bundle).
- **Map & Dialog Code-Splitting:** ແຍກ CSS ແລະ JS ຂອງແຜນທີ່ Leaflet (`leaflet-vendor`) ໄວ້ໃນ `ShopMap.client.vue` ເພື່ອບໍ່ໃຫ້ໜ້າອື່ນຕ້ອງໂຫຼດໄຟລ໌ແຜນທີ່ ແລະ ໃຊ້ `<LazyAdSenseSlot>`, `<LazyMobileInstallDialog>`, `<LazyGpsSecureOriginDialog>` ເພື່ອຫຼຸດຂະໜາດໄຟລ໌ເລີ່ມຕົ້ນ.
- **Brotli + Gzip & Immutable Cache (`frontend/nuxt.config.ts`):** ບີບອັດໄຟລ໌ Static ອັດຕະໂນມັດ ແລະ ຕັ້ງ `Cache-Control: public, max-age=31536000, immutable` ສຳລັບ `/_nuxt/**` ແລະ `/fonts/**`.

### 2. ໄວ (`Blazing-Fast SSR & 60fps UI`)
- **Full Server-Side Rendering (`ssr: true`):** ດຶງຂໍ້ມູນໝວດໝູ່, ອາການ ແລະ ຮ້ານໃກ້ຄຽງແບບຂະໜານ (`Promise.all` ຜ່ານ `useAsyncData`) ຕັ້ງແຕ່ເທິງ Server ເຮັດໃຫ້ເປີດໜ້າທຳອິດເຫັນລາຍຊື່ຮ້ານທັນທີ (`Instant LCP`) — ສ່ວນຕອນ Build ໄຟລ໌ Android APK ສະຄຣິບ `scripts/build-android.mjs` ຈະສະຫຼັບເປັນ `NUXT_SSR=false` ອັດຕະໂນມັດ.
- **In-Memory Store Cache & Request Deduplication (`frontend/app/stores/shops.ts`):** ຈື່ຂໍ້ມູນໝວດໝູ່ ແລະ ອາການໄວ້ໃນ Memory 5 ນາທີ ເຮັດໃຫ້ການສະຫຼັບໜ້າໄປ-ມາໄວ `0ms` ພ້ອມລະບົບປ້ອງກັນ API Response ເກົ່າທັບຜົນຄົ້ນຫາໃໝ່.
- **Zero-CLS & Smooth Scrolling (`frontend/app/assets/css/main.css`):** ໃຊ້ CSS Media Queries ຈັດການ Navbar/Footer ໂດຍບໍ່ມີອາການໜ້າຈໍກະພິບ (`CLS = 0`) ແລະ ໃຊ້ `content-visibility: auto` ກັບບັດຮ້ານຄ້າ ເພື່ອໃຫ້ເລື່ອນໜ້າຈໍມືຖືລື່ນ 60fps.

### 3. ຕິດ Top Search Google SEO (`Technical & Local Business SEO`)
- **Googlebot ອ່ານ HTML ພາສາລາວໄດ້ 100% ທັນທີ:** ທັງໜ້າຫຼັກ (`/`), ໜ້າໝວດໝູ່ (`/?category=...`), ໜ້າຄຳຄົ້ນຫາ (`/?q=...`) ແລະ ໜ້າລາຍລະອຽດຮ້ານ (`/shops/[id]`) ຖືກ Pre-render ເປັນ Semantic HTML (`<h1>`, `<h2>`, `<article>`, `<nav>`, `<details>`).
- **Schema.org Rich Results (`JSON-LD`) ອັດຕະໂນມັດ (`frontend/app/composables/useSeo.ts`):**
  - ໜ້າຫຼັກ (`/`): ຝັງ `WebSite` + `SearchAction` (Sitelinks Search Box), `ItemList` ແລະ `FAQPage`.
  - ໜ້າຮ້ານຄ້າ (`/shops/[id]`): ຝັງ `LocalBusiness` (ພ້ອມພິກັດ `GeoCoordinates`, `telephone`, `openingHours`, `PostalAddress` ປະເທດລາວ `LA`) ແລະ `BreadcrumbList`.
- **Dynamic `/sitemap.xml` ແລະ `/robots.txt` ອັດຕະໂນມັດ:**
  - ເມື່ອ Admin ກົດອະນຸມັດຮ້ານໃໝ່ ລິ້ງ `/shops/{id}` ຈະຖືກເພີ່ມເຂົ້າ `/sitemap.xml` ທັນທີ (ຮ້ານທີ່ຍັງ `PENDING` ຫຼື `REJECTED` ຈະບໍ່ຖືກເປີດເຜີຍ).
  - ກຳນົດ `noindex, nofollow` ໃຫ້ໜ້າ `/admin/**`, `/shops/mine` ແລະ `/login` ເພື່ອໃຫ້ Google ທຸ່ມຄະແນນການຈັດອັນດັບໄປທີ່ໜ້າຮ້ານຄ້າ ແລະ ໜ້າຄົ້ນຫາ 100%.

---

## ໂຄງສ້າງໂປຣເຈັກ

| ໂຟນເດີ / ໄຟລ໌ | ລາຍລະອຽດ |
| :--- | :--- |
| `backend/` | ລະບົບຫຼັງບ້ານ Python 3.12 + FastAPI + SQLAlchemy + PostgreSQL + RBAC & Dynamic SEO API |
| `frontend/` | ລະບົບໜ້າບ້ານ Nuxt 4 (SSR) + Vuetify 4 (Tree-Shaken) + Leaflet + Nitro Sitemap/Robots + Capacitor 8 |
| `dist/` | ບ່ອນເກັບໄຟລ໌ແອັບ Android APK ທີ່ສ້າງສຳເລັດແລ້ວ (`SearchWant-debug.apk`) |
| `.env.example` | ໄຟລ໌ຕົວຢ່າງການຕັ້ງຄ່າ Environment Variables ສຳລັບ Production, ຖານຂໍ້ມູນ, SEO Domain ແລະ Google AdSense |
| `start-backend.bat` | ໄຟລ໌ລັດສຳລັບດັບເບິນຄລິກເປີດເຊີບເວີ Python Backend (`Port 8000`) |
| `start-frontend.bat` | ໄຟລ໌ລັດສຳລັບດັບເບິນຄລິກເປີດເຊີບເວີ Nuxt 4 Frontend (`Port 3000`) |
| `allow-mobile-access.bat` | ໄຟລ໌ເປີດ Windows Firewall (`Port 3000, 8000`) ເພື່ອໃຫ້ມືຖືໃນວົງ Wi-Fi ດຽວກັນເຂົ້າເຖິງໄດ້ |

---

## ວິທີເປີດໃຊ້ງານລະບົບ (Quick Start)

### 1. ເປີດເຊີບເວີ Python Backend (Port `8000`)

ດັບເບິນຄລິກໄຟລ໌ `start-backend.bat` ຫຼື ລັນຄຳສັ່ງໃນ Terminal:

```powershell
cd backend
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- ກວດສອບສະຖານະ API: http://localhost:8000/api/health
- ເອກະສານ API ແບບໂຕ້ຕອບ (Swagger UI — ເປີດສະເພາະໂໝດພັດທະນາ): http://localhost:8000/docs

### 2. ເປີດເຊີບເວີ Nuxt 4 SSR Frontend (Port `3000`)

ດັບເບິນຄລິກໄຟລ໌ `start-frontend.bat` ຫຼື ເປີດ Terminal ອີກໜ້າຕ່າງໜຶ່ງແລ້ວລັນ:

```powershell
cd frontend
npm.cmd run dev
```

- **ເປີດເທິງຄອມພິວເຕີ:** http://localhost:3000
- **ກວດສອບ Sitemap & Robots ສຳລັບ SEO:** http://localhost:3000/sitemap.xml ແລະ http://localhost:3000/robots.txt
- **ເປີດເທິງມືຖືຜ່ານ Wi-Fi ພ້ອມໃຊ້ GPS ສົດ (HTTPS Port `3443`):**
  ```powershell
  cd frontend
  npm.cmd run dev:https
  ```
  ຈາກນັ້ນເປີດໃນມືຖືທີ່ຕໍ່ Wi-Fi ດຽວກັນທີ່ `https://<IP-ຄອມພິວເຕີຂອງທ່ານ>:3443` *(ຫາກມືຖືເຂົ້າບໍ່ໄດ້ ໃຫ້ຄລິກຂວາທີ່ `allow-mobile-access.bat` ແລ້ວເລືອກ **Run as administrator** 1 ຄັ້ງ).*

### 3. ການ Build ແລະ ລັນ Frontend ໃນໂໝດ Production SSR (ຄວາມໄວສູງສຸດ)

```powershell
cd frontend
npm.cmd run build
node .output/server/index.mjs
```

---

## ບັນຊີທົດລອງໃນໂໝດພັດທະນາ (ປິດອັດຕະໂນມັດເມື່ອຕັ້ງ `SEARCH_WANT_ENV=production`)

| ບົດບາດ | ອີເມວ | ລະຫັດຜ່ານ | ສິ່ງທີ່ສາມາດທົດສອບໄດ້ |
| :--- | :--- | :--- | :--- |
| **ຜູ້ບໍລິຫານສູງສຸດ (`SUPER_ADMIN`)** | `admin@searchwant.com` | `admin123` | ຈັດການສິດຜູ້ໃຊ້ທຸກລະດັບ, ກວດສອບຄວາມປອດໄພ Production, ຕັ້ງຄ່າ **Google AdSense** ແລະ ອະນຸມັດຮ້ານ |
| **ເຈົ້າຂອງຮ້ານ (`SHOP_OWNER`)** | `owner@searchwant.com` | `owner123` | ເພີ່ມຮ້ານໃໝ່ເທິງແຜນທີ່, ປັກໝຸດພິກັດ GPS ແລະ ຕິດຕາມການແຈ້ງເຕືອນຜົນອະນຸມັດ |
| **ລູກຄ້າທົ່ວໄປ (`USER`)** | `user@searchwant.com` | `user123` | ພິມບັນຫາລົດ/ໂທລະສັບ/ໄຟຟ້າ-ປະປາ ເພື່ອຄົ້ນຫາຮ້ານໃກ້ຄຽງ, ໂທຫາຮ້ານ ແລະ ນຳທາງ |

---

## ການແບ່ງສິດລະດັບສູງ (4-Tier RBAC) ແລະ ຄວາມປອດໄພລະດັບ Production

ລະບົບແຍກສິດການເຂົ້າເຖິງອອກເປັນ **4 ລະດັບ** ພ້ອມລະບົບຍົກເລີກ Token ທັນທີ (`token_version`) ເມື່ອມີການປ່ຽນສິດ, ລະງັບບັນຊີ ຫຼື ປ່ຽນລະຫັດຜ່ານ:

| ລະດັບສິດ | ສິດທີ່ອະນຸຍາດ | ຂໍ້ຈຳກັດເພື່ອຄວາມປອດໄພ |
| :--- | :--- | :--- |
| **`SUPER_ADMIN` (ຜູ້ບໍລິຫານສູງສຸດ)** | ອະນຸມັດຮ້ານ, **ຕັ້ງຄ່າລາຍຮັບ Google AdSense & `/ads.txt`**, **ແຕ່ງຕັ້ງ/ຖອນສິດ Admin**, **ລະງັບບັນຊີຜູ້ໃຊ້** ແລະ ກວດສອບຄວາມພ້ອມ Production (`/admin/approvals?tab=RBAC`) | ມີລະບົບປ້ອງກັນບໍ່ໃຫ້ຫຼຸດສິດ ຫຼື ລະງັບບັນຊີຕົນເອງ (ປ້ອງກັນການລັອກອອກຈາກລະບົບ) |
| **`ADMIN` (ຜູ້ດູແລອະນຸມັດຮ້ານ)** | ກວດສອບໝຸດແຜນທີ່, ກົດອະນຸມັດ / ປະຕິເສດ / ຢຸດຮ້ານຊົ່ວຄາວ ແລະ ເບິ່ງປະຫວັດການກວດສອບ | **ບໍ່ສາມາດ** ແກ້ໄຂລະຫັດ Google AdSense ແລະ **ບໍ່ສາມາດ** ປ່ຽນສິດ ຫຼື ລະງັບບັນຊີຜູ້ໃຊ້ (`403`) |
| **`SHOP_OWNER` (ເຈົ້າຂອງຮ້ານ)** | ເພີ່ມຮ້ານໃໝ່, ແກ້ໄຂສະເພາະຮ້ານຂອງຕົນເອງ (ຕ້ອງຜ່ານການອະນຸມັດໃໝ່ທຸກຄັ້ງ) ແລະ ລຶບຮ້ານຮ່າງທີ່ຍັງບໍ່ອະນຸມັດ | **ບໍ່ສາມາດ** ແກ້ໄຂຮ້ານຄົນອື່ນ, **ບໍ່ສາມາດ** ແກ້ໄຂຮ້ານທີ່ຖືກຜູ້ດູແລລະງັບ (`SUSPENDED`) ແລະ ເຂົ້າໜ້າ `/admin/*` ບໍ່ໄດ້ |
| **`USER` (ຜູ້ໃຊ້ທົ່ວໄປ)** | ຄົ້ນຫາຮ້ານທີ່ອະນຸມັດແລ້ວ, ປ່ຽນລະຫັດຜ່ານຕົນເອງ ແລະ ອັບເກຣດເປັນ `SHOP_OWNER` ອັດຕະໂນມັດເມື່ອສົ່ງຮ້ານທຳອິດ | ເຂົ້າເຖິງສະເພາະຂໍ້ມູນສາທາລະນະ (ບໍ່ເປີດເຜີຍອີເມວສ່ວນຕົວຂອງເຈົ້າຂອງຮ້ານ) |

### ການຕັ້ງຄ່າກ່ອນນຳຂຶ້ນ Production & Google Search Console (`.env`)
ເມື່ອນຳລະບົບຂຶ້ນເຊີບເວີຈິງ ໃຫ້ກຳນົດຄ່າໃນ `.env` (ເບິ່ງຕົວຢ່າງໃນ `.env.example`):
- `SEARCH_WANT_ENV=production` — ປິດປຸ່ມລ໊ອກອິນທົດລອງ 1 ຄລິກ, ບລັອກບັນຊີທົດລອງທີ່ໃຊ້ລະຫັດຜ່ານອ່ອນ (`admin123`/`owner123`/`user123`), ປິດ `/api/shops/seed-nearby` ແລະ ເຊື່ອງໜ້າ `/docs` ອັດຕະໂນມັດ.
- `SEARCH_WANT_SECRET_KEY=<ລະຫັດສຸ່ມຍາວຢ່າງໜ້ອຍ 32 ຕົວອັກສອນ>` — ບັງຄັບກວດສອບກ່ອນເປີດເຊີບເວີ Production.
- `SEARCH_WANT_SUPER_ADMIN_EMAIL` ແລະ `SEARCH_WANT_SUPER_ADMIN_PASSWORD` — ສ້າງບັນຊີຜູ້ບໍລິຫານສູງສຸດຕົວຈິງຂອງທ່ານອັດຕະໂນມັດໂດຍບໍ່ໃຊ້ບັນຊີທົດລອງ.
- `SEARCH_WANT_CORS_ORIGINS=https://ໂດເມນຂອງທ່ານ.la` — ອະນຸຍາດການເອີ້ນ API ສະເພາະໂດເມນຈິງຂອງທ່ານເທົ່ານັ້ນ.
- `NUXT_PUBLIC_SITE_URL=https://ໂດເມນຂອງທ່ານ.la` ແລະ `SEARCH_WANT_SITE_URL=https://ໂດເມນຂອງທ່ານ.la` — ໃຊ້ສ້າງລິ້ງ Canonical, OpenGraph, JSON-LD ແລະ `/sitemap.xml` ໃຫ້ກົງກັບໂດເມນຈິງ ແລ້ວນຳ `https://ໂດເມນຂອງທ່ານ.la/sitemap.xml` ໄປຢືນຢັນໃນ **Google Search Console → Sitemaps** ເພື່ອໃຫ້ Google ເກັບດັດຊະນີທຸກຮ້ານຂຶ້ນອັນດັບຄົ້ນຫາທັນທີ.

---

## ການເປີດຮັບລາຍຮັບຈິງຈາກ Google AdSense (ເມື່ອນຳເວັບຂຶ້ນໂດເມນຈິງ)

ປັດຈຸບັນລະບົບໄດ້ຜູກລະຫັດບັນຊີ Google AdSense ໄວ້ພ້ອມແລ້ວ (`ca-pub-4990570878383229`, In-Feed Slot: `6642734194`, Banner Slot: `8750022785`). ເມື່ອທ່ານນຳເວັບໄຊຂຶ້ນເຊີບເວີຈິງ ໃຫ້ປະຕິບັດ 3 ຂັ້ນຕອນດັ່ງນີ້:

1. **ອັບເວັບຂຶ້ນໂດເມນຈິງ (HTTPS):** ເຊັ່ນ `.com` ຫຼື `.la` ແລະ ກວດສອບວ່າ `https://ໂດເມນຂອງທ່ານ/ads.txt` ສະແດງຂໍ້ຄວາມ:
   ```text
   google.com, pub-4990570878383229, DIRECT, f08c47fec0942fa0
   ```
2. **ສົ່ງໂດເມນໃຫ້ Google AdSense ອະນຸມັດ:** ເຂົ້າໄປທີ່ເວັບໄຊ Google AdSense -> ເມນູ **Sites** -> ກົດ **Add site** ໃສ່ຊື່ໂດເມນຂອງທ່ານ ແລະ ລໍຖ້າຈົນສະຖານະປ່ຽນເປັນ **`Ready`**.
3. **ປິດໂໝດທົດລອງເພື່ອຮັບໂຄສະນາຈິງ:** ເຂົ້າສູ່ລະບົບ Super Admin ທີ່ໜ້າ `/admin/approvals?tab=ADSENSE` -> ປິດປຸ່ມ **ໂໝດທົດລອງ (Preview / Test Mode)** -> ກົດ **ບັນທຶກການຕັ້ງຄ່າ** ເພື່ອໃຫ້ Google ສະແດງໂຄສະນາຈິງ 100%.

---

## ການສ້າງໄຟລ໌ແອັບ Android APK (Capacitor 8)

ໂປຣເຈັກນີ້ໃຊ້ **Capacitor 8** ຫຸ້ມລະບົບເວັບ Nuxt 4 ເພື່ອສ້າງເປັນໄຟລ໌ແອັບມືຖື Android APK ຈາກໂຄ້ດຊຸດດຽວກັນ (ສະຄຣິບ Build ຈະສະຫຼັບເປັນໂໝດ Static SPA `NUXT_SSR=false` ໃຫ້ອັດຕະໂນມັດ ພ້ອມຕັ້ງ `android:windowSoftInputMode="adjustResize"` ສຳລັບແປ້ນພິມມືຖື).

### ສິ່ງທີ່ຕ້ອງຕິດຕັ້ງຄັ້ງທຳອິດ (ເທິງຄອມພິວເຕີທີ່ໃຊ້ສ້າງ APK)

| ເຄື່ອງມື | ເວີຊັນ | ໝາຍເຫດ |
| :--- | :--- | :--- |
| **JDK** | **21 ຂຶ້ນໄປ** | ຕັ້ງຄ່າ `JAVA_HOME` ໃຫ້ຊີ້ໄປຫາ JDK 21+ (JDK 17 ບໍ່ຮອງຮັບ Capacitor 8). |
| **Android SDK** | Platform **36** + Build-Tools | ຕິດຕັ້ງຜ່ານ Android Studio ຫຼື Command-line tools, ແລ້ວຕັ້ງຄ່າ `ANDROID_HOME` ຫຼື ສ້າງໄຟລ໌ `frontend/android/local.properties` ໂດຍໃສ່ `sdk.dir=C:\\Users\\ຊື່ຜູ້ໃຊ້\\AppData\\Local\\Android\\Sdk`. |

### ຄຳສັ່ງສ້າງໄຟລ໌ APK

ເນື່ອງຈາກແອັບເທິງມືຖືຈິງບໍ່ສາມາດເອີ້ນຫາ `localhost` ຂອງຄອມພິວເຕີໄດ້ໂດຍກົງ, ໃຫ້ລະບຸ URL ຫຼື IP ຂອງເຊີບເວີ Backend ຕອນສ້າງໄຟລ໌ APK:

```powershell
cd frontend

# ກໍລະນີທົດສອບກັບມືຖືຈິງໃນວົງ Wi-Fi ດຽວກັນ: ໃສ່ IPv4 ຂອງຄອມພິວເຕີ (ເບິ່ງໄດ້ຈາກຄຳສັ່ງ `ipconfig`)
npm run android:apk -- --api http://192.168.1.50:8000

# ກໍລະນີນຳ Backend ຂຶ້ນເຊີບເວີອອນລາຍແລ້ວ (ແນະນຳສຳລັບຜູ້ໃຊ້ງານຈິງ) — ໃຊ້ HTTPS
npm run android:apk -- --api https://api.your-domain.com
```

ໄຟລ໌ APK ທີ່ສ້າງສຳເລັດຈະຢູ່ທີ່:
- `dist/SearchWant-debug.apk` *(ຫຼື `frontend/android/app/build/outputs/apk/debug/app-debug.apk`)*

ສາມາດສົ່ງໄຟລ໌ APK ນີ້ເຂົ້າມືຖື Android ແລ້ວກົດຕິດຕັ້ງໄດ້ທັນທີ (ອະນຸຍາດ *"Install unknown apps"* ເມື່ອຕິດຕັ້ງຄັ້ງທຳອິດ).

### ຄຳສັ່ງເພີ່ມເຕີມສຳລັບ Android

| ຄຳສັ່ງ | ໜ້າທີ່ການທຳງານ |
| :--- | :--- |
| `npm run android:sync` | Build ເວັບໃໝ່ ແລະ ຄັດລອກໄປໃສ່ໂຟນເດີ `android/` ໂດຍບໍ່ລັນ Gradle |
| `npm run android:open` | ເປີດໂປຣເຈັກ Android ໃນໂປຣແກຣມ Android Studio |
| `npm run android:apk -- --api <url> --release` | ສ້າງໄຟລ໌ Release APK (ຕ້ອງ Sign Key ກ່ອນນຳຂຶ້ນ Google Play Store) |

ທ່ານຍັງສາມາດບັນທຶກຄ່າ URL ຂອງ Backend ໄວ້ຖາວອນໃນໄຟລ໌ `frontend/.env.android` ໄດ້ ເຊັ່ນ: `NUXT_PUBLIC_API_BASE=http://192.168.1.50:8000`.

### ໝາຍເຫດສຳຄັນສຳລັບແອັບ Android

- ເປີດເຊີບເວີ Backend ດ້ວຍ `--host 0.0.0.0` (ໄຟລ໌ `start-backend.bat` ຕັ້ງໄວ້ໃຫ້ແລ້ວ) ແລະ ອະນຸຍາດ Port `8000` ຜ່ານ Windows Firewall (`allow-mobile-access.bat`).
- ໃນ **Android Emulator**, ຄ່າເລີ່ມຕົ້ນ `http://10.0.2.2:8000` ຈະເຊື່ອມຕໍ່ຫາ Backend ໃນຄອມພິວເຕີໂດຍອັດຕະໂນມັດຫາກບໍ່ໄດ້ລະບຸ `--api`.
- ໃນໂໝດພັດທະນາ ແອັບອະນຸຍາດການເຊື່ອມຕໍ່ແບບ `http://` (`usesCleartextTraffic` ໃນ `android/app/src/main/AndroidManifest.xml`). ເມື່ອເຜີຍແຜ່ຈິງ ແນະນຳໃຫ້ໃຊ້ Backend ແບບ `https://`.
- ຟອນພາສາລາວ (`Noto Sans Lao Looped` ແລະ `Noto Sans Lao`) ຖືກຝັງໄວ້ໃນໂຕແອັບຮຽບຮ້ອຍແລ້ວ ຈຶ່ງສະແດງພາສາລາວໄດ້ທັນທີແມ່ນແຕ່ຕອນອອບລາຍ (ສ່ວນແຜນທີ່ OpenStreetMap ຍັງຕ້ອງໃຊ້ອິນເຕີເນັດໃນການໂຫຼດ).
- ລະບົບ GPS ໃນແອັບຈະຂໍສິດເຂົ້າເຖິງຕຳແໜ່ງ (Location Permission) ອັດຕະໂນມັດເມື່ອກົດປຸ່ມຄົ້ນຫາພິກັດ GPS ຄັ້ງທຳອິດ.

---

## ການລັນຊຸດທົດສອບລະບົບ (Automated Tests)

ສາມາດກວດສອບຄວາມຖືກຕ້ອງຂອງລະບົບ API, RBAC, ຄວາມປອດໄພ Production, Sitemap/Robots SEO ແລະ Google AdSense ທັງໝົດດ້ວຍ Pytest (`11/11` tests):

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```
