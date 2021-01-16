<template>
  <ApolloQuery
    :query="require('./../../../graphql/staff/GetAllStaff.gql')"
  >
    <template v-slot="{ result: { error, data }, isLoading }">
      <!-- Loading -->
      <div v-if="isLoading" class="d-flex justify-center">
        <v-progress-circular
          :size="50"
          color="primary"
          indeterminate
        />
      </div>

      <!-- Error -->
      <div v-else-if="error">An error occurred</div>

      <!-- Result -->
      <div v-else-if="data">
        <v-data-table
          :headers="getHeaders"
          :items="filteredDataByType"
          item-key="id"
          class="elevation-1"
          :search="search"
        >
          <template v-slot:top>
            <v-container class="py-0" fluid>
              <v-row>
                <v-col>
                  <h1 class="title pt-3 px-3">Manage Staff</h1>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-tabs>
                    <v-tab @click="staffTypeFilter = 'coreteam'">Core Team</v-tab>
                    <v-tab @click="staffTypeFilter = 'intern'">Interns</v-tab>
                    <v-tab @click="staffTypeFilter = 'corevolunteer'">Core Volunteers</v-tab>
                  </v-tabs>
                </v-col>
              </v-row>
              <v-row>
                <v-text-field
                  v-model="search"
                  label="Search"
                  append-icon="mdi-magnify"
                  solo
                  dense
                  class="mx-3"
                ></v-text-field>
              </v-row>
            </v-container>
          </template>
        </v-data-table>
      </div>

      <!-- No result -->
      <div v-else>No result :(</div>
    </template>
  </ApolloQuery>
</template>
<script>
export default {
  data () {
    return {
      search: '',
      staffTypeFilter: 'coreteam',
      testData: [
        {
          id: 1,
          name: 'Person 1',
          date_joined: '02/03/2010',
          profession: 'Therapist',
          speech_therapist: true,
          projects: 'Chit Chat, Befriender, Craft Night',
          type: 'coreteam'
        },
        {
          id: 2,
          name: 'Person 2',
          date_joined: '02/03/2010',
          profession: 'Student',
          speech_therapist: false,
          projects: 'Chit Chat, Befriender, Craft Night',
          type: 'intern'
        },
        {
          id: 3,
          name: 'Person 3',
          date_joined: '02/03/2010',
          profession: 'Therapist',
          speech_therapist: true,
          projects: 'Chit Chat, Befriender, Craft Night',
          type: 'corevolunteer'
        },
        {
          id: 4,
          name: 'Person 4',
          date_joined: '02/03/2010',
          profession: 'Helper',
          speech_therapist: true,
          projects: 'Chit Chat, Befriender, Craft Night',
          type: 'coreteam'
        }
      ]
    }
  },
  computed: {
    getHeaders () {
      return [
        { text: 'Name', value: 'name' },
        { text: 'Date Joined', value: 'date_joined' },
        { text: 'Profession', value: 'profession' },
        { text: 'Speech Therapist', value: 'speech_therapist' },
        { text: 'Projects Involved', value: 'projects' }
      ]
    },
    filteredDataByType () {
      return this.testData.filter(item => item.type === this.staffTypeFilter)
    }
  },
  methods: {
    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleLowerCase().includes(search.toLocaleLowerCase()) !== -1
    }
  }
}
</script>
<style scoped>

</style>
