<template>
  <v-select
    v-model="data"
    :label="label"
    :items="vol_voltypes"
    :readonly="readonly"
    hint="Select the type of volunteers that can be qualified for this project (e.g. befrienders: only befrienders can volunteer)"
    persistent-hint
  />
</template>
<script>
import gql from 'graphql-tag'
import { VOLUNTEER_TYPES } from './../../../assets/data'

export default {
  data () {
    return {
      data: this.value
    }
  },
  props: {
    value: {
      type: String,
      default: ''
    },
    label: {
      type: String,
      default: 'Project Volunteer Types'
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
    vol_voltypes: {
      query () {
        return gql`query getVolTypes{
          voltypes {
            type
          }
        }`
      },
      update: data => data.voltypes.map((item) => {
        return { value: item.type, text: VOLUNTEER_TYPES[item.type] }
      })
    }
  }
}
</script>
