<template>
  <v-card class="px-6 py-3 mb-6">
    <h1 class="title">Upcoming Events</h1>
    <v-timeline :dense="$vuetify.breakpoint.smAndDown">
    </v-timeline>
  </v-card>
</template>
<script>
export default {
  data () {
    return {}
  }
}
</script>
