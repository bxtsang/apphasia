<template>
  <v-text-field
    v-model="value"
    :rules="validation"
    label="Hobbies / Interests"
    :required="required"
    :readonly="readonly"
  />
</template>

<script>

export default {
  name: 'BioInput',

  props: {
    value: {
      type: String,
      default: ''
    },
    required: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      validation: []
    }
  },

  watch: {
    value: {
      immediate: true,
      handler (newValue, oldValue) {
        this.$emit('input', newValue)
      }
    }
  }
}

</script>
