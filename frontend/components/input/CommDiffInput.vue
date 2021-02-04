<template>
  <v-select
    v-model="data"
    :items="COMM_DIFF_OPTIONS"
    label="Communication Difficults"
    :rules="validation"
    :required="required"
    :readonly="readonly"
    :disabled="disabled"
    multiple
  />
</template>

<script>
import { INPUT_VALIDATION, COMM_DIFF_OPTIONS } from './../../assets/data'

export default {
  name: 'CommDiffInput',

  props: {
    value: {
      type: Array,
      default () {
        return []
      }
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
      INPUT_VALIDATION,
      COMM_DIFF_OPTIONS,
      validation: [...(this.required ? [INPUT_VALIDATION.comm_diff.required] : [])]
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
