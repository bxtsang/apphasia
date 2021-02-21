<template>
  <v-container class="pa-0 ma-0" fluid>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-card outlined>
          <ListingQuery :resourceType="resourceType" :eventParams="{ project_id: projectId }" :customNavigation="goToSingleEvent" />
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <SingleEventView @home="tab = 0; event = null" :event="singleEvent"/>
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
      singleEvent: null
    }
  },
  methods: {
    goToSingleEvent (event) {
      this.tab = 1
      this.singleEvent = event
    }
  }
}
</script>
