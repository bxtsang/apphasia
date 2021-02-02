<template>
  <v-switch
    v-model="data"
    :rules="validation"
    label="Speech Therapist?"
    :required="required"
    :readonly="readonly"
  />
</template>

<script>

export default {
  name: 'SpeechTherapistInput',

  props: {
    value: {
      type: Boolean,
      default: false
    },
    required: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    }
  },

  data () {
    return {
      data: this.value,
      validation: []
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
