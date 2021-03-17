<template>
    <v-btn
      :loading="isLoading"
      color="amber darken-1"
      dark
      :class="className"
      @click="downloadReport"
    >Generate Report</v-btn>
</template>
<script>
import { utils, writeFile } from 'xlsx'

export default {
  props: {
    className: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      isLoading: false,
      sheets: [{ c: 2 }]
    }
  },
  methods: {
    downloadReport () {
      console.log(utils)
      const wb = utils.book_new()
      const ws = utils.json_to_sheet(this.sheets)
      utils.book_append_sheet(wb, ws, 'Sheet 1')
      writeFile(wb, 'report.xlsx')
    }
  }
}
</script>
