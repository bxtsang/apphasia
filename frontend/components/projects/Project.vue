<template>
  <v-card class="pa-6">
    <h1 class="title">{{ project.name }}</h1>
  </v-card>
</template>
<script>
export default {
  props: { project: Object }
}
</script>
