<template>
  <v-list>
    <NotificationItem v-for="item in notifications" :notification="item" v-bind:key="item.id" />
  </v-list>
</template>
<script>
export default {
  data () {
    return {
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
