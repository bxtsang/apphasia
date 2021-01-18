<template>
  <v-dialog
    v-model="isOpen"
    width="800"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        v-if="text"
        color="primary"
        v-bind="attrs"
        v-on="on"
      >
        <v-icon left>
          mdi-pencil
        </v-icon>
        Edit
      </v-btn>
      <v-btn
        v-else
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
  props: { text: Boolean, staff: Object },
  data () {
    return {
      isOpen: false
    }
  }
}
</script>
