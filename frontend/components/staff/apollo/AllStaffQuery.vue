<template>
  <ApolloQuery
    :query="require('./../../../graphql/staff/GetAllStaff.graphql')"
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
          :items="filteredDataByRole(data.staffs)"
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
                    <v-tab @click="staffRoleFilter = 'core_team'">Core Team</v-tab>
                    <v-tab @click="staffRoleFilter = 'intern'">Interns</v-tab>
                    <v-tab @click="staffRoleFilter = 'core_volunteer'">Core Volunteers</v-tab>
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
                />
              </v-row>
            </v-container>
          </template>
          <template v-slot:[`item.is_speech_therapist`]="{ item }">
            <v-chip v-if="item.is_speech_therapist" color="success">Yes</v-chip>
            <v-chip v-else color="error">No</v-chip>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <EditStaffModal :staff="item" :text="false" />
            <v-btn :to="`/staff?id=${item.id}`" icon>
              <v-icon large>
                mdi-chevron-right
              </v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </div>

      <!-- No result -->
      <div v-else>No result :(</div>
    </template>
  </ApolloQuery>
</template>
<script>
import EditStaffModal from './../modals/EditStaffModal'

export default {
  components: { EditStaffModal },
  data () {
    return {
      search: '',
      staffRoleFilter: 'core_team'
    }
  },
  computed: {
    getHeaders () {
      return [
        { text: 'Name', value: 'name', align: 'start' },
        { text: 'Date Joined', value: 'date_joined' },
        { text: 'Profession', value: 'profession' },
        { text: 'Speech Therapist', value: 'is_speech_therapist' },
        { text: 'Projects Involved', value: '' },
        { text: 'Actions', value: 'actions', sortable: false, align: 'end' }
      ]
    }
  },
  methods: {
    filteredDataByRole (data) {
      return data.filter(item => item.role === this.staffRoleFilter && item.is_active)
    }
  }
}
</script>
