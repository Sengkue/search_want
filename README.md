# Search-Want — ຄົ້ນຫາຮ້ານສ້ອມແປງ ແລະ ບໍລິການໃກ້ຄຽງຈາກບັນຫາຂອງທ່ານ

ລະບົບເວັບແອັບພລິເຄຊັນ ແລະ ແອັບມືຖື Android APK ແບບ Full-Stack (ຮອງຮັບທັງ **ມືຖື ແລະ ຄອມພິວເຕີ**) ພາສາລາວ 100%, ພັດທະນາດ້ວຍ **Nuxt 4 + Vuetify 4 + Pinia + Leaflet + Capacitor 8** ໃນຝັ່ງ Frontend ແລະ **Python 3.12 + FastAPI + SQLAlchemy + PostgreSQL** ໃນຝັ່ງ Backend.

---

## ຄຸນສົມບັດຫຼັກ

1. **ຄົ້ນຫາຮ້ານຈາກອາການ ຫຼື ບັນຫາທີ່ກຳລັງພົບ (`/`):**
   - ພິມອາການ ຫຼື ບັນຫາປະຈຳວັນດ້ວຍພາສາທຳມະດາ (ເຊັ່ນ: *"ລົດສະຕາດບໍ່ຕິດ ແລະ ມີສຽງດັງແກັກໆ"*, *"ເຄື່ອງຈັກມີຄວັນຂຶ້ນ"*, *"ຢາງລົດຮົ່ວ"*, *"ໜ້າຈໍໂທລະສັບແຕກ"*, *"ທໍ່ນ້ຳປະປາຮົ່ວ"*).
   - ລະບົບວິເຄາະອາການອັດສະລິຍະ ຊ່ວຍແນະນຳປະເພດຊ່າງທີ່ກົງຈຸດ ພ້ອມຄຳແນະນຳດ້ານຄວາມປອດໄພເບື້ອງຕົ້ນ.
   - ດຶງພິກັດ GPS ສົດຈາກອຸປະກອນ (ຫຼື ກົດ/ລາກໝຸດເທິງແຜນທີ່ດ້ວຍຕົນເອງ) ເພື່ອຄົ້ນຫາຮ້ານທີ່ **ຜ່ານການອະນຸມັດແລ້ວ** ໃກ້ໂຕທ່ານ ຈັດລຽງຕາມໄລຍະທາງຈິງ (`ກມ.`), ພ້ອມປຸ່ມ **ໂທຫາຮ້ານ** ແລະ **ນຳທາງຜ່ານ Google Maps** ໃນຄລິກດຽວ.

2. **ເຈົ້າຂອງຮ້ານເພີ່ມຮ້ານຂຶ້ນແຜນທີ່ໄດ້ເອງຟຣີ (`/shops/add` ແລະ `/shops/mine`):**
   - ເຈົ້າຂອງຮ້ານ ຫຼື ຊ່າງສ້ອມແປງ ສາມາດລົງທະບຽນ/ເຂົ້າສູ່ລະບົບ, ລະບຸບັນຫາທີ່ຮັບແກ້ໄຂ ແລະ **ປັກໝຸດຕຳແໜ່ງຮ້ານທີ່ຊັດເຈນ** ເທິງແຜນທີ່ (ຫຼື ກົດປຸ່ມ *"ໃຊ້ພິກັດ GPS ປັດຈຸບັນ"*).
   - ຮ້ານທີ່ສົ່ງເຂົ້າມາຈະຢູ່ໃນສະຖານະ **`PENDING` (ລໍຖ້າອະນຸມັດ)** ແລະ ແຈ້ງເຕືອນຫາຜູ້ດູແລລະບົບທັນທີ. ເຈົ້າຂອງຮ້ານສາມາດຕິດຕາມສະຖານະ ແລະ ແກ້ໄຂຂໍ້ມູນເພື່ອສົ່ງກວດຄືນໃໝ່ໄດ້.

3. **ໜ້າຜູ້ດູແລລະບົບກວດສອບ ແລະ ອະນຸມັດຮ້ານ (`/admin/approvals`):**
   - ກວດສອບລາຍລະອຽດຮ້ານທີ່ສົ່ງເຂົ້າມາ, ກວດພິກັດໝຸດເທິງແຜນທີ່ ແລ້ວກົດ **ອະນຸມັດ (`Approve`)** ເພື່ອເຜີຍແຜ່ຮ້ານຂຶ້ນແຜນທີ່ທັນທີ (ພ້ອມສົ່ງແຈ້ງເຕືອນຫາເຈົ້າຂອງຮ້ານ) ຫຼື **ປະຕິເສດ (`Reject`)** ພ້ອມລະບຸຄຳແນະນຳໃນການແກ້ໄຂ.

4. **ດີໄຊນ໌ຮອງຮັບທັງມືຖື ແລະ ຄອມພິວເຕີ + ຟອນພາສາລາວຝັງໃນໂຕ 100%:**
   - **ມືຖື (Mobile):** ແຖບເມນູລຸ່ມສຸດ (Footer Navigation) ກົດງ່າຍດ້ວຍມືດຽວ (ບໍ່ມີແຖບເມນູເທິງບັງໜ້າຈໍ), ສະຫຼັບມຸມມອງ ລາຍຊື່ຮ້ານ / ແຜນທີ່, ຮອງຮັບໂໝດແຈ້ງ ແລະ ໂໝດມືດ.
   - **ຄອມພິວເຕີ (Desktop):** ແຖບເມນູດ້ານເທິງ, ໜ້າຈໍແບ່ງຊ້າຍ-ຂວາ (ລາຍຊື່ຮ້ານ + ແຜນທີ່ໂຕ້ຕອບແບບ Sticky) ແລະ ໜ້າຈັດການຮ້ານສຳລັບ Admin.
   - **ຟອນພາສາລາວໃນໂຕ (Self-Hosted Lao Fonts):** ຝັງໄຟລ໌ຟອນ `Noto Sans Lao Looped` ແລະ `Noto Sans Lao` ໄວ້ໃນໂປຣເຈັກໂດຍກົງ (`frontend/public/fonts/` ແລະ `backend/app/static/fonts/`) ສະແດງຜົນພາສາລາວຄົມຊັດທຸກໜ້າຈໍ ລວມທັງໜ້າ `/docs` ໂດຍບໍ່ຕ້ອງເພິ່ງຟອນພາຍນອກ.

5. **ລະບົບສ້າງລາຍຮັບ Google AdSense (`/admin/approvals?tab=ADSENSE`, `/ads.txt`, `/privacy`):**
   - ຕິດຕັ້ງຊ່ອງໂຄສະນາ **In-Feed** (ແຊກລະຫວ່າງບັດລາຍຊື່ຮ້ານ) ແລະ **ປ້າຍໂຄສະນາທ້າຍໜ້າເວັບ (Responsive Banner)** ພ້ອມ `<meta name="google-adsense-account">` ແລະ ລະບົບ Auto Ads ຄົບຖ້ວນ.
   - ຕັ້ງຄ່າລະຫັດ Publisher ID (`ca-pub-4990570878383229`), Slot IDs (`6642734194`, `8750022785`), Auto Ads ແລະ **ໂໝດທົດລອງ (Preview / Test Mode)** ໄດ້ສົດໆຈາກໜ້າຜູ້ດູແລລະບົບ (ແຖບ `ໂຄສະນາ AdSense`) ຫຼື ຜ່ານໄຟລ໌ `.env`.
   - ສ້າງໄຟລ໌ `/ads.txt`, `/robots.txt` ແລະ ໜ້ານະໂຍບາຍຄວາມເປັນສ່ວນຕົວ (`/privacy`) ອັດຕະໂນມັດຕາມກົດລະບຽບຂອງ Google AdSense ແລະ ປິດໂຄສະນາເວັບອັດຕະໂນມັດເມື່ອເປີດໃຊ້ງານຜ່ານແອັບ Android APK (Capacitor), ໜ້າ `/login` ແລະ ໜ້າ `/admin/*`.

---

## ໂຄງສ້າງໂປຣເຈັກ

| ໂຟນເດີ / ໄຟລ໌ | ລາຍລະອຽດ |
| :--- | :--- |
| `backend/` | ລະບົບຫຼັງບ້ານ Python 3.12 + FastAPI + SQLAlchemy + PostgreSQL |
| `frontend/` | ລະບົບໜ້າບ້ານ Nuxt 4 + Vuetify 4 + Leaflet + Capacitor 8 Android |
| `dist/` | ບ່ອນເກັບໄຟລ໌ແອັບ Android APK ທີ່ສ້າງສຳເລັດແລ້ວ (`SearchWant-debug.apk`) |
| `.env.example` | ໄຟລ໌ຕົວຢ່າງການຕັ້ງຄ່າ Environment Variables ສຳລັບຖານຂໍ້ມູນ ແລະ Google AdSense |
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
- ເອກະສານ API ແບບໂຕ້ຕອບ (Swagger UI): http://localhost:8000/docs

### 2. ເປີດເຊີບເວີ Nuxt 4 + Vuetify 4 Frontend (Port `3000`)

ດັບເບິນຄລິກໄຟລ໌ `start-frontend.bat` ຫຼື ເປີດ Terminal ອີກໜ້າຕ່າງໜຶ່ງແລ້ວລັນ:

```powershell
cd frontend
npm.cmd run dev
```

- **ເປີດເທິງຄອມພິວເຕີ:** http://localhost:3000
- **ເປີດເທິງມືຖືຜ່ານ Wi-Fi ພ້ອມໃຊ້ GPS ສົດ (HTTPS Port `3443`):**
  ```powershell
  cd frontend
  npm.cmd run dev:https
  ```
  ຈາກນັ້ນເປີດໃນມືຖືທີ່ຕໍ່ Wi-Fi ດຽວກັນທີ່ `https://<IP-ຄອມພິວເຕີຂອງທ່ານ>:3443` *(ຫາກມືຖືເຂົ້າບໍ່ໄດ້ ໃຫ້ຄລິກຂວາທີ່ `allow-mobile-access.bat` ແລ້ວເລືອກ **Run as administrator** 1 ຄັ້ງ).*

---

## ບັນຊີທົດລອງທີ່ມີໃຫ້ພ້ອມ (ກົດເຂົ້າສູ່ລະບົບໃນຄລິກດຽວໄດ້ທີ່ໜ້າ `/login`)

| ບົດບາດ | ອີເມວ | ລະຫັດຜ່ານ | ສິ່ງທີ່ສາມາດທົດສອບໄດ້ |
| :--- | :--- | :--- | :--- |
| **ຜູ້ດູແລລະບົບ (Admin)** | `admin@searchwant.com` | `admin123` | ເຂົ້າໜ້າ **ອະນຸມັດຮ້ານ** ເພື່ອກວດສອບ/ອະນຸມັດຮ້ານໃໝ່ ແລະ ຕັ້ງຄ່າ **ໂຄສະນາ AdSense** |
| **ເຈົ້າຂອງຮ້ານ (Shop Owner)** | `owner@searchwant.com` | `owner123` | ເພີ່ມຮ້ານໃໝ່ເທິງແຜນທີ່, ປັກໝຸດພິກັດ GPS ແລະ ຕິດຕາມການແຈ້ງເຕືອນຜົນອະນຸມັດ |
| **ລູກຄ້າທົ່ວໄປ (Customer)** | `user@searchwant.com` | `user123` | ພິມບັນຫາລົດ/ໂທລະສັບ/ໄຟຟ້າ-ປະປາ ເພື່ອຄົ້ນຫາຮ້ານໃກ້ຄຽງ, ໂທຫາຮ້ານ ແລະ ນຳທາງ |

---

## ການເປີດຮັບລາຍຮັບຈິງຈາກ Google AdSense (ເມື່ອນຳເວັບຂຶ້ນໂດເມນຈິງ)

ປັດຈຸບັນລະບົບໄດ້ຜູກລະຫັດບັນຊີ Google AdSense ໄວ້ພ້ອມແລ້ວ (`ca-pub-4990570878383229`, In-Feed Slot: `6642734194`, Banner Slot: `8750022785`). ເມື່ອທ່ານນຳເວັບໄຊຂຶ້ນເຊີບເວີຈິງ ໃຫ້ປະຕິບັດ 3 ຂັ້ນຕອນດັ່ງນີ້:

1. **ອັບເວັບຂຶ້ນໂດເມນຈິງ (HTTPS):** ເຊັ່ນ `.com` ຫຼື `.la` ແລະ ກວດສອບວ່າ `https://ໂດເມນຂອງທ່ານ/ads.txt` ສະແດງຂໍ້ຄວາມ:
   ```text
   google.com, pub-4990570878383229, DIRECT, f08c47fec0942fa0
   ```
2. **ສົ່ງໂດເມນໃຫ້ Google AdSense ອະນຸມັດ:** ເຂົ້າໄປທີ່ເວັບໄຊ Google AdSense -> ເມນູ **Sites** -> ກົດ **Add site** ໃສ່ຊື່ໂດເມນຂອງທ່ານ ແລະ ລໍຖ້າຈົນສະຖານະປ່ຽນເປັນ **`Ready`**.
3. **ປິດໂໝດທົດລອງເພື່ອຮັບໂຄສະນາຈິງ:** ເຂົ້າສູ່ລະບົບ Admin ທີ່ໜ້າ `/admin/approvals?tab=ADSENSE` -> ປິດປຸ່ມ **ໂໝດທົດລອງ (Preview / Test Mode)** -> ກົດ **ບັນທຶກການຕັ້ງຄ່າ** ເພື່ອໃຫ້ Google ສະແດງໂຄສະນາຈິງ 100%.

---

## ການສ້າງໄຟລ໌ແອັບ Android APK (Capacitor 8)

ໂປຣເຈັກນີ້ໃຊ້ **Capacitor 8** ຫຸ້ມລະບົບເວັບ Nuxt 4 ເພື່ອສ້າງເປັນໄຟລ໌ແອັບມືຖື Android APK ຈາກໂຄ້ດຊຸດດຽວກັນ.

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

ສາມາດກວດສອບຄວາມຖືກຕ້ອງຂອງລະບົບ API ແລະ AdSense ທັງໝົດດ້ວຍ Pytest:

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```
