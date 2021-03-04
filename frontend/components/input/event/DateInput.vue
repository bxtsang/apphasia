<template>
  <v-menu
    transition="scale-transition"
    offset-y
    :close-on-content-click="false"
    min-width="auto"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        v-model="data"
        :label="label"
        v-bind="attrs"
        readonly
        :rules="validation"
        :required="required"
        v-on="on"
      />
    </template>
    <v-date-picker
      ref="picker"
      v-model="data"
    />
  </v-menu>
</template>

<script>

export default {
  name: 'DateInput',

  props: {
    value: {
      type: String,
      default: ''
    },
    required: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: 'Field'
    }
  },

  data () {
    return {
      data: this.value,
      validation: [...(this.required ? [v => !!v || `${this.label} is required`] : [])]
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
