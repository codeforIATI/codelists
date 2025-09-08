// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    head: {
      title: 'Code for IATI Codelists',
      htmlAttrs: {
        lang: 'en',
      },
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      ]
    }
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@nuxt/content',
    '@bootstrap-vue-next/nuxt',
    '@nuxtjs/i18n',
    '@pinia/nuxt'
  ],
  css: ['bootstrap/dist/css/bootstrap.min.css'],
  i18n: {
    locales: [
      { code: 'en', language: 'en-GB', name: 'English', file: 'en.json' },
      { code: 'fr', language: 'fr-FR', name: 'Français', file: 'fr.json' }
    ],
    defaultLocale: 'en',
    strategy: 'prefix_except_default',
    defaultLocale: 'en'
  },
  components: {
    global: true,
    dirs: ['~/components']
  },
  content: {
    build: {
      pathMeta: {
        slugifyOptions: {
          lower: false
        }
      }
    }
  }
})