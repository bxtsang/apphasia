<template>
  <v-app :style="{background: $vuetify.theme.themes[theme].background}">
    <Notification />
    <v-navigation-drawer fixed app permanent>
      <v-img src="/asg.png" />
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title d-flex flex-column">
              <span v-if="fullname">Hello, {{ fullname }}</span>
              <v-progress-circular v-else indeterminate color="primary" class="align-self-center"/>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider />
      <v-list nav dense>
        <v-subheader class="py-0">
          General
        </v-subheader>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          color="primary"
          link
          router
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-divider />
      <v-list dense nav>
        <v-subheader class="py-0">
          Settings
        </v-subheader>
        <v-list-item
          v-for="(item, i) in settings"
          :key="i"
          :to="item.to"
          color="primary"
          link
          router
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <v-list dense nav>
          <v-list-item link @click="logout">
            <v-list-item-icon>
              <v-icon>{{ 'mdi-logout' }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>
    <v-main>
      <div class="pa-6">
        <nuxt />
      </div>
    </v-main>
  </v-app>
</template>

<script>
import gql from 'graphql-tag'
import Notification from './../components/Notification'

export default {
  components: { Notification },
  middleware: ['isLoggedIn'],
  data () {
    return {
      items: [
        {
          icon: 'mdi-view-dashboard',
          title: 'Dashboard',
          to: '/'
        },
        {
          icon: 'mdi-clipboard-account',
          title: 'Manage PWAs',
          to: '/pwas'
        },
        {
          icon: 'mdi-hand-heart',
          title: 'Manage Volunteers',
          to: '/volunteers'
        },
        {
          icon: 'mdi-calendar-check',
          title: 'Projects',
          to: '/projects'
        },
        {
          icon: 'mdi-account-group',
          title: 'Manage Staffs',
          to: '/staffs'
        }
      ],
      settings: [
        {
          icon: 'mdi-cog',
          title: 'Settings',
          to: '/settings'
        },
        {
          icon: 'mdi-bell',
          title: 'Notifications',
          to: '/notifications'
        }
      ]
    }
  },
  computed: {
    theme () {
      return (this.$vuetify.theme.dark) ? 'dark' : 'light'
    }
  },
  methods: {
    logout () {
      this.$apolloHelpers.onLogout()
      this.$auth.logout()
    },
    checkToken () {
      if (
        this.$store.state.token_expiry.expiration === null ||
        new Date(this.$store.state.token_expiry.expiration) <= new Date()
      ) {
        console.log('force out')
        this.logout()
        this.$nuxt.$emit('new-notification', 'Token expired. Please login again.')
      } else {
        console.log(new Date(this.$store.state.token_expiry.expiration))
      }
    }
  },
  apollo: {
    fullname: {
      query () {
        return gql`query($email: String!) {
          staffs(where: {email: {_eq: $email}}) {
            name
          }
        }`
      },
      variables () {
        return {
          email: this.$auth.user.email
        }
      },
      update: data => data.staffs[0].name
    }
  },
  created () {
    this.$nuxt.$on('new-notification', (message) => {
      console.log('trigger default')
      this.$store.commit('notification/newNotification', [message, 'error'])
    })
  },
  mounted () {
    this.checkToken()
    setInterval(this.checkToken, 60000)
  },
  watch: {
    '$route.query': {
      handler (newVal, old) {
        this.checkToken()
      }
    }
  }
}
// cache clear code
// mounted () {
//   this.$apollo.vm.$apolloProvider.defaultClient.cache.data.clear()
// }
// Object.keys(cache.data.data).forEach(key =>
//   key.match(/^Item/) && cache.data.delete(key)
// )
</script>
