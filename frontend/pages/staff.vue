<template>
  <div>
    <!-- <IndividualStaffView v-if="projectId" /> -->
    <!-- <v-container v-else class="pa-0" fluid> -->
    <v-container class="pa-0" fluid>
      <v-row>
        <v-col>
          <NewStaffModal />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card class="px-6 py-3">
            <h1 class="title">Manage Staff</h1>
            <v-row>
              <v-col>
                <AllStaffQuery />
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import NewStaffModal from './../components/staff/modals/NewStaffModal'
import AllStaffQuery from './../components/staff/apollo/AllStaffQuery'

export default {
  components: { NewStaffModal, AllStaffQuery },
  data () {
    return {
      staffId: this.$route.query.id
    }
  },
  watch: {
    '$route.query.id': {
      handler () {
        this.projectId = this.$route.query.id
      }
    }
  }
}
</script>
