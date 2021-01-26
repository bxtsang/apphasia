<template>
  <v-select
    v-model="value"
    :items="GENDER_OPTIONS"
    :rules="validation"
    label="Gender"
    :required="required"
    :readonly="readonly"
  />
</template>

<script>
import { GENDER_OPTIONS } from './../../assets/data'
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'GenderInput',

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
      GENDER_OPTIONS,
      validation: [INPUT_VALIDATION.gender.required]
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
