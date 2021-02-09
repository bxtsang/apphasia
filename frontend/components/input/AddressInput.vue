<template>
  <v-text-field
    v-model="data"
    :rules="validation"
    label="Home Address"
    :required="required"
    :readonly="readonly"
    :outlined="outlined"
  />
</template>

<script>
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'AddressInput',

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
    },
    outlined: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      data: this.value,
      validation: [...(this.required ? [INPUT_VALIDATION.address.required] : [])]
    }
  },

  watch: {
    data: {
      immediate: true,
      handler (newValue, oldValue) {
        this.$emit('input', newValue)
      }
    },
    value: {
      handler (newValue, oldValue) {
        this.data = this.value
      }
    }
  }
}

</script>
