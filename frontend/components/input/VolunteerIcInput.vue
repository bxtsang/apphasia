<template>
  <v-select
    v-model="data"
    :items="staffs"
    :label="'Tag IC(s)'"
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
  name: 'VolunteerIcInput',
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
    staffs: {
      query () {
        return gql`query getStaffs {
          staffs {
            id,
            name
          }
        }`
      },
      update: data => data.staffs.map((item) => {
        return { value: item.id, text: item.name }
      })
    }
  }
}
</script>

<style scoped>

</style>
