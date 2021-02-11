<template>
  <v-chip color="primary"><v-icon>mdi-repeat</v-icon>{{ value ? ' Yes' : ' No' }}</v-chip>
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
