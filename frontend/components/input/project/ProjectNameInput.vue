<template>
  <v-text-field
    v-model="data"
    :rules="validation"
    :label="label"
    :readonly="readonly"
  />
</template>

<script>

export default {
  name: 'ProjectNameInput',

  props: {
    value: {
      type: String,
      default: ''
    },
    readonly: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: 'Project Name'
    }
  },

  data () {
    return {
      data: this.value,
      validation: [v => !!v || 'Project Name is required']
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
