<template>
  <v-row>
    <v-col>
      <v-card class="px-6 py-3">
        <h1 class="title hover-underline">
          <NuxtLink to="/staff">
            Staff
          </NuxtLink> / {{ staffId ? staffId : "" }}
        </h1>
        <v-row>
          Hello
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>

export default {
  data () {
    return {
      isLoading: true,
      staffId: this.$route.query.id
    }
  }
}
</script>
<style scoped>
.hover-underline > a {
  color: inherit;
  text-decoration: none !important;
}
.hover-underline > a:hover {
  text-decoration: underline !important;
}
</style>
