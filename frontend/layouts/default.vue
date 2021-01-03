<template>
  <v-app :style="{background: $vuetify.theme.themes[theme].background}">
    <v-navigation-drawer fixed app permanent>
      <v-img src="/asg.png"/>
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title">
              Hello, {{ $auth.user.name }}
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
export default {
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
          icon: 'mdi-calendar-check',
          title: 'Projects',
          to: '/projects'
        },
        {
          icon: 'mdi-clipboard-account',
          title: 'Manage PWAs',
          to: '/pwa'
        },
        {
          icon: 'mdi-account-group',
          title: 'Manage Staff',
          to: '/staff'
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
      this.$auth.logout()
    }
  }
}
</script>
