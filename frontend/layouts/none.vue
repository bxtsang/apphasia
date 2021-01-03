<template>
  <v-app :style="{background: $vuetify.theme.themes[theme].background}">
    <v-main>
      <v-container class="d-flex justify-center align-center" fill-height>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
export default {
  computed: {
    theme () {
      return (this.$vuetify.theme.dark) ? 'dark' : 'light'
    }
  }
}
</script>
