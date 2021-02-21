<template>
  <v-card class="pa-8">
    <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="formSubmitMethod">
      <v-container class="pa-0">
        <v-row>
          <v-col class="py-0">
            <span v-if="event" class="section-title">Edit Event</span>
            <span v-else class="section-title">Add Event</span>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
</template>
<script>
export default {
  props: {
    project: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      valid: true,
      isSubmitting: false
    }
  }
}
</script>
