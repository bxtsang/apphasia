<template>
  <v-row no-gutters>
    <v-col cols="3" class="d-flex justify-start align-center">
      <v-subheader class="pa-0">{{ label }}</v-subheader>
    </v-col>
    <v-col cols="6">
      <v-select
        v-model="data"
        :items="WEEK"
        :rules="validation"
      />
    </v-col>
    <v-col cols="3" class="d-flex justify-center align-center">
      <v-subheader class="pa-0">Week</v-subheader>
    </v-col>
  </v-row>
</template>

<script>
import { WEEK } from './../../../assets/data'

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
      WEEK,
      validation: [...(this.required ? [v => (v > 0 & v < 7) || 'Week is required'] : [])]
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
