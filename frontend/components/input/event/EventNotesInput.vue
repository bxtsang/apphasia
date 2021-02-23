<template>
  <v-textarea
    v-model="data"
    :label="label"
    :readonly="readonly"
    auto-grow
    />
</template>

<script>

export default {
  name: 'EventNotesInput',

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
      default: 'Event Notes'
    }
  },

  data () {
    return {
      data: this.value,
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
