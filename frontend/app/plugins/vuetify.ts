import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    components,
    directives,
    theme: {
      defaultTheme: 'searchWantLight',
      themes: {
        searchWantLight: {
          dark: false,
          colors: {
            background: '#F5F7FB',
            surface: '#FFFFFF',
            primary: '#1A73E8',
            secondary: '#0D9488',
            accent: '#F59E0B',
            error: '#DC2626',
            info: '#0284C7',
            success: '#16A34A',
            warning: '#EA580C',
          },
        },
        searchWantDark: {
          dark: true,
          colors: {
            background: '#0B1120',
            surface: '#151F32',
            primary: '#3B82F6',
            secondary: '#14B8A6',
            accent: '#F59E0B',
            error: '#EF4444',
            info: '#38BDF8',
            success: '#22C55E',
            warning: '#F97316',
          },
        },
      },
    },
    defaults: {
      VBtn: {
        rounded: 'lg',
        elevation: 0,
      },
      VCard: {
        rounded: 'xl',
        elevation: 0,
      },
      VChip: {
        rounded: 'pill',
      },
      VTextField: {
        variant: 'outlined',
        density: 'compact',
        rounded: 'lg',
      },
      VSelect: {
        variant: 'outlined',
        density: 'compact',
        rounded: 'lg',
      },
      VTextarea: {
        variant: 'outlined',
        density: 'compact',
        rounded: 'lg',
      },
    },
  })

  nuxtApp.vueApp.use(vuetify)
})
