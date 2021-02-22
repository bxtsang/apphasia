<template>
  <v-select
    v-model="data"
    :items="INTERVAL_OPTIONS"
    :label="label"
    :rules="validation"
  />
</template>

<script>

export default {
  name: 'IntervalInput',

  props: {
    value: {
      type: String,
      default: 'None'
    },
    required: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: 'Repeat'
    },
    type: {
      type: String,
      default: 'Day'
    }
  },
  data () {
    return {
      data: this.value,
      INTERVAL_OPTIONS: [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12
      ],
      validation: [...(this.required ? [v => !!v || 'Interval is required'] : [])]
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
