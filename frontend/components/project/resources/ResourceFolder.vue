<template>
  <v-card class="ma-2 d-flex align-center clickable" outlined width="200">
    <v-icon class="ma-4">
      mdi-folder
    </v-icon>
    <span> {{ folder.name }}</span>
  </v-card>
</template>
<script>
export default {
  props: {
    folder: {
      type: Object,
      default: null
    }
  },
  data () {
    return {}
  }
}
</script>
<style scoped>
.clickable {
  cursor: pointer;
}
</style>
