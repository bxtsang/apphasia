<template>
  <v-menu
    transition="scale-transition"
    offset-y
    :close-on-content-click="false"
    min-width="auto"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        v-model="value"
        label="Date of Birth"
        v-bind="attrs"
        readonly
        :rules="validation"
        :required="required"
        v-on="on"
      />
    </template>
    <v-date-picker
      ref="picker"
      v-model="value"
      :max="new Date().toISOString().substr(0, 10)"
    />
  </v-menu>
</template>

<script>
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'DateOfBirthInput',

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
      validation: [INPUT_VALIDATION.dob.required]
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
