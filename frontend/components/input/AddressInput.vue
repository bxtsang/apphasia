<template>
  <v-text-field
    v-model="data"
    :rules="validation"
    :label="label"
    :required="required"
    :readonly="readonly"
    :outlined="outlined"
    data-cy="cy-form-address-input"
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
    },
    label: {
      type: String,
      default: 'Home Address'
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
