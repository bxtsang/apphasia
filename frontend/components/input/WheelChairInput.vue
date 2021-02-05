<template>
  <v-select
    v-model="data"
    :items="OPTIONS"
    :rules="validation"
    label="Wheelchair needed?"
    :required="required"
    :readonly="readonly"
    :outlined="outlined"
  />
</template>

<script>
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'WheelChairInput',

  props: {
    value: {
      type: Boolean,
      default: null
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
      OPTIONS: [
        { text: 'Yes', value: true },
        { text: 'No', value: false }
      ],
      data: this.value,
      validation: [...(this.required ? [INPUT_VALIDATION.wheelchair.required] : [])]
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
