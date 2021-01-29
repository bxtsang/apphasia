<template>
  <v-select
    v-model="data"
    :items="GENDER_OPTIONS"
    :rules="validation"
    label="Gender"
    :required="required"
    :readonly="readonly"
    :outlined="outlined"
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
    },
    outlined: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      GENDER_OPTIONS,
      data: this.value,
      validation: [INPUT_VALIDATION.gender.required]
    }
  },

  watch: {
    data: {
      immediate: true,
      handler (newValue, oldValue) {
        this.$emit('input', newValue)
      }
    }
  }
}

</script>
