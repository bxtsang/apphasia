<template>
  <v-card class="px-6 py-3">
    <div class="d-flex justify-space-between align-center">
      <h1 class="title">Notifications</h1>
      <v-btn color="primary">Mark all as read</v-btn>
    </div>
    <v-tabs v-model="tab">
      <v-tab
        v-for="option in notificationTabOptions"
        :key="option"
      >
        {{ option }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item
        v-for="option in notificationTabOptions"
        :key="option"
      >
        <div class="notification-wrapper">
          <NotificationList v-if="option === 'unread'"/>
        </div>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>
<script>
export default {
  data () {
    return {
      tab: 'read',
      notificationTabOptions: [
        'unread', 'read'
      ]
    }
  }
}
</script>
<style scoped>
.notification-wrapper {
  max-height: 325px;
  overflow-y: auto;
}
</style>
