<template>
  <v-app>
    <!-- DESKTOP ONLY Top Navbar (Hidden completely on Mobile Phones per UX best-practice) -->
    <v-app-bar
      v-if="!smAndDown"
      elevation="0"
      color="transparent"
      height="58"
      class="px-4 sw-desktop-navbar"
    >
      <NuxtLink to="/" class="d-flex align-center text-decoration-none text-high-emphasis ga-2 mr-4">
        <BrandLogo :size="36" />
        <div>
          <div class="text-title-small font-weight-black" style="line-height: 1.25">
            Search-Want
          </div>
          <div class="text-body-small text-medium-emphasis" style="font-size: 11px; line-height: 1.35">
            ຊອກຫາຮ້ານສ້ອມແປງໃກ້ທ່ານ
          </div>
        </div>
      </NuxtLink>

      <!-- Desktop Primary Navigation Pills -->
      <div class="d-flex align-center ga-1">
        <v-btn
          to="/"
          size="small"
          :variant="route.path === '/' ? 'tonal' : 'text'"
          :color="route.path === '/' ? 'primary' : undefined"
          prepend-icon="mdi-compass-outline"
        >
          ຄົ້ນຫາຮ້ານໃກ້ຄຽງ
        </v-btn>

        <v-btn
          to="/shops/add"
          size="small"
          :variant="route.path === '/shops/add' ? 'tonal' : 'text'"
          :color="route.path === '/shops/add' ? 'primary' : undefined"
          prepend-icon="mdi-store-plus-outline"
        >
          ເພີ່ມຮ້ານຂອງຂ້ອຍ
        </v-btn>

        <v-btn
          v-if="authStore.isLoggedIn"
          to="/shops/mine"
          size="small"
          :variant="route.path === '/shops/mine' ? 'tonal' : 'text'"
          :color="route.path === '/shops/mine' ? 'primary' : undefined"
          prepend-icon="mdi-storefront-outline"
        >
          ຮ້ານຂອງຂ້ອຍ
        </v-btn>

        <v-btn
          v-if="authStore.isAdmin"
          to="/admin/approvals"
          size="small"
          :variant="route.path.startsWith('/admin') ? 'flat' : 'tonal'"
          color="warning"
          prepend-icon="mdi-shield-check-outline"
        >
          ອະນຸມັດຮ້ານ
        </v-btn>
      </div>

      <v-spacer />

      <!-- Desktop Right Controls -->
      <div class="d-flex align-center ga-1">
        <v-btn
          v-if="showInstallButton"
          color="success"
          variant="tonal"
          size="small"
          prepend-icon="mdi-cellphone-arrow-down"
          @click="installDialogOpen = true"
        >
          ຕິດຕັ້ງ APK
        </v-btn>

        <v-btn
          icon
          variant="text"
          size="small"
          :title="isDark ? 'ປ່ຽນເປັນໂໝດແຈ້ງ' : 'ປ່ຽນເປັນໂໝດມືດ'"
          @click="toggleTheme"
        >
          <v-icon :icon="isDark ? 'mdi-weather-sunny' : 'mdi-weather-night'" size="20" />
        </v-btn>

        <!-- Desktop Notifications Bell -->
        <v-menu
          v-if="authStore.isLoggedIn"
          location="bottom end"
          max-width="360"
          :close-on-content-click="false"
        >
          <template #activator="{ props: menuProps }">
            <v-btn icon variant="text" size="small" v-bind="menuProps" @click="authStore.fetchNotifications()">
              <v-badge
                v-if="authStore.unreadCount > 0"
                :content="authStore.unreadCount"
                color="error"
              >
                <v-icon icon="mdi-bell-outline" size="20" />
              </v-badge>
              <v-icon v-else icon="mdi-bell-outline" size="20" />
            </v-btn>
          </template>

          <v-card width="340" class="pa-0 overflow-hidden">
            <div class="d-flex align-center justify-space-between px-4 py-2 bg-primary text-white">
              <div class="font-weight-bold text-body-medium">
                ການແຈ້ງເຕືອນ (ຍັງບໍ່ອ່ານ {{ authStore.unreadCount }})
              </div>
              <v-btn
                v-if="authStore.unreadCount > 0"
                variant="text"
                size="x-small"
                color="white"
                @click="authStore.markAllNotificationsRead()"
              >
                ອ່ານທັງໝົດແລ້ວ
              </v-btn>
            </div>

            <v-list
              v-if="authStore.notifications.length"
              lines="two"
              max-height="340"
              class="overflow-y-auto py-0"
            >
              <template v-for="(n, index) in authStore.notifications" :key="n.id">
                <v-list-item
                  :class="!n.is_read ? (isDark ? 'bg-grey-darken-4' : 'bg-blue-lighten-5') : ''"
                  @click="handleNotificationClick(n.id, n.link_url)"
                >
                  <template #prepend>
                    <v-avatar :color="notifColor(n.notif_type)" size="30" variant="tonal">
                      <v-icon :icon="notifIcon(n.notif_type)" size="16" />
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-body-small font-weight-bold">
                    {{ n.title }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-body-small">
                    {{ n.message }}
                  </v-list-item-subtitle>
                </v-list-item>
                <v-divider v-if="index < authStore.notifications.length - 1" />
              </template>
            </v-list>

            <div v-else class="pa-5 text-center text-medium-emphasis text-body-small">
              ຍັງບໍ່ມີການແຈ້ງເຕືອນໃໝ່
            </div>
          </v-card>
        </v-menu>

        <!-- Desktop User Menu / Login -->
        <template v-if="authStore.isLoggedIn && authStore.user">
          <v-menu location="bottom end">
            <template #activator="{ props: userMenuProps }">
              <v-btn
                v-bind="userMenuProps"
                variant="tonal"
                color="primary"
                size="small"
                class="ml-1"
                prepend-icon="mdi-account-circle-outline"
              >
                <span class="text-truncate" style="max-width: 120px">
                  {{ authStore.user.full_name }}
                </span>
                <v-chip
                  v-if="authStore.isAdmin"
                  size="x-small"
                  color="warning"
                  variant="flat"
                  class="ml-1 font-weight-bold"
                >
                  ຜູ້ດູແລ
                </v-chip>
              </v-btn>
            </template>

            <v-card min-width="220" class="pa-2">
              <div class="px-3 py-2">
                <div class="font-weight-bold text-body-medium">{{ authStore.user.full_name }}</div>
                <div class="text-body-small text-medium-emphasis">{{ authStore.user.email }}</div>
                <v-chip size="x-small" color="primary" variant="tonal" class="mt-1">
                  {{ roleLabel(authStore.user.role) }}
                </v-chip>
              </div>
              <v-divider class="my-1" />
              <v-list density="compact" nav>
                <v-list-item to="/shops/add" prepend-icon="mdi-store-plus-outline" title="ເພີ່ມຮ້ານຂອງຂ້ອຍ" />
                <v-list-item to="/shops/mine" prepend-icon="mdi-storefront-outline" title="ຮ້ານຂອງຂ້ອຍ" />
                <v-list-item
                  v-if="authStore.isAdmin"
                  to="/admin/approvals"
                  prepend-icon="mdi-shield-check-outline"
                  title="ອະນຸມັດຮ້ານ"
                />
                <v-list-item
                  prepend-icon="mdi-logout"
                  title="ອອກຈາກລະບົບ"
                  base-color="error"
                  @click="handleLogout"
                />
              </v-list>
            </v-card>
          </v-menu>
        </template>

        <v-btn
          v-else
          to="/login"
          color="primary"
          variant="flat"
          size="small"
          prepend-icon="mdi-login"
          class="ml-1"
        >
          ເຂົ້າສູ່ລະບົບ
        </v-btn>
      </div>
    </v-app-bar>

    <!-- Main Page Content (No top navbar offset on Mobile; clean bottom clearance for Mobile Footer) -->
    <v-main :style="smAndDown ? 'padding-bottom: 68px' : ''">
      <slot />
    </v-main>

    <!-- MOBILE ONLY Sleek Bottom Footer Bar (Replaces top navbar completely on phone screens) -->
    <nav v-if="smAndDown" class="sw-mobile-footer" aria-label="ເມນູຫຼັກມືຖື">
      <NuxtLink to="/" class="sw-footer-item" :class="{ 'is-active': route.path === '/' }">
        <span class="sw-footer-icon-pill">
          <v-icon :icon="route.path === '/' ? 'mdi-compass' : 'mdi-compass-outline'" size="20" />
        </span>
        <span>ຄົ້ນຫາ</span>
      </NuxtLink>

      <NuxtLink
        to="/shops/add"
        class="sw-footer-item"
        :class="{ 'is-active': route.path === '/shops/add' }"
      >
        <span class="sw-footer-icon-pill">
          <v-icon
            :icon="route.path === '/shops/add' ? 'mdi-store-plus' : 'mdi-store-plus-outline'"
            size="20"
          />
        </span>
        <span>ເພີ່ມຮ້ານ</span>
      </NuxtLink>

      <NuxtLink
        v-if="authStore.isLoggedIn"
        to="/shops/mine"
        class="sw-footer-item"
        :class="{ 'is-active': route.path === '/shops/mine' }"
      >
        <span class="sw-footer-icon-pill">
          <v-icon
            :icon="route.path === '/shops/mine' ? 'mdi-storefront' : 'mdi-storefront-outline'"
            size="20"
          />
        </span>
        <span>ຮ້ານຂ້ອຍ</span>
      </NuxtLink>

      <NuxtLink
        v-if="authStore.isAdmin"
        to="/admin/approvals"
        class="sw-footer-item"
        :class="{ 'is-active': route.path.startsWith('/admin') }"
      >
        <span class="sw-footer-icon-pill">
          <v-icon
            :icon="route.path.startsWith('/admin') ? 'mdi-shield-check' : 'mdi-shield-check-outline'"
            size="20"
          />
        </span>
        <span>ອະນຸມັດ</span>
      </NuxtLink>

      <NuxtLink
        v-if="!authStore.isLoggedIn"
        to="/login"
        class="sw-footer-item"
        :class="{ 'is-active': route.path === '/login' }"
      >
        <span class="sw-footer-icon-pill">
          <v-icon
            :icon="route.path === '/login' ? 'mdi-account-circle' : 'mdi-account-circle-outline'"
            size="20"
          />
        </span>
        <span>ເຂົ້າລະບົບ</span>
      </NuxtLink>

      <button
        type="button"
        class="sw-footer-item"
        :class="{ 'is-active': mobileMenuOpen }"
        @click="openMobileMenu"
      >
        <span class="sw-footer-icon-pill position-relative">
          <v-badge
            v-if="authStore.unreadCount > 0"
            :content="authStore.unreadCount"
            color="error"
            floating
          >
            <v-icon icon="mdi-dots-horizontal-circle-outline" size="20" />
          </v-badge>
          <v-icon v-else icon="mdi-dots-horizontal-circle-outline" size="20" />
        </span>
        <span>ເມນູ</span>
      </button>
    </nav>

    <!-- Mobile Quick Menu / Account / Notifications / APK Sheet -->
    <v-dialog v-model="mobileMenuOpen" max-width="420">
      <v-card rounded="xl" class="sw-hero-card pa-4">
        <div class="d-flex align-center justify-space-between mb-3">
          <div class="d-flex align-center ga-2">
            <BrandLogo :size="36" />
            <div>
              <div class="text-title-small font-weight-black">Search-Want</div>
              <div class="text-body-small text-medium-emphasis">ຕັ້ງຄ່າ &amp; ບັນຊີຂອງທ່ານ</div>
            </div>
          </div>
          <v-btn icon="mdi-close" variant="text" size="x-small" @click="mobileMenuOpen = false" />
        </div>

        <!-- Account Summary or Sign-In Prompt -->
        <v-sheet
          v-if="authStore.isLoggedIn && authStore.user"
          rounded="lg"
          class="pa-3 mb-3 border"
          color="background"
        >
          <div class="d-flex align-center justify-space-between">
            <div>
              <div class="text-title-small font-weight-bold">{{ authStore.user.full_name }}</div>
              <div class="text-body-small text-medium-emphasis">{{ authStore.user.email }}</div>
            </div>
            <v-chip size="x-small" color="primary" variant="tonal" class="font-weight-bold">
              {{ roleLabel(authStore.user.role) }}
            </v-chip>
          </div>
        </v-sheet>

        <v-btn
          v-else
          to="/login"
          color="primary"
          variant="flat"
          block
          prepend-icon="mdi-login"
          class="mb-3"
          @click="mobileMenuOpen = false"
        >
          ເຂົ້າສູ່ລະບົບ / ສ້າງບັນຊີໃໝ່
        </v-btn>

        <!-- Quick Utility Buttons (Install APK & Dark Mode) -->
        <div class="d-flex ga-2 mb-3">
          <v-btn
            v-if="showInstallButton"
            color="success"
            variant="tonal"
            size="small"
            class="flex-grow-1"
            prepend-icon="mdi-android"
            @click="mobileMenuOpen = false; installDialogOpen = true"
          >
            ຕິດຕັ້ງ APK
          </v-btn>
          <v-btn
            variant="tonal"
            color="secondary"
            size="small"
            class="flex-grow-1"
            :prepend-icon="isDark ? 'mdi-weather-sunny' : 'mdi-weather-night'"
            @click="toggleTheme"
          >
            {{ isDark ? 'ໂໝດແຈ້ງ' : 'ໂໝດມືດ' }}
          </v-btn>
        </div>

        <!-- Notifications Section (if logged in) -->
        <template v-if="authStore.isLoggedIn">
          <div class="d-flex align-center justify-space-between mb-1">
            <span class="text-body-small font-weight-bold text-medium-emphasis">
              ການແຈ້ງເຕືອນ ({{ authStore.unreadCount }} ໃໝ່)
            </span>
            <v-btn
              v-if="authStore.unreadCount > 0"
              variant="text"
              size="x-small"
              color="primary"
              @click="authStore.markAllNotificationsRead()"
            >
              ອ່ານທັງໝົດແລ້ວ
            </v-btn>
          </div>

          <v-sheet
            v-if="authStore.notifications.length"
            rounded="lg"
            border
            class="overflow-y-auto mb-3"
            style="max-height: 190px"
          >
            <v-list density="compact" lines="two" class="py-0">
              <template v-for="(n, idx) in authStore.notifications.slice(0, 6)" :key="n.id">
                <v-list-item
                  @click="mobileMenuOpen = false; handleNotificationClick(n.id, n.link_url)"
                >
                  <template #prepend>
                    <v-icon :icon="notifIcon(n.notif_type)" :color="notifColor(n.notif_type)" size="18" class="mr-2" />
                  </template>
                  <v-list-item-title class="text-body-small font-weight-bold">
                    {{ n.title }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-body-small">
                    {{ n.message }}
                  </v-list-item-subtitle>
                </v-list-item>
                <v-divider v-if="idx < Math.min(authStore.notifications.length, 6) - 1" />
              </template>
            </v-list>
          </v-sheet>
          <div v-else class="text-body-small text-medium-emphasis text-center py-2 mb-2">
            ຍັງບໍ່ມີການແຈ້ງເຕືອນ
          </div>

          <v-btn
            color="error"
            variant="tonal"
            size="small"
            block
            prepend-icon="mdi-logout"
            @click="mobileMenuOpen = false; handleLogout()"
          >
            ອອກຈາກລະບົບ
          </v-btn>
        </template>
      </v-card>
    </v-dialog>

    <!-- Global Notification Toast -->
    <v-snackbar
      v-model="authStore.toast.show"
      :color="authStore.toast.color"
      :location="smAndDown ? 'top' : 'top right'"
      timeout="3800"
      rounded="lg"
      elevation="4"
    >
      <div class="d-flex align-center ga-2 text-body-small">
        <v-icon :icon="authStore.toast.icon" size="18" />
        <span class="font-weight-medium">{{ authStore.toast.message }}</span>
      </div>
      <template #actions>
        <v-btn icon="mdi-close" size="x-small" variant="text" @click="authStore.toast.show = false" />
      </template>
    </v-snackbar>

    <!-- Automatic Mobile APK / App Install Prompt Dialog -->
    <MobileInstallDialog v-model="installDialogOpen" />

    <!-- Smart GPS HTTPS / Localhost / Map-Pin Helper Dialog -->
    <GpsSecureOriginDialog />
  </v-app>
</template>

<script setup lang="ts">
import { useDisplay, useTheme } from 'vuetify'
import MobileInstallDialog from '~/components/MobileInstallDialog.vue'
import { useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const { isNativeApp } = useApi()
const { loadAdSenseConfig, registerAdSenseHead } = useAdSense()
const route = useRoute()
const router = useRouter()
const { smAndDown } = useDisplay()
const { roleLabel } = useLabels()
const theme = useTheme()

registerAdSenseHead()

const installDialogOpen = ref(false)
const showInstallButton = ref(false)
const mobileMenuOpen = ref(false)

const isDark = computed(() => theme.global.current.value.dark)

function toggleTheme() {
  theme.global.name.value = isDark.value ? 'searchWantLight' : 'searchWantDark'
}

function openMobileMenu() {
  if (authStore.isLoggedIn) {
    authStore.fetchNotifications()
  }
  mobileMenuOpen.value = true
}

function notifColor(type: string): string {
  if (type === 'SHOP_APPROVED') return 'success'
  if (type === 'SHOP_REJECTED') return 'error'
  if (type === 'SHOP_PENDING') return 'warning'
  return 'primary'
}

function notifIcon(type: string): string {
  if (type === 'SHOP_APPROVED') return 'mdi-check-decagram'
  if (type === 'SHOP_REJECTED') return 'mdi-alert-circle'
  if (type === 'SHOP_PENDING') return 'mdi-clock-alert-outline'
  return 'mdi-bell-ring-outline'
}

async function handleNotificationClick(id: number, linkUrl: string | null) {
  await authStore.markNotificationRead(id)
  if (linkUrl) {
    router.push(linkUrl)
  }
}

function handleLogout() {
  authStore.logout()
  router.push('/')
}

onMounted(() => {
  authStore.initAuth()
  loadAdSenseConfig()
  const standalone =
    window.matchMedia?.('(display-mode: standalone)').matches ||
    Boolean((window.navigator as any)?.standalone)
  showInstallButton.value = !isNativeApp() && !standalone
})
</script>
