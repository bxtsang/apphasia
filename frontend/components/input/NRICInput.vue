<template>
  <v-text-field
    v-model="value"
    :rules="validation"
    label="NRIC"
    :required="required"
    :readonly="readonly"
  />
</template>

<script>
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'NRICInput',

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
      validation: [INPUT_VALIDATION.nric.required, INPUT_VALIDATION.nric.valid]
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
