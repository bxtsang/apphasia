<template>
  <v-text-field
    v-model="data"
    :rules="validation"
    :label="label"
    :required="required"
    :readonly="readonly"
    :outlined="outlined"
  />
</template>

<script>
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'ContactInput',

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
      default: 'Contact'
    }
  },

  data () {
    return {
      data: this.value,
      validation: [INPUT_VALIDATION.contact.required, INPUT_VALIDATION.contact.valid]
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
