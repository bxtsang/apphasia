<template>
  <v-container class="pa-0 ma-0" fluid>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <ListingQuery :resourceType="resourceType" :eventParams="{ project_id: projectId }" :customNavigation="goToSingleEvent" />
      </v-tab-item>
      <v-tab-item>
        <SingleEventView @home="tab = 0"/>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>
<script>
export default {
  data () {
    return {
      tab: 0,
      singleEvent: -1,
      resourceType: 'events',
      projectId: this.$route.query.id
    }
  },
  methods: {
    goToSingleEvent (eventId) {
      this.tab = 1
      this.singleEvent = eventId
    }
  }
}
</script>
