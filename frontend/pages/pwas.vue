<template>
  <div>
    <!-- <IndividualPWAView v-if="pwaId" :resourceType="resourceType"/>
    <v-container v-else class="pa-0" fluid> -->
    <v-container class="pa-0" fluid>   
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
// import IndividualPWAView from './../components/volunteer/IndividualPWAView'
import ListingQuery from './../components/common/ListingQuery'

export default {
  components: { ListingQuery, AddResourceModal },
  data () {
    return {
      pwaId: this.$route.query.id,
      resourceType: 'pwas'
    }
  },
  watch: {
    '$route.query.id': {
      handler () {
        this.pwaId = this.$route.query.id
      }
    }
  }
}
</script>
