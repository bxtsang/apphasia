<template>
  <v-radio-group v-if="inputType === 'radio'" v-model="data" :rules="validation" label="Agreeable to receive promotional materials?">
    <v-radio
      v-for="role in CONSENT_OPTIONS"
      :key="role.value"
      :label="role.text"
      :value="role.value"
      :readonly="readonly"
    />
  </v-radio-group>
  <v-select
    v-else
    v-model="data"
    :items="CONSENT_OPTIONS"
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
  name: 'ConstInput',

  props: {
    value: {
      type: null,
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
    inputType: {
      type: String,
      default: 'radio'
    },
    label: {
      type: String,
      default: 'Agreeable to receive promotional materials?'
    }
  },

  data () {
    return {
      CONSENT_OPTIONS: [
        { text: 'Yes', value: true },
        { text: 'No', value: false }
      ],
      data: this.value,
      validation: [...(this.required ? [INPUT_VALIDATION.consent.required] : [])]
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
