<template>
  <div>
    <IndividualStaffView v-if="staffId" />
    <v-container v-else class="pa-0" fluid>
      <v-row>
        <v-col>
          <NewStaffModal />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <!-- <v-card class="px-6 py-3">
            <h1 class="title">Manage Staff</h1>
            <v-row>
              <v-col>
                <AllStaffQuery />
              </v-col>
            </v-row>
          </v-card> -->
          <AllStaffQuery />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import NewStaffModal from './../components/staff/modals/NewStaffModal'
import AllStaffQuery from './../components/staff/apollo/AllStaffQuery'
import IndividualStaffView from './../components/staff/IndividualStaffView'

export default {
  components: { NewStaffModal, AllStaffQuery, IndividualStaffView },
  data () {
    return {
      staffId: this.$route.query.id
    }
  },
  watch: {
    '$route.query.id': {
      handler () {
        this.staffId = this.$route.query.id
      }
    }
  }
}
</script>
