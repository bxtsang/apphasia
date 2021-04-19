<template>
  <v-menu
    transition="scale-transition"
    offset-y
    :close-on-content-click="false"
    min-width="auto"
    v-model="menu"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        v-model="data"
        :label="label"
        v-bind="attrs"
        readonly
        :rules="validation"
        :required="required"
        v-on="on"
        :outlined="outlined"
      />
    </template>
    <v-date-picker
      ref="picker"
      v-model="data"
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
    },
    outlined: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: 'Date of Birth'
    }
  },

  data () {
    return {
      menu: false,
      data: this.value,
      validation: [...(this.required ? [INPUT_VALIDATION.dob.required] : [])]
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
    },
    menu (val) {
      val && setTimeout(() => (this.$refs.picker.activePicker = 'YEAR'))
    }
  }
}

</script>
