<template>
  <div>
    <IndividualStaffView v-if="staffId" :resourceType="resourceType"/>
    <v-container v-else class="pa-0" fluid>
      <v-row>
        <v-col>
          <AddResourceModal :resourceType="resourceType"/>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <ListingQuery :resourceType="resourceType"></ListingQuery>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
import AddResourceModal from './../components/modals/AddResourceModal'
import IndividualStaffView from './../components/staff/IndividualStaffView'
import ListingQuery from './../components/common/ListingQuery'

export default {
  components: { ListingQuery, IndividualStaffView, AddResourceModal },
  data () {
    return {
      staffId: this.$route.query.id,
      resourceType: 'staffs'
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
