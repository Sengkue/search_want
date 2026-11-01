<template>
  <v-app>
    <!-- DESKTOP ONLY Top Navbar (CSS-hidden on Mobile for zero SSR hydration flash) -->
    <v-app-bar
      elevation="0"
      color="transparent"
      height="58"
      class="px-4 sw-desktop-navbar sw-desktop-only"
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
          :aria-label="isDark ? 'ປ່ຽນເປັນໂໝດແຈ້ງ' : 'ປ່ຽນເປັນໂໝດມືດ'"
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
            <v-btn
              icon
              variant="text"
              size="small"
              aria-label="ການແຈ້ງເຕືອນ"
              title="ການແຈ້ງເຕືອນ"
              v-bind="menuProps"
              @click="authStore.fetchNotifications()"
            >
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
                  :color="authStore.isSuperAdmin ? 'deep-purple' : 'warning'"
                  variant="flat"
                  class="ml-1 font-weight-bold text-white"
                >
                  {{ authStore.isSuperAdmin ? 'ສູງສຸດ' : 'ຜູ້ດູແລ' }}
                </v-chip>
              </v-btn>
            </template>

            <v-card min-width="235" class="pa-2">
              <div class="px-3 py-2">
                <div class="font-weight-bold text-body-medium">{{ authStore.user.full_name }}</div>
                <div class="text-body-small text-medium-emphasis">{{ authStore.user.email }}</div>
                <v-chip
                  size="x-small"
                  :color="authStore.isSuperAdmin ? 'deep-purple' : authStore.isAdmin ? 'warning' : 'primary'"
                  variant="tonal"
                  class="mt-1 font-weight-bold"
                >
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
                  v-if="authStore.isSuperAdmin"
                  to="/admin/approvals?tab=RBAC"
                  prepend-icon="mdi-shield-crown-outline"
                  title="ສິດຜູ້ໃຊ້ & Production"
                />
                <v-list-item
                  prepend-icon="mdi-key-change"
                  title="ປ່ຽນລະຫັດຜ່ານ"
                  @click="openPasswordDialog"
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

    <!-- Main Page Content (CSS-first zero-CLS responsive clearance for Mobile Footer) -->
    <v-main class="sw-main-content" :class="{ 'is-keyboard-open': isMobileKeyboardOpen }">
      <slot />

      <!-- Mandatory Google AdSense Policy Compliance & Sitemap SEO Footer -->
      <footer class="text-center py-3 px-3 text-body-small text-medium-emphasis" style="font-size: 11.5px">
        <span>Search-Want</span>
        <span class="mx-1">•</span>
        <NuxtLink to="/privacy" class="text-primary text-decoration-none font-weight-medium">
          ນະໂຍບາຍຄວາມເປັນສ່ວນຕົວ &amp; ໂຄສະນາ
        </NuxtLink>
        <span class="mx-1">•</span>
        <a href="/sitemap.xml" target="_blank" class="text-medium-emphasis text-decoration-none">
          ແຜນຜັງເວັບໄຊ (Sitemap)
        </a>
        <span class="mx-1">•</span>
        <a href="/ads.txt" target="_blank" class="text-medium-emphasis text-decoration-none">
          ads.txt
        </a>
      </footer>
    </v-main>

    <!-- MOBILE ONLY Sleek Bottom Footer Bar (Auto-hides while virtual keyboard is open on phones) -->
    <nav
      class="sw-mobile-footer sw-mobile-only"
      :class="{ 'is-keyboard-open': isMobileKeyboardOpen }"
      aria-label="ເມນູຫຼັກມືຖື"
    >
      <NuxtLink
        to="/"
        class="sw-footer-item"
        :class="{ 'is-active': route.path === '/' }"
        @click="handleMobileSearchNavTap"
      >
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

          <div class="d-flex ga-2 mb-2">
            <v-btn
              color="primary"
              variant="tonal"
              size="small"
              class="flex-grow-1"
              prepend-icon="mdi-key-change"
              @click="mobileMenuOpen = false; openPasswordDialog()"
            >
              ປ່ຽນລະຫັດຜ່ານ
            </v-btn>
            <v-btn
              v-if="authStore.isSuperAdmin"
              to="/admin/approvals?tab=RBAC"
              color="deep-purple"
              variant="tonal"
              size="small"
              class="flex-grow-1"
              prepend-icon="mdi-shield-crown-outline"
              @click="mobileMenuOpen = false"
            >
              ຈັດການສິດ
            </v-btn>
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

    <!-- Self-Service Password Rotation Dialog (Revokes old tokens across other devices) -->
    <v-dialog v-model="passwordDialogOpen" max-width="420">
      <v-card rounded="xl" class="pa-4 pa-md-5">
        <div class="d-flex align-center justify-space-between mb-2">
          <div class="text-title-medium font-weight-bold d-flex align-center ga-2">
            <v-icon icon="mdi-lock-reset" color="primary" size="20" />
            <span>ປ່ຽນລະຫັດຜ່ານໃໝ່</span>
          </div>
          <v-btn icon="mdi-close" variant="text" size="x-small" @click="passwordDialogOpen = false" />
        </div>
        <p class="text-body-small text-medium-emphasis mb-3">
          ເມື່ອປ່ຽນລະຫັດຜ່ານແລ້ວ ເຊດຊັນທີ່ເຄີຍເຂົ້າສູ່ລະບົບໄວ້ໃນເຄື່ອງອື່ນຈະຖືກຍົກເລີກທັນທີເພື່ອຄວາມປອດໄພ.
        </p>

        <v-alert
          v-if="pwError"
          type="error"
          variant="tonal"
          density="compact"
          class="mb-3 text-body-small"
        >
          {{ pwError }}
        </v-alert>

        <v-form @submit.prevent="submitPasswordChange">
          <v-text-field
            v-model="pwForm.currentPassword"
            label="ລະຫັດຜ່ານປັດຈຸບັນ"
            type="password"
            prepend-inner-icon="mdi-lock-outline"
            required
            class="mb-2"
          />
          <v-text-field
            v-model="pwForm.newPassword"
            label="ລະຫັດຜ່ານໃໝ່ (ຢ່າງໜ້ອຍ 8 ຕົວອັກສອນ)"
            type="password"
            prepend-inner-icon="mdi-lock-plus-outline"
            required
            class="mb-2"
          />
          <v-text-field
            v-model="pwForm.confirmPassword"
            label="ຢືນຢັນລະຫັດຜ່ານໃໝ່"
            type="password"
            prepend-inner-icon="mdi-lock-check-outline"
            required
            class="mb-3"
          />
          <div class="d-flex justify-end ga-2">
            <v-btn variant="text" size="small" @click="passwordDialogOpen = false">ຍົກເລີກ</v-btn>
            <v-btn
              type="submit"
              color="primary"
              variant="flat"
              size="small"
              :loading="savingPassword"
              prepend-icon="mdi-content-save-check"
            >
              ບັນທຶກລະຫັດຜ່ານໃໝ່
            </v-btn>
          </div>
        </v-form>
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

    <!-- Lazy Client-Only Helper Dialogs (Zero SSR DOM & zero initial hydration overhead until opened) -->
    <ClientOnly>
      <LazyMobileInstallDialog v-if="installDialogOpen" v-model="installDialogOpen" />
      <LazyGpsSecureOriginDialog />
    </ClientOnly>
  </v-app>
</template>

<script setup lang="ts">
import { useDisplay, useTheme } from 'vuetify'
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
const passwordDialogOpen = ref(false)
const savingPassword = ref(false)
const pwError = ref('')
const pwForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})

function openPasswordDialog() {
  pwError.value = ''
  pwForm.currentPassword = ''
  pwForm.newPassword = ''
  pwForm.confirmPassword = ''
  passwordDialogOpen.value = true
}

async function submitPasswordChange() {
  pwError.value = ''
  if (pwForm.newPassword.length < 8) {
    pwError.value = 'ລະຫັດຜ່ານໃໝ່ຕ້ອງມີຢ່າງໜ້ອຍ 8 ຕົວອັກສອນ.'
    return
  }
  if (pwForm.newPassword !== pwForm.confirmPassword) {
    pwError.value = 'ລະຫັດຜ່ານໃໝ່ ແລະ ຢືນຢັນລະຫັດຜ່ານບໍ່ກົງກັນ.'
    return
  }
  savingPassword.value = true
  try {
    await authStore.changePassword(pwForm.currentPassword, pwForm.newPassword)
    passwordDialogOpen.value = false
  } catch (err: any) {
    pwError.value = err?.data?.detail || 'ປ່ຽນລະຫັດຜ່ານບໍ່ສຳເລັດ.'
  } finally {
    savingPassword.value = false
  }
}

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

// Keyboard-aware Mobile Bottom Navigation: auto-hides fixed footer when phone virtual keyboard opens
const hasFocusedTextInput = ref(false)
const viewportShrunkForKeyboard = ref(false)
let focusOutTimer: ReturnType<typeof setTimeout> | null = null
let maxObservedViewportHeight = 0

const NON_KEYBOARD_INPUT_TYPES = new Set([
  'button',
  'submit',
  'reset',
  'checkbox',
  'radio',
  'range',
  'file',
  'color',
  'hidden',
  'image',
])

function isTextEditableElement(el: Element | null): boolean {
  if (!el) return false
  if (el instanceof HTMLTextAreaElement) return !el.readOnly && !el.disabled
  if (el instanceof HTMLInputElement) {
    return !el.readOnly && !el.disabled && !NON_KEYBOARD_INPUT_TYPES.has((el.type || 'text').toLowerCase())
  }
  return (el as HTMLElement).isContentEditable === true
}

function handleGlobalFocusIn(e: FocusEvent) {
  if (focusOutTimer) {
    clearTimeout(focusOutTimer)
    focusOutTimer = null
  }
  if (isTextEditableElement(e.target as Element | null)) {
    hasFocusedTextInput.value = true
  }
}

function handleGlobalFocusOut() {
  if (focusOutTimer) clearTimeout(focusOutTimer)
  focusOutTimer = setTimeout(() => {
    hasFocusedTextInput.value = isTextEditableElement(document.activeElement)
  }, 70)
}

function handleVisualViewportResize() {
  if (!import.meta.client) return
  const vv = window.visualViewport
  if (!vv) return
  const currentHeight = vv.height
  if (currentHeight > maxObservedViewportHeight) {
    maxObservedViewportHeight = currentHeight
  }
  const referenceHeight = Math.max(window.screen?.availHeight ? Math.min(window.innerHeight, maxObservedViewportHeight) : maxObservedViewportHeight, window.innerHeight)
  viewportShrunkForKeyboard.value = referenceHeight - currentHeight > 130
}

function handleWindowOrientationChange() {
  maxObservedViewportHeight = 0
  viewportShrunkForKeyboard.value = false
}

const isMobileKeyboardOpen = computed(
  () => smAndDown.value && (hasFocusedTextInput.value || viewportShrunkForKeyboard.value),
)

function handleMobileSearchNavTap() {
  if (import.meta.client) {
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur()
    }
    if (route.path === '/') {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
}

onMounted(() => {
  authStore.initAuth()
  loadAdSenseConfig()
  const standalone =
    window.matchMedia?.('(display-mode: standalone)').matches ||
    Boolean((window.navigator as any)?.standalone)
  showInstallButton.value = !isNativeApp() && !standalone

  maxObservedViewportHeight = window.visualViewport?.height || window.innerHeight
  document.addEventListener('focusin', handleGlobalFocusIn, { passive: true })
  document.addEventListener('focusout', handleGlobalFocusOut, { passive: true })
  window.visualViewport?.addEventListener('resize', handleVisualViewportResize, { passive: true })
  window.addEventListener('orientationchange', handleWindowOrientationChange, { passive: true })
})

onBeforeUnmount(() => {
  if (focusOutTimer) clearTimeout(focusOutTimer)
  document.removeEventListener('focusin', handleGlobalFocusIn)
  document.removeEventListener('focusout', handleGlobalFocusOut)
  window.visualViewport?.removeEventListener('resize', handleVisualViewportResize)
  window.removeEventListener('orientationchange', handleWindowOrientationChange)
})
</script>
