<template>
  <v-radio-group v-model="data" :rules="validation">
    <v-radio
      v-for="role in CONSENT_OPTIONS"
      :key="role.value"
      :label="role.label"
      :value="role.value"
      :readonly="readonly"
    />
  </v-radio-group>
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
    }
  },

  data () {
    return {
      CONSENT_OPTIONS: [
        { label: 'Yes, I wish to receive updates about Aphasia SG events and programmes!', value: true },
        { label: 'No', value: false }
      ],
      data: this.value,
      validation: [INPUT_VALIDATION.consent.required]
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
