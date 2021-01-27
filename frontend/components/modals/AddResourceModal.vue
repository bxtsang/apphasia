<template>
  <v-dialog
    v-model="isOpen"
    width="800"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" v-bind="attrs" v-on="on">
        Add {{ resource }}
      </v-btn>
    </template>
    <StaffForm v-if="resourceType === 'staffs'" v-on:closeForm="isOpen = false" />
  </v-dialog>
</template>
<script>
import StaffForm from './../staff/StaffForm'

export default {
  components: { StaffForm },
  props: {
    text: Boolean,
    resourceType: {
      type: String,
      default: null
    }
  },
  data () {
    return {
      isOpen: false
    }
  },
  computed: {
    resource () {
      if (this.resourceType === 'staffs') {
        return 'Staff'
      }
      return 'Resource'
    }
  }
}
</script>
