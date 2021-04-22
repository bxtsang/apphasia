<template>
  <v-autocomplete
    v-model="data"
    :label="label"
    :items="items"
    chips
    item-text="name"
    item-value="id"
    multiple
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
    type: {
      type: String,
      default: ''
    },
    projectId: {
      type: String,
      default: null
    }
  },

  computed: {
    items () {
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
    volunteers: {
      query () {
        return gql`query getProjectVols($id: Int!){
          projects_by_pk(id: $id) {
            id
            volunteers {
              volunteer {
                general_info {
                  id
                  name
                }
              }
            }
          }
        }`
      },
      variables () { return { id: this.projectId } },
      update: data => data.projects_by_pk.volunteers.map((item) => {
        return { id: item.volunteer.general_info.id, name: item.volunteer.general_info.name }
      })
    },
    pwas: {
      query () {
        return gql`query getProjectPWAs($id: Int!) {
          projects_by_pk(id: $id) {
            id
            pwas {
              pwa {
                general_info {
                  id
                  name
                }
              }
            }
          }
        }`
      },
      variables () { return { id: this.projectId } },
      update: data => data.projects_by_pk.pwas.map((item) => {
        return { id: item.pwa.general_info.id, name: item.pwa.general_info.name }
      })
    }
  }
}
</script>
