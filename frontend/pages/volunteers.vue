<template>
  <div>
    <IndividualVolunteerView v-if="volunteerId" :resourceType="resourceType"/>
    <v-container v-else class="pa-0" fluid>
      <v-row>
        <v-col>
          <AddResourceModal :resource-type="resourceType" />
          <ReportGenerationButton :resourceType="resourceType"/>
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
import IndividualVolunteerView from './../components/volunteer/IndividualVolunteerView'
import ListingQuery from './../components/common/ListingQuery'

export default {
  components: { ListingQuery, IndividualVolunteerView, AddResourceModal },
  data () {
    return {
      volunteerId: this.$route.query.id,
      resourceType: 'volunteers'
    }
  },
  watch: {
    '$route.query.id': {
      handler () {
        this.volunteerId = this.$route.query.id
      }
    }
  }
}
</script>
