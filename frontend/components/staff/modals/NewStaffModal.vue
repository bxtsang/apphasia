<template>
  <v-dialog
    v-model="isOpen"
    width="800"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" v-bind="attrs" v-on="on">
        Add Staff
      </v-btn>
    </template>
    <StaffForm v-on:closeForm="isOpen = false" />
  </v-dialog>
</template>
<script>
import StaffForm from './../StaffForm'

export default {
  components: { StaffForm },
  data () {
    return {
      isOpen: false
    }
  }
}
</script>
