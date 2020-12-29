<template>
  <v-card>
    <v-toolbar flat>
      <h1 class="title">{{ project.name }}</h1>
      <v-spacer />
      <v-btn
        fab
        text
        small
        color="primary"
      >
        <v-icon small>
          mdi-chevron-right
        </v-icon>
      </v-btn>
    </v-toolbar>
  </v-card>
</template>
<script>
export default {
  props: { project: Object }
}
</script>
