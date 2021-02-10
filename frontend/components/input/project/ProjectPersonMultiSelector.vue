<template>
  <v-autocomplete
    v-model="data"
    :label="label"
    :items="items"
    chips
    item-text="name"
    item-value="id"
    multiple
    :readonly="readonly"
  />
</template>
<script>
import gql from 'graphql-tag'

export default {
  data () {
    return {
      data: this.value
    }
  },
  props: {
    value: {
      type: Array,
      default () {
        return []
      }
    },
    label: {
      type: String,
      default: ''
    },
    readonly: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: ''
    }
  },

  computed: {
    items () {
      if (this.type === 'staffs') {
        return this.staffs
      }
      if (this.type === 'volunteers') {
        return this.volunteers
      }
      if (this.type === 'pwas') {
        return this.pwas
      }
      return []
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
    },
    volunteers: {
      query () {
        return gql`query getVolunteers {
          volunteers {
            id,
            general_info {
              name
            }
          }
        }`
      },
      update: data => data.volunteers.map((item) => {
        return { id: item.id, name: item.general_info.name }
      })
    },
    pwas: {
      query () {
        return gql`query getPWAs {
          pwas {
            id,
            general_info {
              name
            }
          }
        }`
      },
      update: data => data.pwas.map((item) => {
        return { id: item.id, name: item.general_info.name }
      })
    }
  }
}
</script>
