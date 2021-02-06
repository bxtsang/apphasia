<template>
  <v-select
    v-model="data"
    :items="status"
    label="Status"
    :rules="validation"
    :required="required"
    :readonly="readonly"
    :disabled="disabled"
  />
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'VolunteerStatusInput',
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
    status: {
      query () {
        return gql`query getVoltypes {
          status {
            status
          }
        }`
      },
      update: data => data.status.map((item) => {
        return { value: item.status, text: item.status }
      })
    }
  }
}
</script>

<style scoped>

</style>
