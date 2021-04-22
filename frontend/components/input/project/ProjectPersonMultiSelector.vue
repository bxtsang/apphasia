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
      searchInput: ''
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
    },
    voltype: {
      type: String,
      default: null
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
        return gql`query GetVolsByType($voltype: voltypes_enum){
          volunteers(where: {
            vol_voltypes: {
              voltype: {_eq: $voltype}
            }
          }) {
            id
            general_info {
              name
            }
          }
        }`
      },
      variables () { return { voltype: this.voltype } },
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
