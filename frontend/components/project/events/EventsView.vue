<template>
  <v-container class="pa-0 ma-0" fluid>
        <SingleEventView v-if="eventId" @home="tab = 0" :resourceType="resourceType" />
        <v-card v-else outlined>
          <ListingQuery :resourceType="resourceType" :eventParams="{ project_id: projectId }" />
        </v-card>
  </v-container>
</template>
<script>
export default {
  data () {
    return {
      resourceType: 'events',
      projectId: this.$route.query.id,
      eventId: this.$route.query.event
    }
  },
  watch: {
    '$route.query.event': {
      handler () {
        this.eventId = this.$route.query.event
      }
    }
  }
}
</script>
