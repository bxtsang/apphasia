<template>
  <v-autocomplete
    v-model="data"
    :label="label"
    :items="staffs"
    item-text="name"
    item-value="id"
    :readonly="readonly"
    :rules="validation"
    :searchInput.sync="searchInput"
    @change="searchInput=''"
  />
</template>
<script>
import gql from 'graphql-tag'

export default {
  data () {
    return {
      data: this.value,
      validation: [v => v !== -1 || 'Staff is Required'],
      searchInput: ''
    }
  },
  props: {
    value: {
      type: Number,
      default: -1
    },
    label: {
      type: String,
      default: ''
    },
    readonly: {
      type: Boolean,
      default: false
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
      }
    }
  }
}
</script>
