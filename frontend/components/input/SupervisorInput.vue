<template>
  <v-select
    v-model="data"
    :items="supervisors"
    label="Tag Supervisor(s)"
    :required="required"
    :readonly="readonly"
    multiple
  />
</template>

<script>
import gql from 'graphql-tag'

export default {
  name: 'SupervisorInput',

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
    supervisors: {
      query () {
        return gql`query getCoreTeamMembers {
          staffs(where: {role: {_eq: core_team}}){
            id
            name
          }
        }`
      },
      update: data => data.staffs.map((item) => { return { text: item.name, value: item.id } })
    }
  }
}

</script>
