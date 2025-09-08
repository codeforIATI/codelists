<template>
  <BRow class="d-md-none mt-5">
    <BCol>
      <BButton variant="link" underline-opacity="0" @click="showNavigation">&laquo; Navigation</BButton>
    </BCol>
  </BRow>
  <div class="scrollable-column">
    <BOffcanvas v-model="navigationVisible" placement="start" responsive="md">
      <BNav vertical pills>
        <template v-if="navigation">
          <BNavItem v-for="item in navigation" :key="item.path" :to="localePath(item.path)">{{ item.title }}</BNavItem>
        </template>
        <hr />
        <template v-if="codelistsObj">
          <BNavItem v-for="item in codelistsObj" :key="item.code" :to="localePath('/' + item.code)">{{ item[locale].name
            ||
            item.en.name
          }}
          </BNavItem>
        </template>
      </BNav>
    </BOffcanvas>
  </div>
</template>
<style>
.scrollable-column {
  max-height: calc(-6rem + 100vh);
  overflow-y: auto;
  position: sticky;
  top: 5rem;
}
</style>
<script setup>
const { locale } = useI18n()
const localePath = useLocalePath()
const main = useStore()
const { data: navigation } = await useAsyncData('navigation' + locale.value, () => {
  return queryCollectionNavigation('content_' + locale.value)
}, {
  watch: [locale], // Refetch when locale changes
})
const codelists = main.codelists
const codelistsObj = main.codelistsObj
const navigationVisible = ref(false)
const showNavigation = () => {
  navigationVisible.value = true
}
</script>
