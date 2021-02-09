<template>
  <v-select
    v-model="data"
    :items="PWA_PREFFERED_CONTACTED_OPTIONS"
    :label="label"
    :rules="validation"
    :required="required"
    :readonly="readonly"
    :disabled="disabled"
    :outlined="outlined"
    :hint="hint"
    :persistent-hint="hint ? true : false"
  />
</template>

<script>
import { INPUT_VALIDATION, PWA_PREFFERED_CONTACTED_OPTIONS } from './../../assets/data'

export default {
  name: 'PWAPreferredCommInput',

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
    },
    outlined: {
      type: Boolean
    },
    label: {
      type: String,
      default: 'Preferred mode of communication'
    },
    hint: {
      type: String,
      default: ''
    }
  },

  data () {
    return {
      data: this.value,
      INPUT_VALIDATION,
      PWA_PREFFERED_CONTACTED_OPTIONS,
      validation: [...(this.required ? [INPUT_VALIDATION.pref_comm.required] : [])]
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
