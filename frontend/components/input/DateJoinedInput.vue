<template>
  <v-menu
    transition="scale-transition"
    offset-y
    :close-on-content-click="false"
    min-width="auto"
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
      />
    </template>
    <v-date-picker
      ref="picker"
      v-model="data"
    />
  </v-menu>
</template>

<script>
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'DateJoinedInput',

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
    label: {
      type: String,
      default: 'Date Joined'
    }
  },

  data () {
    return {
      data: this.value,
      validation: [INPUT_VALIDATION.dateJoined.required]
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
