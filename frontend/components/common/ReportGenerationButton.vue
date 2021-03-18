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
    },
    resourceType: {
      type: String,
      default: 'pwas'
    }
  },
  data () {
    return {
      isLoading: false,
      generationLink: 'https://cj00d9qd80.execute-api.ap-southeast-1.amazonaws.com/dev',
      sheets: [{ c: 2 }]
    }
  },
  methods: {
    async downloadReport () {
      const postHeader = {
        'Content-Type': 'application/json'
      }
      const postBody = {
        resources: this.resourceType
      }
      await this.$axios.post(this.generationLink, JSON.stringify(postBody), { postHeader }).then((response) => {
        switch (this.resourceType) {
          case 'projects':
            this.generateProjectsReport(response.data)
            break
          case 'volunteers':
            break
          default: // pwas
            break
        }
      }).catch((error) => {
        console.error(error)
      })
    },
    generateProjectsReport (data) {
      const workbook = utils.book_new()
      const dataArray = [['Project Analytics', ''], ['Project Name', '# of events per year']]
      for (const projectName in data) {
        dataArray.push([projectName, data[projectName]])
      }
      const worksheet = utils.aoa_to_sheet(dataArray)
      utils.book_append_sheet(workbook, worksheet, 'Sheet 1')
      writeFile(workbook, `projects_report_${new Date().toString().substring(4, 15)}.xlsx`)
    },
    generateExternalPeopleReport (data) {

    }
  }
}
</script>
