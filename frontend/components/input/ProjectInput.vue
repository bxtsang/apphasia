<template>
  <v-select
    v-model="data"
    :items="projects"
    label="Projects Involved"
    :rules="validation"
    :required="required"
    :readonly="readonly"
    multiple
  />
</template>

<script>
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  name: 'ProjectInput',

  props: {
    value: {
      type: Array,
      default () {
        return []
      }
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
      data: this.value,
      projects: ['project1'],
      validation: [INPUT_VALIDATION.address.required]
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
