<template>
    <v-list-item link class="px-0">
      <v-list-item-avatar :color="color">
        <v-icon dark>{{ icon }}</v-icon>
      </v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title class="font-weight-bold pb-1" v-text="notification.description" />
        <v-list-item-subtitle v-text="notification.user" />
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
      switch (this.notification.type) {
        case 'insert':
          return 'success'
        case 'update':
          return 'warning'
        case 'delete':
          return 'error'
        default:
          return 'warning'
      }
    },
    icon () {
      switch (this.notification.type) {
        case 'insert':
          return 'mdi-plus-circle-outline'
        case 'update':
          return 'mdi-alert-circle-outline'
        case 'delete':
          return 'mdi-alert-outline'
        default:
          return 'mdi-alert-circle-outline'
      }
    }
  }
}
</script>
