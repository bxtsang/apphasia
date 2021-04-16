<template>
  <v-list-item class="px-0">
    <v-list-item-avatar :color="color">
      <v-icon dark>{{ icon }}</v-icon>
    </v-list-item-avatar>

    <v-list-item-content>
      <v-list-item-title class="font-weight-bold pb-1">
        <p :title="notification.message" class="pa-0 ma-0 d-flex align-center"><NuxtLink class="notification-link" :to="link">{{ notification.message }}<v-icon small>mdi-open-in-new</v-icon></NuxtLink></p>
      </v-list-item-title>
      <v-list-item-subtitle>
        {{ $moment(notification.created_at.slice(0,10)).format('DD MMM YYYY') }}
      </v-list-item-subtitle>
    </v-list-item-content>

    <v-list-item-action class="pr-3">
      <v-menu bottom left offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            v-bind="attrs"
            v-on="on"
            icon
            :loading="isLoading"
          >
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item link @click="setNotificationRead">
            <v-list-item-avatar>
              <v-icon>{{ notification.is_read ? 'mdi-eye-off' : 'mdi-eye'}}</v-icon>
            </v-list-item-avatar>
            <v-list-item-title>Mark as {{ notification.is_read ? 'Unread' : 'Read'}}</v-list-item-title>
          </v-list-item>
          <v-list-item link :to="link">
            <v-list-item-avatar>
              <v-icon>mdi-open-in-new</v-icon>
            </v-list-item-avatar>
            <v-list-item-title>Go to Resource</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-list-item-action>
  </v-list-item>
</template>
<script>
import UpdateSingleNotification from './../../graphql/notifications/UpdateSingleNotification.graphql'

export default {
  props: {
    notification: {
      type: Object,
      default () {
        return null
      }
    },
    query: {
      type: Object,
      default () {
        return null
      }
    }
  },
  data () {
    return {
      isLoading: false
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
      return `/${this.notification.type}?id=${this.notification.entity_id}${this.notification.type === 'projects' ? '&tab=1' : ''}`
    }
  },
  methods: {
    setNotificationRead () {
      this.isLoading = true
      this.$apollo.mutate({
        mutation: UpdateSingleNotification,
        variables: {
          id: this.notification.id,
          is_read: !this.notification.is_read
        }
      }).then((data) => {
        this.isLoading = false
        if (!this.notification.is_read) {
          this.query.refetch()
        } else {
          this.$apollo.vm.$apolloProvider.defaultClient.resetStore()
        }
      }).catch((error) => {
        this.isLoading = false
        this.$store.commit('notification/newNotification', [error.message, 'error'])
      })
    }
  }
}
</script>
<style scoped>
.notification-link{
  color: initial;
  text-decoration: none;
}
.notification-link:hover {
  text-decoration: underline;
}
</style>
