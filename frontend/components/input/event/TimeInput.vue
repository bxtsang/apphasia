<template>
    <v-menu
        ref="menu"
        v-model="isOpen"
        :close-on-content-click="false"
        :nudge-right="40"
        :return-value.sync="data"
        transition="scale-transition"
        offset-y
        max-width="290px"
        min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="data"
            :label="label"
            append-icon="mdi-clock-time-four-outline"
            readonly
            v-bind="attrs"
            v-on="on"
            :rules="validation"
          />
        </template>
        <v-time-picker
        ampm-in-title
          v-if="isOpen"
          v-model="data"
          full-width
          scrollable
          @click:minute="$refs.menu.save(data)"
        />
      </v-menu>
</template>
<script>

export default {
  name: 'TimeInput',

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
      isOpen: false,
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
