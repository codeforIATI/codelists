export default defineEventHandler(async (event) => {
  // event.context.path to get the route path: '/api/foo/bar/baz'
  // event.context.params._ to get the route segment: 'bar/baz'
  const assetStorage = useStorage('assets:server')
  const exampleJson = await assetStorage.getItem(`api/${event.context.params._}`)
  return exampleJson
})