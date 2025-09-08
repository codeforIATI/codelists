<template>
    <ContentRenderer v-if="page" :value="page" />
    <div v-else-if="codelist">
        <CodelistPage :codelist="codelistPageName" :lang="locale" :title="codelistPageName" />
    </div>
    <div v-else>
        <h1>Page not found</h1>
    </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
import { withLeadingSlash } from 'ufo'
import type { Collections } from '@nuxt/content'

const route = useRoute()
const { locale } = useI18n()
const slug = computed(() => withLeadingSlash(String(route.params.slug)))


const main = useStore()
const codelistPageName = computed(() => {
    if (route.params.slug.length > 0) {
        return route.params.slug[0]
    }
})
const codelist = computed(() => { return main.codelists.includes(codelistPageName.value) })

const { data: page } = await useAsyncData(() => `page-${slug.value}-${locale.value}`, async () => {
    // Build collection name based on current locale
    const collection = ('content_' + locale.value) as keyof Collections
    const content = await queryCollection(collection).path(slug.value).first()

    // Optional: fallback to default locale if content is missing
    if (!content && locale.value !== 'en') {
        return await queryCollection('content_en').path(slug.value).first()
    }

    return content
}, {
    watch: [locale], // Refetch when locale changes
})

const pageTitle = computed(() => {
    if (page.value) {
        return `${page.value?.title} | ${t('siteTitle')}`
    } else if (codelist) {
        return `${codelistPageName.value} | ${t('siteTitle')}`
    } else {
        return t('siteTitle')
    }
})

useHead({
    title: pageTitle.value
})
</script>