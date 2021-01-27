<template>
  <v-text-field
    v-model="data"
    :rules="validation"
    label="Current Place of Work / Study"
    :required="required"
    :readonly="readonly"
  />
</template>

<script>

export default {
  name: 'WorkplaceInput',

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
    }
  }
}

</script>
