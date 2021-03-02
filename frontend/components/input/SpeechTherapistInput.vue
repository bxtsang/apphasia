<template>
  <v-switch
    v-model="data"
    :rules="validation"
    :label="message"
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

  computed: {
    message () {
      const label = 'Speech Therapist: '
      if (this.data) {
        return label + 'Yes'
      } return label + 'No'
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
