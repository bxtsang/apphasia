<template>
  <v-select
    v-model="data"
    :label="label"
    :items="vol_voltypes"
    :readonly="readonly"
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
          vol_voltypes {
            voltype
          }
        }`
      },
      update: data => data.vol_voltypes.map((item) => {
        return { value: item.voltype, text: VOLUNTEER_TYPES[item.voltype] }
      })
    }
  }
}
</script>
