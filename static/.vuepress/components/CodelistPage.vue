<template>
  <div>
    <b-row>
      <b-col md="8">
        <h2>{{ this.$frontmatter.title }}</h2>
        <p class="text-muted" v-if="lastUpdatedDate">
          {{ this.$themeLocaleConfig.lastUpdated }}: {{ lastUpdatedDate }}
        </p>
      </b-col>
      <b-col md="4" class="md-text-right">
        <b-dropdown :text="this.$themeLocaleConfig.download" right style="margin-bottom:10px">
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
    <b-pagination
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      align="fill"
      size="sm"
      class="my-0"
      v-if="totalRows > 100"
    ></b-pagination>
    <b-table
      :fields="fields"
      :items="codes"
      :tbody-tr-class="rowClass"
      :current-page="currentPage"
      :per-page="perPage"
      :busy="isBusy"
      responsive>

      <template v-slot:table-busy>
        <div class="text-center">
          <b-spinner class="align-middle" label="Loading..."></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>

      <template v-slot:cell(code)="data">
        <a :id="data.item.code" style="visibility:hidden;padding-top:73px;"></a>
        <router-link :to="'#' + data.item.code">{{ data.item.code }}</router-link>
      </template>

      <template v-slot:cell(category)="data" v-if="categoryCodelist">
        <router-link :to="'../' + categoryCodelist + '/#' + data.item.category">{{ data.item.category }}</router-link>
      </template>
    </b-table>
    <b-pagination
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      align="fill"
      size="sm"
      class="my-0"
      v-if="totalRows > 100"
      responsive
    ></b-pagination>
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
  table {
    display: table;
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
        downloadURLs: [],
        lastUpdatedDate: null,
        perPage: 500,
        currentPage: 1,
        isBusy: true
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
      this.lastUpdatedDate = data.data.metadata["last-updated-date"] ? data.data.metadata["last-updated-date"] : null
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
      this.isBusy = false
    },
    watch: {
      codes: {
        handler: 'handleScroll'
      }
    },
    computed: {
      totalRows() {
        return this.codes.length
      }
    },
    methods: {
      handleScroll() {
        var hash = this.$route.hash.split("#")[1]
        if (this.totalRows > this.perPage) {
          var codeIndex = this.codes.findIndex(code => code.code == hash)+1
          var newPage = Math.ceil(codeIndex/parseFloat(this.perPage))
          this.currentPage = newPage
        }
        if (this.$route.hash) {
          setTimeout(() => {
            var anchor = document.getElementById(hash)
            VueScrollTo.scrollTo(anchor, 500)
          }, 300)
        }
      },
      rowClass(item, type) {
        if (!item) return
        if (item.status === 'withdrawn') return 'withdrawn-code'
        if ((item['budget-alignment:status']) && (item['budget-alignment:status'] != "")) return 'table-danger'
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
        return value.replace(/\n/g, '<br>').replace(/`([^<]+) <([^>]+)>`__/g, '<a href="$2">$1</a>')
      }
    }
  }
</script>