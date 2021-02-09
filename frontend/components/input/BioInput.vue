<template>
  <v-text-field
    v-model="data"
    :rules="validation"
    :label="label"
    :required="required"
    :readonly="readonly"
    :outlined="outlined"
  />
</template>

<script>

export default {
  name: 'BioInput',

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
      default: 'Hobbies / Interests'
    }
  },

  data () {
    return {
      data: this.value,
      validation: []
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
