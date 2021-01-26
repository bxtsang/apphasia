<template>
  <v-text-field
    v-model="inputValue"></v-text-field>
</template>

<script>
export default {
  name: 'EmailInput',

  props: {
    inputValue: {
      type: String,
      default: ''
    }
  },

  watch: {
    inputValue (newValue, oldValue) {
      this.$emit('input', newValue)
    }
  }
}

</script>

<style scoped>

</style>
