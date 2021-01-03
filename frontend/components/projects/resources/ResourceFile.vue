<template>
  <v-card class="pa-3 ma-2 d-flex flex-column align-center clickable" outlined width="200">
    <v-icon x-large class="ma-4">mdi-file</v-icon>
    <span>file name.pdf</span>
  </v-card>
</template>
<script>
export default {
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
