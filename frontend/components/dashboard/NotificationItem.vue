<template>
    <v-list-item link class="px-0" :to="link">
      <v-list-item-avatar :color="color">
        <v-icon dark>{{ icon }}</v-icon>
      </v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title class="font-weight-bold pb-1" v-text="notification.message" />
        <v-list-item-subtitle v-text="notification.staff.name" />
      </v-list-item-content>

      <v-list-item-action>
        <v-btn icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
</template>
<script>
export default {
  props: {
    notification: {
      type: Object,
      default () {
        return null
      }
    }
  },
  computed: {
    color () {
      switch (this.notification.operation) {
        case 'INSERT':
          return 'success'
        case 'UPDATE':
          return 'warning'
        case 'DELETE':
          return 'error'
        default:
          return 'warning'
      }
    },
    icon () {
      switch (this.notification.operation) {
        case 'INSERT':
          return 'mdi-plus-circle-outline'
        case 'UPDATE':
          return 'mdi-alert-circle-outline'
        case 'DELETE':
          return 'mdi-alert-outline'
        default:
          return 'mdi-alert-circle-outline'
      }
    },
    link () {
      return `/${this.notification.type}?id=${this.notification.entity_id}`
    }
  }
}
</script>
