<template>
  <div>
    <b-row>
      <b-col md="8"><h2>{{ this.$frontmatter.title }}</h2></b-col>
      <b-col md="4" class="text-right">
        <b-dropdown :text="this.$themeLocaleConfig.download" right>
          <b-dropdown-item v-for="downloadURL in downloadURLs" :href="downloadURL.url">{{ downloadURL.format }}</b-dropdown-item>
        </b-dropdown>
      </b-col>
    </b-row>
    <b-alert show>
      <p v-if="description"><i v-html="description"></i></p>
      <p v-if="categoryCodelist">{{ this.$themeLocaleConfig.categorisedCodelist }}
      <router-link :to="`../${categoryCodelist}`"><code>{{ categoryCodelist }}</code></router-link>.</p>
      <p v-if="url">{{ this.$themeLocaleConfig.source }}: <a :href="url">{{ url }}</a></p>
    </b-alert>
    <b-table
      :fields="fields"
      :items="codes"
      :tbody-tr-class="rowClass">

      <template v-slot:cell(code)="data">
        <a :id="data.item.code" style="visibility:hidden;padding-top:73px;"></a>
        <router-link :to="'#' + data.item.code">{{ data.item.code }}</router-link>
      </template>

      <template v-slot:cell(category)="data" v-if="categoryCodelist">
        <router-link :to="'../' + categoryCodelist + '/#' + data.item.category">{{ data.item.category }}</router-link>
      </template>
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
  import VueScrollTo from 'vue-scrollto'
  import 'bootstrap/dist/css/bootstrap.css'
  import 'bootstrap-vue/dist/bootstrap-vue.css'
  export default {
    name: 'CodelistPage',
    props: ['codelist', 'lang'],
    data () {
      return {
        description: null,
        categoryCodelist: null,
        url: null,
        codes: [],
        fields: [],
        downloadURLs: []
      }
    },
    async beforeMount() {
      var data = await axios.get(`/api/json/${this.lang}/${this.codelist}.json`)
      this.fields = Object.keys(data.data.data[0]).map(field => {
        var f = {
          key: field,
          sortable: true,
          label: this.$themeLocaleConfig.headers[field] ? this.$themeLocaleConfig.headers[field] : null
        }
        if (field == 'status') {
          f.formatter = 'statusFormatter'
        }
        return f
      })
      this.codes = data.data.data
      this.description = (data.data.metadata.description != "") ? this.rstToHtml(data.data.metadata.description) : null
      this.categoryCodelist = data.data.attributes["category-codelist"] ? data.data.attributes["category-codelist"] : null
      this.url = data.data.metadata.url ? data.data.metadata.url : null
      this.downloadURLs = [
        {
          "url":`/api/xml/${this.codelist}.xml`,
          "format": "XML"
        },
        {
          "url":`/api/csv/${this.lang}/${this.codelist}.csv`,
          "format": "CSV"
        },
        {
          "url":`/api/xlsx/${this.lang}/${this.codelist}.xlsx`,
          "format": "XLSX"
        },
        {
          "url":`/api/json/${this.lang}/${this.codelist}.json`,
          "format": "JSON"
        }
      ]
    },
    mounted() {
      if (this.$route.hash) {
        setTimeout(() => {
          var anchor = document.getElementById(this.$route.hash.split("#")[1])
          VueScrollTo.scrollTo(anchor, 500)
        }, 500)
      }
    },
    methods: {
      rowClass(item, type) {
        if (!item) return
        if (item.status === 'withdrawn') return 'withdrawn-code'
      },
      statusFormatter(value) {
        return this.columnFormatter('status', value)
      },
      columnFormatter(field, value) {
        if (!this.$themeLocaleConfig.columnValues) { return value }
        return this.$themeLocaleConfig.columnValues[field][value] ? this.$themeLocaleConfig.columnValues[field][value] : value
      },
      rstToHtml(value) {
        // it's tricky to do this properly in javascript,
        // so a regex will have to suffice
        return value.replace(/`([^<]+) <([^>]+)>`__/g, '<a href="$2">$1</a>')
      }
    }
  }
</script>