<template>
  <v-btn
    :loading="isLoading"
    color="amber darken-1"
    dark
    :class="className"
    @click="downloadReport"
  >
    Generate Report
  </v-btn>
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
      accessToken: '',
      isLoading: false,
      generationLink: 'https://api.apphasia.cf/reportgeneration'
    }
  },
  mounted () {
    const accessToken = localStorage.getItem(`auth.CognitoIdentityServiceProvider.${this.$auth.strategies.cognito.options.clientId}.${this.$auth.user.sub}.accessToken`)
    this.accessToken = accessToken
  },
  methods: {
    async downloadReport () {
      this.isLoading = true
      const postHeader = {
        'Content-Type': 'application/json',
        Authorization: this.accessToken
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
            this.generateExternalPeopleReport(response.data, 'Volunteer')
            break
          default: // pwas
            this.generateExternalPeopleReport(response.data, 'PWA')
            break
        }
      }).catch((error) => {
        console.error(error)
      })
      this.isLoading = false
    },
    generateProjectsReport (data) {
      const workbook = utils.book_new()
      const dataArray = [['Project Name', '# of events per year']]
      for (const projectName in data) {
        dataArray.push([projectName, data[projectName]])
      }
      const worksheet = utils.aoa_to_sheet(dataArray)
      utils.book_append_sheet(workbook, worksheet, 'Project Analytics')
      writeFile(workbook, `Projects_report_${new Date().toString().substring(4, 15)}.xlsx`)
    },
    generateExternalPeopleReport (data, type) {
      const _ = require('lodash')
      const workbook = utils.book_new()

      // Attendance Tracking
      const attendanceArray = {}
      for (const category in data['Attendance Tracking']) {
        Object.keys(data['Attendance Tracking'][category]).map((name) => {
          if (name in attendanceArray) {
            const row = _.cloneDeep(attendanceArray[name])
            row[category] = data['Attendance Tracking'][category][name]
            attendanceArray[name] = row
          } else {
            const row = { Name: name }
            row[category] = data['Attendance Tracking'][category][name]
            attendanceArray[name] = row
          }
        })
      }
      const attendanceWorksheet = utils.json_to_sheet(Object.values(attendanceArray).sort((a, b) => b['# of total events attended this year'] - a['# of total events attended this year']))
      utils.book_append_sheet(workbook, attendanceWorksheet, 'Attendance Analytics')

      // Create Age Analytics
      const ageArray = [Object.keys(data['Capture Age'])]
      const rowArray = []
      for (const value in data['Capture Age']) {
        rowArray.push(data['Capture Age'][value])
      }
      ageArray.push(rowArray)
      const ageWorksheet = utils.aoa_to_sheet(ageArray)
      utils.book_append_sheet(workbook, ageWorksheet, 'Age Analytics')

      // Capture attrition rate
      let attritionArray = [Object.keys(data['Capture attrition rate'])]
      const attritionRowArray = []
      for (const value in data['Capture attrition rate']) {
        attritionRowArray.push(data['Capture attrition rate'][value])
      }
      attritionArray = [...attritionArray, ..._.zip(...attritionRowArray)]
      const attritionWorksheet = utils.aoa_to_sheet(attritionArray)
      utils.book_append_sheet(workbook, attritionWorksheet, 'Attrition Analytics')

      // Language proficiency
      let languageArray = [Object.keys(data['Language proficiency'])]
      const languageRowArray = []
      for (const value in data['Language proficiency']) {
        languageRowArray.push(data['Language proficiency'][value])
      }
      languageArray = [...languageArray, ..._.zip(...languageRowArray)]
      const languageWorksheet = utils.aoa_to_sheet(languageArray)
      utils.book_append_sheet(workbook, languageWorksheet, 'Language Analytics')

      // PWA/Volunteer Profile
      let pwaArray = [Object.keys(data[`${type} profile`])]
      const pwaRowArray = []
      for (const value in data[`${type} profile`]) {
        pwaRowArray.push(data[`${type} profile`][value])
      }
      pwaArray = [...pwaArray, ..._.zip(...pwaRowArray)]
      const pwaWorksheet = utils.aoa_to_sheet(pwaArray)
      utils.book_append_sheet(workbook, pwaWorksheet, `${type} Profile`)

      writeFile(workbook, `${type}_report_${new Date().toString().substring(4, 15)}.xlsx`)
    }
  }
}
</script>
