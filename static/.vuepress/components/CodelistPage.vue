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
        <b-dropdown :text="this.$themeLocaleConfig.download" right class="download-dropdown">
          <b-dropdown-item v-for="downloadURL in downloadURLs" :href="downloadURL.url">{{ downloadURL.format }}</b-dropdown-item>
        </b-dropdown>
      </b-col>
    </b-row>
    <b-alert :show="(description != null) || (categoryCodelist != null) || (url != null)">
      <p v-if="description"><i v-html="description"></i></p>
      <p v-if="categoryCodelist">{{ this.$themeLocaleConfig.categorisedCodelist }}
      <router-link :to="`../${categoryCodelist}`"><code>{{ categoryCodelist }}</code></router-link>.</p>
      <p v-if="url">{{ this.$themeLocaleConfig.source }}: <a :href="url">{{ url }}</a></p>
    </b-alert>
    <b-row v-if="codes">
      <b-col class="my-1" lg="6">
        <b-form-group
          label="Filter"
          :label-cols-sm="false"
          label-cols-md="3"
          label-cols-lg="2"
          label-align-lg="right"
          label-size="sm"
          label-for="filterInput"
          class="mb-0"
        >
          <b-input-group size="sm">
            <b-form-input
              v-model="filter"
              type="search"
              id="filterInput"
              placeholder="Type to Search"
            ></b-form-input>
            <b-input-group-append>
              <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
            </b-input-group-append>
          </b-input-group>
        </b-form-group>
      </b-col>
      <b-col class="my-1"
        lg="6"
        v-if="totalRows > perPage">
        <b-form-group
          label="Page"
          :label-cols-sm="false"
          label-cols-md="3"
          label-cols-lg="2"
          label-align-lg="right"
          label-size="sm"
          class="mb-0"
        >
          <b-pagination
            v-model="currentPage"
            :total-rows="totalRows"
            :per-page="perPage"
            align="fill"
            size="sm"
            class="my-0"
          ></b-pagination>
        </b-form-group>
      </b-col>
    </b-row>
    <b-table
      :fields="fields"
      :items="codes"
      :tbody-tr-class="rowClass"
      :current-page="currentPage"
      :per-page="perPage"
      :busy="isBusy"
      :filter="filter"
      @filtered="onFiltered"
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
    <b-form-group
      label="Page"
      label-cols-sm="1"
      label-align-lg="right"
      label-size="sm"
      class="mb-0"
      v-if="totalRows > perPage">
      <b-pagination
        v-model="currentPage"
        :total-rows="totalRows"
        :per-page="perPage"
        align="fill"
        size="sm"
        class="my-0"
      ></b-pagination>
    </b-form-group>
  </div>
</template>
<style>
  body {
    overflow-wrap: break-word;
  }
  .download-dropdown {
    margin-bottom:10px;
    width:100%;
  }
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
        totalRows: 0,
        filter: null,
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
      this.totalRows = this.codes.length
      this.isBusy = false
    },
    watch: {
      codes: {
        handler: 'handleScroll'
      }
    },
    methods: {
      onFiltered(filteredItems) {
        // Trigger pagination to update the number of buttons/pages due to filtering
        this.totalRows = filteredItems.length
        this.currentPage = 1
      },
      handleScroll() {
        var hash = this.$route.hash.split("#")[1]
        if (this.$route.hash) {
          if (this.totalRows > this.perPage) {
            var codeIndex = this.codes.findIndex(code => code.code == hash)+1
            var newPage = Math.ceil(codeIndex/parseFloat(this.perPage))
            this.currentPage = newPage
          }
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