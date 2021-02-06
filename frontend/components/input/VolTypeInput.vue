<template>
  <v-select
    v-model="data"
    :items="voltypes"
    label="Volunteer Type"
    :rules="validation"
    :required="required"
    :readonly="readonly"
    :disabled="disabled"
    multiple
  />
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'VolTypeInput',
  props: {
    value: {
      type: Array,
      default () {
        return []
      }
    },
    required: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    },
    disabled: {
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
  },

  apollo: {
    voltypes: {
      query () {
        return gql`query getVoltypes {
          voltypes {
            type
          }
        }`
      },
      update: data => data.voltypes.map((item) => {
        return { value: item.type, text: item.type.replace('_', ' ') }
      })
    }
  }
}
</script>

<style scoped>

</style>
