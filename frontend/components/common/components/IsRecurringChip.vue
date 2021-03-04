<template>
  <v-chip  v-if="value" color="primary">
    <v-icon>mdi-repeat</v-icon>
  </v-chip>
</template>
<script>

export default {
  props: {
    value: {
      type: Boolean,
      default: false
    }
  }
}
</script>
