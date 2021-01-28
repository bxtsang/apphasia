<template>
  <v-text-field
    v-model="data"
    :rules="validation"
    label="Nickname / Alias"
    :required="required"
    :readonly="readonly"
    :outlined="true"
  />
</template>

<script>

export default {
  name: 'AliasInput',

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
