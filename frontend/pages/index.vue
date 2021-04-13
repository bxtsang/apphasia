<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" lg="6">
        <TimelineWidget />
      </v-col>
      <v-col cols="12" lg="6">
        <NotificationWidget />
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  middleware: ['isEmailVerified'],
  data () {
    return {
      loading: false
    }
  }
}
</script>
