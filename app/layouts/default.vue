<template>
  <div class="page-body">
    <BNavbar v-b-color-mode="'light'" toggleable="lg" variant="light" fixed="top">
      <BNavbarBrand :to="localePath('/')"><img src="https://codeforiati.org/assets/img/logo.png"
          alt="Replicated Codelists" class="logo"> {{ $t('title') }}</BNavbarBrand>
      <BNavbarToggle target="nav-collapse" />
      <BCollapse id="nav-collapse" is-nav>
        <!-- Right aligned nav items -->
        <BNavbarNav class="ms-auto mb-2 mb-lg-0">

          <BNavItem variant="primary" @click.prevent="showSearch = true">{{ $t('search') }}</BNavItem>
          <BNavItem href="/api/index.json">API</BNavItem>
          <BNavItemDropdown :text="$t('selectText')" right>
            <BDropdownItem v-for="locale in availableLocales" :key="locale.code" :to="switchLocalePath(locale.code)">{{
              locale.name }}</BDropdownItem>
          </BNavItemDropdown>
        </BNavbarNav>
      </BCollapse>
    </BNavbar>
    <BContainer fluid class="my-md-4">
      <BRow>
        <BCol md="3" lg="2" class="mt-3">
          <Sidebar />
        </BCol>
        <BCol md="9" lg="10" class="mt-3 pt-md-5 page-body">
          <slot />
        </BCol>
      </BRow>
    </BContainer>
    <BModal v-model="showSearch" :title="$t('search')" no-footer>
      <BFormInput v-model="query" :placeholder="$t('typeToSearch')" />
      <ul>
        <li v-for="link of result" :key="link.id" class="mt-2">
          <NuxtLink :to="link.id">{{ link.title }}</NuxtLink>
          <p class="text-gray-500 text-xs">{{ link.content }}</p>
        </li>
      </ul>
    </BModal>
  </div>
</template>
<style>
.navbar .logo {
  height: 2.2rem;
  min-width: 2.2rem;
  margin-right: .8rem;
  vertical-align: top;
}

.page-body {
  min-height: 100vh;
}
</style>
<script setup>
import MiniSearch from 'minisearch'
const { locale, locales } = useI18n()
const localePath = useLocalePath()
const switchLocalePath = useSwitchLocalePath()
const main = useStore()

const availableLocales = computed(() => {
  return locales.value
})
await callOnce(main.fetch)

/* Search */
const showSearch = ref(false)
const query = ref('')
const { data } = await useAsyncData('search', () => queryCollectionSearchSections(`content_${locale.value}`), {
  watch: [locale], // Refetch when locale changes
})

const codelistsObj = main.codelistsObj

const combinedData = computed(() => {
  return data.value.concat(main.codelistsObj.map(item => {
    return {
      title: item[locale.value].name,
      content: item[locale.value].description,
      id: localePath('/' + item.code)
    }
  }))
})

const miniSearch = new MiniSearch({
  fields: ['title', 'content'],
  storeFields: ['title', 'content'],
  searchOptions: {
    prefix: true,
    fuzzy: 0.2,
  },
})

const result = computed(() => miniSearch.search(toValue(query)))

watch(
  [() => locale.value],
  () => {
    miniSearch.removeAll()
    query.value = ''
    miniSearch.addAll(toValue(combinedData.value))
  },
  { immediate: true }
)

useHead({
  bodyAttrs: {
    class: 'page-body'
  }
})
</script>
