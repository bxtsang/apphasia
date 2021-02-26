<template>
  <v-row no-gutters>
    <v-col cols="3" class="d-flex justify-start align-center">
      <v-subheader class="pa-0">{{ label }}</v-subheader>
    </v-col>
    <v-col cols="6">
      <v-select
        v-model="data"
        :items="INTERVAL_OPTIONS"
        :rules="validation"
      />
    </v-col>
    <v-col cols="3" class="d-flex justify-center align-center">
      <v-subheader class="pa-0">{{ UNIT_MEASURE }}</v-subheader>
    </v-col>
  </v-row>
</template>

<script>

export default {
  name: 'IntervalInput',

  props: {
    value: {
      type: Number,
      default: -1
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
      validation: [...(this.required ? [v => v > 0 || 'Interval is required'] : [])]
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
      let options = []
      const limit = this.type === 'Monthly' ? 12 : 4
      for (const index of Array(limit).keys()) {
        options = [...options, index + 1]
      }
      return options
    },
    UNIT_MEASURE () {
      return this.type === 'Monthly' ? 'Month(s)' : 'Week(s)'
    }
  }
}

</script>
