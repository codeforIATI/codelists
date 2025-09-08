<template>
  <div>
    <BRow>
      <BCol md="8">
        <h2>{{ name }}</h2>
        <p>Codelist: <code>{{ codelist }}</code></p>
        <p class="text-muted" v-if="lastUpdatedDate">
          {{ $t('lastUpdated') }}: {{ lastUpdatedDate }}
        </p>
      </BCol>
      <BCol md="4" class="text-md-end">
        <b-dropdown :text="$t('download')" right class="download-dropdown">
          <b-dropdown-item v-for="downloadURL in downloadURLs" :href="downloadURL.url">{{ downloadURL.format
          }}</b-dropdown-item>
        </b-dropdown>
      </BCol>
    </BRow>
    <b-alert :show="(description != null) || (categoryCodelist != null) || (url != null)">
      <p v-if="description"><i v-html="description"></i></p>
      <p v-if="categoryCodelist">{{ $t('categorisedCodelist') }}
        <nuxt-link :to="`../${categoryCodelist}`"><code>{{ categoryCodelist }}</code></nuxt-link>.
      </p>
      <p v-if="url">{{ $t('source') }}: <a :href="url">{{ url }}</a></p>
    </b-alert>
    <BRow v-if="codes">
      <BCol class="my-1" lg="6">
        <b-form-group :label="$t('search')" :label-cols-sm="false" label-cols-md="3" label-cols-lg="2"
          label-align-lg="right" label-size="sm" label-for="filterInput" class="mb-0">
          <b-input-group size="sm">
            <b-form-input v-model="filter" type="search" id="filterInput"
              :placeholder="$t('typeToSearch')"></b-form-input>
            <template #append>
              <b-button :disabled="!filter" @click="filter = ''">{{ $t('clear') }}</b-button>
            </template>
          </b-input-group>
        </b-form-group>
      </BCol>
      <BCol class="my-1" lg="6" v-if="totalRows > perPage">
        <b-form-group label="Page" :label-cols-sm="false" label-cols-md="3" label-cols-lg="2" label-align-lg="right"
          label-size="sm" class="mb-0">
          <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="perPage" align="fill" size="sm"
            class="my-0"></b-pagination>
        </b-form-group>
      </BCol>
    </BRow>
    <b-table :fields="fields" :items="codes" :tbody-tr-class="rowClass" :current-page="currentPage" :per-page="perPage"
      :filter="filter" @filtered="onFiltered" responsive>

      <template v-slot:table-busy>
        <div class="text-center">
          <b-spinner class="align-middle" label="Loading..."></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>

      <template v-slot:cell(url)="data">
        <template v-if="isValidUrl(data.item.url)">
          <a :href="data.item.url">{{ data.item.url }}</a>
        </template>
        <template v-else>
          {{ data.item.url }}
        </template>
      </template>

      <template v-slot:cell(code)="data">
        <a :id="data.item.code" style="visibility:hidden;padding-top:73px;"></a>
        <nuxt-link :to="'#' + data.item.code">{{ data.item.code }}</nuxt-link>
      </template>

      <template v-slot:cell(category)="data" v-if="categoryCodelist">
        <template v-if="data.item.category != null">
          <span class="category-item" v-for="category in data.item.category.split(';').sort()" :key="category">
            <nuxt-link :to="'../' + categoryCodelist + '/#' + category">{{ category }}</nuxt-link>
          </span>
        </template>
      </template>

      <template v-slot:cell(status)="data">
        {{ rt(tm('columnValues')['status'][data.item.status]) }}
      </template>
    </b-table>
    <b-form-group label="Page" label-cols-sm="1" label-align-lg="right" label-size="sm" class="mb-0"
      v-if="totalRows > perPage">
      <b-pagination v-model="currentPage" :total-rows="totalRows" :per-page="perPage" align="fill" size="sm"
        class="my-0"></b-pagination>
    </b-form-group>
  </div>
</template>
<style>
body {
  overflow-wrap: break-word;
}

.download-dropdown {
  margin-bottom: 10px;
  width: 100%;
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

.category-item:after {
  content: "; ";
  color: #888;
}

.category-item:last-child:after {
  content: ""
}

.url,
.description {
  word-break: break-word;
}
</style>
<script setup>
const { t, tm, rt } = useI18n()

const props = defineProps({
  'codelist': {
    type: String,
    required: true
  },
  'lang': {
    type: String,
    required: true
  }
})

const perPage = ref(500)
const currentPage = ref(1)
const filter = ref(null)
const isBusy = ref(true)


const isValidUrl = (url) => {
  try {
    new URL(url)
    return true
  } catch (err) {
    return false
  }
}
const onFiltered = (filteredItems) => {
  // Trigger pagination to update the number of buttons/pages due to filtering
  totalRows.value = filteredItems.length
  currentPage.value = 1
}
const rowClass = (item, type) => {
  if (!item) return
  if (item.status === 'withdrawn') return 'withdrawn-code'
  if ((item['budget-alignment:status']) && (item['budget-alignment:status'] != "")) return 'table-danger'
}
const rstToHtml = (value) => {
  // it's tricky to do this properly in javascript,
  // so a regex will have to suffice
  return value.replace(/\n/g, '<br>').replace(/`([^<]+) <([^>]+)>`__/g, '<a href="$2">$1</a>')
}

const themeHeaders = computed(() => {
  return Object.entries(tm('headers')).reduce((summary, item) => {
    summary[item[0]] = rt(item[1])
    return summary
  }, {})
})

const { data: apiData } = await useFetch(`/api/json/${props.lang}/${props.codelist}.json`)

const fields = computed(() => {
  return Object.keys(apiData.value?.data[0]).map(field => {
    var f = {
      key: field,
      sortable: true,
      tdClass: ['description', 'url'].includes(field) ? field : null,
      label: themeHeaders.value[field] ? themeHeaders.value[field] : null
    }
    return f
  })
})

const codes = computed(() => {
  return apiData.value.data
})

const name = computed(() => {
  return apiData.value.metadata.name ? apiData.value.metadata.name : props.codelist
})

const description = computed(() => {
  return !["", null].includes(apiData.value?.metadata.description) ? rstToHtml(apiData.value.metadata.description.trim()) : null
})

const lastUpdatedDate = computed(() => {
  return apiData.value.metadata["last-updated-date"] ? apiData.value.metadata["last-updated-date"] : null
})

const categoryCodelist = computed(() => {
  return apiData.value.metadata["category-codelist"] ? apiData.value.metadata["category-codelist"] : null
})

const url = computed(() => {
  return apiData.value.metadata.url ? apiData.value.metadata.url : null
})

const downloadURLs = computed(() => {
  return [
    {
      "url": `/api/xml/${props.codelist}.xml`,
      "format": "XML"
    },
    {
      "url": `/api/csv/${props.lang}/${props.codelist}.csv`,
      "format": "CSV"
    },
    {
      "url": `/api/xlsx/${props.lang}/${props.codelist}.xlsx`,
      "format": "XLSX"
    },
    {
      "url": `/api/json/${props.lang}/${props.codelist}.json`,
      "format": "JSON"
    }
  ]
})

const totalRows = computed(() => {
  return codes.value.length
})

</script>