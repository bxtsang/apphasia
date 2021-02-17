<template>
  <v-chip color="primary">
    <v-icon v-if="value">mdi-repeat</v-icon><v-icon v-else>mdi-repeat-off</v-icon>{{ value ? ' Yes' : ' No' }}
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
