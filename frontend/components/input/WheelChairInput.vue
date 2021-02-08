<template>
  <v-select
    v-if="type === 'select'"
    v-model="data"
    :items="OPTIONS"
    :rules="validation"
    :label="!placeholderOnly ? label : ''"
    :placeholder="placeholderOnly ? label : ''"
    :required="required"
    :readonly="readonly"
    :outlined="outlined"
  />
  <v-radio-group v-else v-model="data" :rules="validation">
    <v-radio v-for="option in OPTIONS" :key="option.value" :label="option.text" :value="option.value" :readonly="readonly"/>
  </v-radio-group>
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
    },
    label: {
      type: String,
      default: 'Wheelchair needed?'
    },
    type: {
      type: String,
      default: 'select'
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
