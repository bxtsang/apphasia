<template>
  <v-row no-gutters>
    <v-col cols="3" class="d-flex justify-start align-center">
      <v-subheader class="pa-0">{{ label }}</v-subheader>
    </v-col>
    <v-col cols="9">
      <v-select
        v-model="data"
        :items="DAY"
        :rules="validation"
      />
    </v-col>
  </v-row>
</template>

<script>
import { DAY } from './../../../assets/data'

export default {
  name: 'DayInput',

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
    }
  },
  data () {
    return {
      data: this.value,
      DAY,
      validation: [...(this.required ? [v => (v > -1 && v < 7) || 'Day is required'] : [])]
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
