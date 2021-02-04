<template>
  <v-chip :color="color">{{ value }}</v-chip>
</template>
<script>
import { VOLUNTEER_STATUS } from './../../../assets/data'

export default {
  props: {
    value: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      VOLUNTEER_STATUS
    }
  },
  computed: {
    color () {
      return VOLUNTEER_STATUS[this.value].chipColor
    }
  }
}
</script>
