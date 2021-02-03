<template>
  <v-chip :color="color">{{ value }}</v-chip>
</template>
<script>
import { CONTACT_STATUS } from './../../../assets/data'

export default {
  props: {
    value: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      CONTACT_STATUS
    }
  },
  computed: {
    color () {
      return CONTACT_STATUS[this.value].chipColor
    }
  }
}
</script>
