<template>
  <v-dialog
    v-model="isOpen"
    width="800"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        icon
        v-bind="attrs"
        v-on="on"
      >
        <v-icon>
          mdi-pencil
        </v-icon>
      </v-btn>
    </template>
    <StaffForm />
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
