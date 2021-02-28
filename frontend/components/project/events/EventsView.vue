<template>
  <v-container class="pa-0 ma-0" fluid>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-card outlined>
          <ListingQuery :resourceType="resourceType" :eventParams="{ project_id: projectId }" />
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <SingleEventView v-if="eventId" @home="tab = 0" :resourceType="resourceType" />
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>
<script>
export default {
  data () {
    return {
      tab: 0,
      resourceType: 'events',
      projectId: this.$route.query.id,
      eventId: this.$route.query.event ? Number(this.$route.query.event) : null
    }
  },
  watch: {
    '$route.query.event': {
      handler () {
        this.eventId = Number(this.$route.query.event)
        if (this.eventId) {
          this.tab = 1
        } else {
          this.tab = 0
        }
      },
      immediate: true
    }
  }
}
</script>
