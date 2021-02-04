<template>
  <v-text-field
    v-model="data"
    :label="label"
    :readonly="readonly"
    :outlined="outlined"
    :disabled="disabled"
  />
</template>

<script>
export default {
  name: 'GeneralOptionalText',
  props: {
    value: {
      type: String,
      default: ''
    },
    readonly: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    outlined: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: ''
    }
  },

  data () {
    return {
      data: this.value
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
