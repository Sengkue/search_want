<template>
  <v-container class="py-4 py-md-10 px-3" style="max-width: 460px">
    <v-card class="sw-hero-card pa-4 pa-md-6">
      <!-- Friendly Compact Header with Signature App Icon -->
      <div class="text-center mb-3">
        <div class="d-flex justify-center mb-2">
          <BrandLogo :size="54" />
        </div>
        <h1 class="text-title-large font-weight-black">ຍິນດີຕ້ອນຮັບສູ່ Search-Want</h1>
        <p class="text-body-small text-medium-emphasis mt-1 mb-0">
          ເຂົ້າສູ່ລະບົບເພື່ອເພີ່ມຮ້ານຂອງທ່ານ, ຕິດຕາມສະຖານະ ຫຼື ອະນຸມັດຮ້ານ
        </p>
      </div>

      <!-- Primary Login / Register Tabs First (Clear & Non-Confusing) -->
      <v-tabs v-model="tab" grow color="primary" density="compact" class="mb-3">
        <v-tab value="login">ເຂົ້າສູ່ລະບົບ</v-tab>
        <v-tab value="register">ສ້າງບັນຊີ</v-tab>
      </v-tabs>

      <v-alert v-if="errorMsg" type="error" variant="tonal" density="compact" class="mb-3 text-body-small">
        {{ errorMsg }}
      </v-alert>

      <!-- Sign In Form -->
      <v-form v-if="tab === 'login'" @submit.prevent="submitLogin">
        <v-text-field
          v-model="loginForm.email"
          label="ອີເມວ"
          type="email"
          prepend-inner-icon="mdi-email-outline"
          required
          class="mb-2"
        />
        <v-text-field
          v-model="loginForm.password"
          label="ລະຫັດຜ່ານ"
          :type="showPass ? 'text' : 'password'"
          prepend-inner-icon="mdi-lock-outline"
          :append-inner-icon="showPass ? 'mdi-eye-off' : 'mdi-eye'"
          required
          class="mb-3"
          @click:append-inner="showPass = !showPass"
        />
        <v-btn
          type="submit"
          color="primary"
          variant="flat"
          block
          :loading="submitting"
          prepend-icon="mdi-login"
        >
          ເຂົ້າສູ່ລະບົບ
        </v-btn>
      </v-form>

      <!-- Register Form -->
      <v-form v-else @submit.prevent="submitRegister">
        <v-text-field
          v-model="regForm.full_name"
          label="ຊື່ຂອງທ່ານ ຫຼື ຊື່ເຈົ້າຂອງທຸລະກິດ"
          prepend-inner-icon="mdi-account-outline"
          required
          class="mb-2"
        />
        <v-text-field
          v-model="regForm.email"
          label="ອີເມວ"
          type="email"
          prepend-inner-icon="mdi-email-outline"
          required
          class="mb-2"
        />
        <v-text-field
          v-model="regForm.phone"
          label="ເບີໂທ (ບໍ່ບັງຄັບ)"
          placeholder="+856 20 5555 1234"
          prepend-inner-icon="mdi-phone-outline"
          class="mb-2"
        />
        <v-text-field
          v-model="regForm.password"
          label="ລະຫັດຜ່ານ (ຢ່າງໜ້ອຍ 6 ຕົວອັກສອນ)"
          :type="showPass ? 'text' : 'password'"
          prepend-inner-icon="mdi-lock-outline"
          :append-inner-icon="showPass ? 'mdi-eye-off' : 'mdi-eye'"
          required
          class="mb-3"
          @click:append-inner="showPass = !showPass"
        />
        <v-btn
          type="submit"
          color="primary"
          variant="flat"
          block
          :loading="submitting"
          prepend-icon="mdi-account-plus"
        >
          ສ້າງບັນຊີ
        </v-btn>
      </v-form>

      <!-- Tidy 1-Tap Demo Role Switcher (Automatically Hidden in Production / DEMO_MODE=false) -->
      <template v-if="authStore.publicConfig.demo_mode">
        <v-divider class="my-4" />
        <div class="text-body-small text-medium-emphasis text-center mb-2">
          <v-icon icon="mdi-lightning-bolt" size="14" color="warning" />
          ທົດລອງເຂົ້າໃຊ້ດ່ວນດ້ວຍ 1 ຄລິກ (ໂໝດພັດທະນາ):
        </div>
        <div class="d-flex flex-wrap justify-center ga-1">
          <v-btn
            size="small"
            color="warning"
            variant="tonal"
            prepend-icon="mdi-shield-crown-outline"
            :loading="demoLoading === 'admin'"
            @click="quickDemoLogin('admin@searchwant.com', 'admin123', 'admin')"
          >
            ຜູ້ດູແລລະບົບ
          </v-btn>
          <v-btn
            size="small"
            color="secondary"
            variant="tonal"
            prepend-icon="mdi-store-outline"
            :loading="demoLoading === 'owner'"
            @click="quickDemoLogin('owner@searchwant.com', 'owner123', 'owner')"
          >
            ເຈົ້າຂອງຮ້ານ
          </v-btn>
          <v-btn
            size="small"
            color="primary"
            variant="tonal"
            prepend-icon="mdi-car-outline"
            :loading="demoLoading === 'user'"
            @click="quickDemoLogin('user@searchwant.com', 'user123', 'user')"
          >
            ລູກຄ້າ / ຄົນຂັບລົດ
          </v-btn>
        </div>
      </template>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { isSafeInternalPath, useAuthStore } from '~/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const tab = ref<'login' | 'register'>('login')
const showPass = ref(false)
const submitting = ref(false)
const demoLoading = ref<string | null>(null)
const errorMsg = ref('')

const loginForm = reactive({
  email: '',
  password: '',
})

const regForm = reactive({
  full_name: '',
  email: '',
  phone: '',
  password: '',
})

function redirectAfterAuth(role: string) {
  const redir = route.query.redirect
  if (isSafeInternalPath(redir) && redir !== '/login') {
    router.push(redir)
  } else if (role === 'ADMIN' || role === 'SUPER_ADMIN') {
    router.push('/admin/approvals')
  } else {
    router.push('/')
  }
}

async function submitLogin() {
  errorMsg.value = ''
  submitting.value = true
  try {
    const user = await authStore.login(loginForm.email, loginForm.password)
    redirectAfterAuth(user.role)
  } catch (err: any) {
    errorMsg.value = err?.data?.detail || 'ເຂົ້າສູ່ລະບົບບໍ່ສຳເລັດ. ກະລຸນາກວດສອບອີເມວ ແລະ ລະຫັດຜ່ານ.'
  } finally {
    submitting.value = false
  }
}

async function submitRegister() {
  errorMsg.value = ''
  if (regForm.password.length < 6) {
    errorMsg.value = 'ລະຫັດຜ່ານຕ້ອງມີຢ່າງໜ້ອຍ 6 ຕົວອັກສອນ.'
    return
  }
  submitting.value = true
  try {
    const user = await authStore.register(regForm)
    redirectAfterAuth(user.role)
  } catch (err: any) {
    errorMsg.value = err?.data?.detail || 'ການສ້າງບັນຊີບໍ່ສຳເລັດ. ກະລຸນາກວດສອບຂໍ້ມູນ.'
  } finally {
    submitting.value = false
  }
}

async function quickDemoLogin(email: string, pass: string, tag: string) {
  errorMsg.value = ''
  demoLoading.value = tag
  try {
    const user = await authStore.login(email, pass)
    redirectAfterAuth(user.role)
  } catch (err: any) {
    errorMsg.value = err?.data?.detail || 'ເຂົ້າສູ່ລະບົບສາທິດບໍ່ສຳເລັດ.'
  } finally {
    demoLoading.value = null
  }
}
</script>
