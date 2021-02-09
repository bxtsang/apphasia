<template>
  <v-radio-group v-model="data" :rules="validation" row>
    <v-radio v-for="role in ROLE_OPTIONS" :key="role.value" :label="role.label" :value="role.value" :readonly="readonly"/>
  </v-radio-group>
</template>

<script>
import { INPUT_VALIDATION, ROLE_OPTIONS } from './../../assets/data'

export default {
  name: 'RoleInput',

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
      ROLE_OPTIONS,
      data: this.value,
      validation: [INPUT_VALIDATION.role.required]
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
