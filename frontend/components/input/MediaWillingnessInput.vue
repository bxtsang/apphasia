<template>
  <v-select
    v-model="data"
    :items="OPTIONS"
    :rules="validation"
    label="Agreeable to speak to Media?"
    :required="required"
    :readonly="readonly"
    :outlined="outlined"
  />
</template>

<script>

export default {
  name: 'MediaWillingnessInput',

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
    }
  },

  data () {
    return {
      OPTIONS: [
        { text: 'Yes', value: true },
        { text: 'No', value: false }
      ],
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
