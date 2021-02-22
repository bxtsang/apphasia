<template>
  <v-select
    v-model="data"
    :items="DAY"
    :label="label"
    :rules="validation"
  />
</template>

<script>
import { DAY } from './../../../assets/data'

export default {
  name: 'DayInput',

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
    }
  },
  data () {
    return {
      data: this.value,
      DAY,
      validation: [...(this.required ? [v => !!v || 'Day is required'] : [])]
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
