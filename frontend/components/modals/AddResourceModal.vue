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
    <StaffForm v-if="resourceType === 'staffs'" @closeForm="isOpen = false" />
    <PWAForm v-if="resourceType === 'pwas'" @closeForm="isOpen = false" />
  </v-dialog>
</template>
<script>
import StaffForm from './../staff/StaffForm'
import PWAForm from './../pwa/PWAForm'

export default {
  components: { StaffForm, PWAForm },
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
      if (this.resourceType === 'pwas') {
        return 'PWA'
      }
      return 'Resource'
    }
  }
}
</script>
