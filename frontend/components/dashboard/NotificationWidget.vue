<template>
  <v-card class="px-6 py-3">
    <div class="d-flex justify-space-between align-center">
      <h1 class="title">Notifications</h1>
      <v-btn v-if="tab === notificationTabOptions.indexOf('unread')" color="primary" @click="markAllRead" :loading="isLoading">Mark all as read</v-btn>
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
          <ReadNotificationList v-if="option === 'read'"/>
        </div>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>
<script>
import UpdateAllNotifications from './../../graphql/notifications/UpdateAllNotifications.graphql'

export default {
  data () {
    return {
      tab: 'unread',
      notificationTabOptions: [
        'unread', 'read'
      ],
      isLoading: false
    }
  },
  methods: {
    markAllRead () {
      this.isLoading = true
      this.$apollo.mutate({
        mutation: UpdateAllNotifications,
        variables: {
          staff: this.$auth.user['custom:hasura_id'],
          is_read: true
        }
      }).then((data) => {
        this.isLoading = false
      }).catch((error) => {
        this.isLoading = false
        this.$store.commit('notification/newNotification', [error.message, 'error'])
      })
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
