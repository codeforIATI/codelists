import { defineContentConfig, defineCollection, z } from '@nuxt/content'

const commonSchema = z.object({

})

export default defineContentConfig({
  collections: {
    content_en: defineCollection({
      type: 'page',
      source: {
        include: 'en/**',
        prefix: '',
      },
      schema: commonSchema
    }),
    content_fr: defineCollection({
      type: 'page',
      source: {
        include: 'fr/**',
        prefix: '',
      },
      schema: commonSchema
    })
  },
  build: {
    pathMeta: {
      slugifyOptions: {
        lower: false
      }
    },
  },
  anchorLinks: false
})
