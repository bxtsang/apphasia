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
  },
  computed: {
    INTERVAL_OPTIONS () {
      const unit = this.type === 'Monthly' ? 'month' : 'week'
      let options = []
      const limit = this.type === 'Monthly' ? 12 : 4
      console.log(Array(limit))
      for (const index of Array(limit).keys()) {
        options = [...options, {
          value: index + 1,
          text: `${index + 1} ${unit}${index + 1 > 1 ? 's' : ''}`
        }]
      }
      console.log(options)
      return options
    }
  }
}

</script>
