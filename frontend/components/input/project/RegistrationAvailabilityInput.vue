<template>
  <v-switch
    v-model="data"
    :label="`Available for ${resourceType}: ${allowed}`"
    :readonly="readonly"
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
    },
    readonly: {
      type: Boolean,
      default: false
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
