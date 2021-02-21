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
        <v-row>
          <v-col class="py-0">
            <v-row class="mt-3">
              <v-col cols="12" class="py-0">
                <span class="font-weight-bold">Event Details</span>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                Event Name
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                Event Notes
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                Start Date
              </v-col>
              <v-col class="py-0">
                End Date
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                Start Time
              </v-col>
              <v-col class="py-0">
                End Time
              </v-col>
            </v-row>
            <v-row class="mt-3">
              <v-col cols="12" class="py-0">
                <span class="font-weight-bold">Custom Recurrence</span>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                Repeat
              </v-col>
            </v-row>
            <v-row class="mt-3">
              <v-col cols="12" class="py-0">
                <span class="font-weight-bold">People Involved</span>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                Volunteer Involved
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                PWA Involved
              </v-col>
            </v-row>
            <v-row>
              <div class="my-3 ml-3">
                <DeleteResourceModal
                  v-if="$auth.user['custom:role'] === 'core_team' && event"
                  :resource="event"
                  :resourceType="'events'"
                  @deleteSuccess="$emit('closeForm')"
                />
              </div>
              <v-spacer/>
              <v-btn color="primary" class="my-3 mr-3" type="submit" :loading="isSubmitting">
                {{ event ? 'Edit' : 'Save' }}
              </v-btn>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
</template>
<script>
export default {
  props: {
    event: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      valid: true,
      isSubmitting: false
    }
  },
  computed: {
    formSubmitMethod () {
      if (this.event) {
        return this.editEvent
      } else {
        return this.submitEvent
      }
    }
  },
  methods: {
    submitEvent () {
      return ''
    },
    editEvent () {
      return ''
    }
  },
}
</script>
