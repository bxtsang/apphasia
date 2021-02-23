<template>
  <v-select
    v-model="data"
    :items="FREQUENCY_OPTIONS"
    :label="label"
    :rules="validation"
  />
</template>

<script>

export default {
  name: 'FrequencyInput',

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
      FREQUENCY_OPTIONS: [
        'None',
        'Weekly',
        'Monthly'
      ],
      validation: [...(this.required ? [v => !!v || 'Frequency is required'] : [])]
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
