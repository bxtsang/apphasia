<template>
  <v-select
    v-model="data"
    :items="PWA_CONTACT_STATUS_OPTIONS"
    label="Status"
    :rules="validation"
    :required="required"
    :readonly="readonly"
    :disabled="disabled"
  />
</template>

<script>
import { PWA_CONTACT_STATUS_OPTIONS } from './../../assets/data'

export default {
  name: 'PWAContactStatusInput',

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
    disabled: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      data: this.value,
      PWA_CONTACT_STATUS_OPTIONS,
      validation: []
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
