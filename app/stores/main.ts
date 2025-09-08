export const useStore = defineStore('mainStore', {
  state: () => ({
    codelists: [],
    codelistsObj: []
  }),
  actions: {
    async fetch() {
      const data = await $fetch('/api/index.v2.json')
      this.codelists = Object.keys(data)
      this.codelistsObj = Object.values(data)
    }
  }
})