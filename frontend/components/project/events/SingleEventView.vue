<template>
  <v-container class="pa-0 ma-0">
    <v-row>
      <v-col class="d-flex align-center">
        <v-btn icon @click="$emit('home')">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <span>Event Name</span>
      </v-col>
      <v-col class="d-flex align-center justify-end">
        <v-btn color="primary">Edit</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          label="Event Name"
        />
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  props: {
    event: {
      type: Object,
      default: null
    }
  },
  data () {
    return {}
  }
}
</script>
