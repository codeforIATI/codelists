<template>
  <div>
    <b-row>
      <b-col md="8"><h1>{{ title }}</h1></b-col>
      <b-col md="4" class="text-right">
        <b-dropdown text="Download" right>
          <b-dropdown-item v-for="downloadURL in downloadURLs" :href="downloadURL.url">{{ downloadURL.format }}</b-dropdown-item>
        </b-dropdown>
      </b-col>
    </b-row>
    <b-alert show>
      <p v-if="description"><i>{{ description }}</i></p>
      <p v-if="categoryCodelist">This codelist is grouped into categories, using the
      <a :href="`../${categoryCodelist}`"><code>{{ categoryCodelist }}</code></a>
    codelist.</p>
      <p v-if="url">Original source: <a :href="url">{{ url }}</a></p>
    </b-alert>
    <b-table
      :fields="fields"
      :items="codes"
      :tbody-tr-class="rowClass">
    </b-table>
  </div>
</template>
<style>
  .theme-default-content:not(.custom) {
    max-width: inherit;
  }
  .withdrawn-code {
    font-style: italic;
    color: #bbbbbb;
  }
</style>
<script>
  import axios from 'axios'
  import 'bootstrap/dist/css/bootstrap.css'
  import 'bootstrap-vue/dist/bootstrap-vue.css'
  export default {
    name: 'CodelistPage',
    props: ['codelist', 'lang'],
    data () {
      return {
        title: "",
        description: null,
        categoryCodelist: null,
        url: null,
        codes: [],
        fields: [],
        downloadURLs: []
      }
    },
    async beforeMount() {
      var data = await axios.get(`/clv3/json/${this.lang}/${this.codelist}.json`)
      this.fields = Object.keys(data.data.data[0]).map(field => {
        return { key: field, sortable: true }
      })
      this.codes = data.data.data
      this.title = data.data.attributes.name
      this.description = (data.data.metadata.description != "") ? data.data.metadata.description : null
      this.categoryCodelist = data.data.attributes["category-codelist"] ? data.data.attributes["category-codelist"] : null
      this.url = data.data.metadata.url ? data.data.metadata.url : null
      this.downloadURLs = [
        {
          "url":`/clv3/xml/${this.codelist}.xml`,
          "format": "XML"
        },
        {
          "url":`/clv3/csv/${this.lang}/${this.codelist}.csv`,
          "format": "CSV"
        },
        {
          "url":`/clv3/json/${this.lang}/${this.codelist}.json`,
          "format": "JSON"
        }
      ]
    },
    methods: {
      rowClass(item, type) {
        if (!item) return
        if (item.status === 'withdrawn') return 'withdrawn-code'
      }
    }
  }
</script>