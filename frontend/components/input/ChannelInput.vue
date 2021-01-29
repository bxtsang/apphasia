<template>
  <v-select
    v-model="data"
    :items="channels"
    :label="!placeholderOnly ? 'How did you hear about Aphasia SG?' : ''"
    :placeholder="placeholderOnly ? 'How did you hear about Aphasia SG?' : ''"
    :rules="validation"
    :required="required"
    :readonly="readonly"
  />
</template>

<script>
import gql from 'graphql-tag'
import { VOLUNTEER_CHANNELS } from './../../assets/data'
export default {
  name: 'ChannelInput',

  props: {
    value: {
      type: String,
      default: ''
    },
    required: {
      type: Boolean,
      default: false
    },
    readonly: {
      type: Boolean,
      default: false
    },
    placeholderOnly: {
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
    }
  },

  apollo: {
    channels: {
      query () {
        return gql`query getChannels {
          channels {
            channel
          }
        }`
      },
      update: data => data.channels.map((item) => {
        return { value: item.channel, text: VOLUNTEER_CHANNELS[item.channel].text }
      })
    }
  }
}

</script>
