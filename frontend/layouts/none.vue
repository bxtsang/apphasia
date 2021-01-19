<template>
  <v-app :style="{background: $vuetify.theme.themes[theme].background}">
    <Notification />
    <v-main>
      <v-container class="d-flex justify-center align-center" fill-height>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
import Notification from './../components/Notification'

export default {
  components: { Notification },
  computed: {
    theme () {
      return (this.$vuetify.theme.dark) ? 'dark' : 'light'
    }
  }
}
</script>
