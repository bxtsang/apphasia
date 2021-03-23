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
          <v-list>
            <NotificationItem v-for="item in notifications" :notification="item" v-bind:key="item.id" />
          </v-list>
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
      ],
      notifications: [
        {
          id: 1,
          type: 'update',
          description: 'Chit Chat Event Updated',
          user: 'User 1'
        },
        {
          id: 2,
          type: 'insert',
          description: 'New Document Added',
          user: 'User 2'
        },
        {
          id: 3,
          type: 'delete',
          description: 'User XX has been archived',
          user: 'User 3'
        },
        {
          id: 4,
          type: 'insert',
          description: 'Befriender assigned to person 1',
          user: 'User 1'
        },
        {
          id: 4,
          type: 'insert',
          description: 'Befriender assigned to person 1',
          user: 'User 1'
        },
        {
          id: 4,
          type: 'insert',
          description: 'Befriender assigned to person 1',
          user: 'User 1'
        },
        {
          id: 4,
          type: 'insert',
          description: 'Befriender assigned to person 1',
          user: 'User 1'
        },
        {
          id: 4,
          type: 'insert',
          description: 'Befriender assigned to person 1',
          user: 'User 1'
        }
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
