import { defineComponent, h } from 'vue'
import { createVuetify } from 'vuetify'
import { aliases, mdi as mdiSvg } from 'vuetify/iconsets/mdi-svg'
import {
  VAlert,
  VApp,
  VAppBar,
  VAvatar,
  VBadge,
  VBtn,
  VBtnToggle,
  VCard,
  VCardActions,
  VCardText,
  VChip,
  VCol,
  VContainer,
  VDialog,
  VDivider,
  VForm,
  VIcon,
  VList,
  VListItem,
  VListItemSubtitle,
  VListItemTitle,
  VMain,
  VMenu,
  VProgressCircular,
  VProgressLinear,
  VRow,
  VSelect,
  VSheet,
  VSnackbar,
  VSpacer,
  VSwitch,
  VTab,
  VTabs,
  VTextField,
  VTextarea,
} from 'vuetify/components'
import { Ripple } from 'vuetify/directives'
import { resolveMdiSvgPath } from '~/utils/mdiIcons'

const SwMdiSvgIcon = defineComponent({
  name: 'SwMdiSvgIcon',
  inheritAttrs: false,
  props: {
    icon: {
      type: [String, Array, Object, Function],
      default: '',
    },
    tag: {
      type: String,
      default: 'i',
    },
  },
  setup(props, { attrs }) {
    return () => {
      const pathData = resolveMdiSvgPath(typeof props.icon === 'string' ? props.icon : '')
      return h(
        props.tag,
        { ...attrs, style: null },
        [
          h(
            'svg',
            {
              class: 'v-icon__svg',
              xmlns: 'http://www.w3.org/2000/svg',
              viewBox: '0 0 24 24',
              role: 'img',
              'aria-hidden': 'true',
            },
            [h('path', { d: pathData })],
          ),
        ],
      )
    }
  },
})

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    ssr: true,
    components: {
      VAlert,
      VApp,
      VAppBar,
      VAvatar,
      VBadge,
      VBtn,
      VBtnToggle,
      VCard,
      VCardActions,
      VCardText,
      VChip,
      VCol,
      VContainer,
      VDialog,
      VDivider,
      VForm,
      VIcon,
      VList,
      VListItem,
      VListItemSubtitle,
      VListItemTitle,
      VMain,
      VMenu,
      VProgressCircular,
      VProgressLinear,
      VRow,
      VSelect,
      VSheet,
      VSnackbar,
      VSpacer,
      VSwitch,
      VTab,
      VTabs,
      VTextField,
      VTextarea,
    },
    directives: {
      Ripple,
    },
    icons: {
      defaultSet: 'mdi',
      aliases,
      sets: {
        mdi: {
          component: SwMdiSvgIcon as any,
        },
        svg: mdiSvg,
      },
    },
    theme: {
      defaultTheme: 'searchWantLight',
      themes: {
        searchWantLight: {
          dark: false,
          colors: {
            background: '#F5F7FB',
            surface: '#FFFFFF',
            primary: '#155EEF',
            secondary: '#0F766E',
            accent: '#B45309',
            error: '#B91C1C',
            info: '#0369A1',
            success: '#15803D',
            warning: '#C2410C',
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
