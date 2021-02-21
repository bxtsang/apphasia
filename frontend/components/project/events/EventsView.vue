<template>
  <v-container class="pa-0 ma-0" fluid>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <ListingQuery :resourceType="resourceType"/>
        <v-btn @click="tab = 1">next</v-btn>
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
      resourceType: 'events'
    }
  }
}
</script>
