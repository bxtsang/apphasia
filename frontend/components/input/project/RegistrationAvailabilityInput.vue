<template>
  <v-switch
    v-model="data"
    :label="`Available for ${resourceType}: ${allowed}`"
  />
</template>

<script>
export default {
  name: 'RegistrationAvailabilityInput',

  props: {
    value: {
      type: Boolean,
      default: false
    },
    resourceType: {
      type: String,
      default: null
    }
  },

  data () {
    return {
      data: this.value
    }
  },

  computed: {
    allowed () {
      if (this.value) {
        return 'Yes'
      } return 'No'
    }
  },

  watch: {
    data: {
      immediate: true,
      handler (newVal) {
        this.$emit('input', newVal)
      }
    }
  }
}
</script>

<style scoped>

</style>
