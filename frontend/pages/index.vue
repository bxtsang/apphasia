<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" lg="8">
        <TimelineWidget></TimelineWidget>
        <NotificationList></NotificationList>
      </v-col>
      <v-col cols="12" lg="4">
        <CalendarWidget></CalendarWidget>
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
