<template>
  <v-textarea
    v-model="data"
    :rules="validation"
    :label="label"
    :readonly="readonly"
    auto-grow
    />
</template>

<script>

export default {
  name: 'ProjectNotesInput',

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
      default: 'Project Notes'
    }
  },

  data () {
    return {
      data: this.value,
      validation: [v => !!v || 'Project Notes is required']
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
