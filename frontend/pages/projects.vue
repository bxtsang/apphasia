<template>
  <div>
    <IndividualProjectView v-if="projectId" :resourceType="resourceType"/>
    <v-container v-else class="pa-0" fluid>
      <v-row>
        <v-col>
          <AddResourceModal :resourceType="resourceType" />
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
import IndividualProjectView from './../components/project/IndividualProjectView'

export default {
  components: { IndividualProjectView },
  data () {
    return {
      isLoading: true,
      projectId: this.$route.query.id,
      resourceType: 'projects',
      projects: []
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
