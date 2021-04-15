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
                <EventNameInput
                  v-model="eventData.name"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                <EventNotesInput
                  v-model="eventData.note"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                <DateInput
                  label="Start Date"
                  v-model="eventData.start_date"
                  required
                />
              </v-col>
              <v-col class="py-0">
                <DateInput
                  label="End Date"
                  v-model="eventData.recurringData.end_date"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                <TimePickerInput
                  v-model="eventData.start_time"
                  label="Start Time"
                  required />
              </v-col>
              <v-col class="py-0">
                <TimePickerInput
                  v-model="eventData.end_time"
                  label="End Time"
                  required />
              </v-col>
            </v-row>
            <v-row class="mt-3">
              <v-col cols="12" class="py-0">
                <span class="font-weight-bold">Custom Recurrence</span>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0" cols="6">
                <FrequencyInput
                  v-model="eventData.recurringData.frequency"
                  label="Repeat"
                  required
                />
              </v-col>
            </v-row>
            <v-row v-if="eventData.recurringData.frequency !== 'None'">
              <v-col class="py-0" cols="6">
                <IntervalInput
                  v-model="eventData.recurringData.interval"
                  label="Every"
                  :type="eventData.recurringData.frequency"
                  required
                />
              </v-col>
            </v-row>
            <v-row v-if="eventData.recurringData.frequency == 'Monthly'">
              <v-col class="py-0" cols="6">
                <WeekInput
                  v-model="eventData.recurringData.week"
                  label="On"
                  required
                />
              </v-col>
            </v-row>
            <v-row v-if="eventData.recurringData.frequency !== 'None'">
              <v-col class="py-0" cols="6">
                <DayInput
                  v-model="eventData.recurringData.day"
                  label="On"
                  required
                />
              </v-col>
            </v-row>
            <v-row class="mt-3">
              <v-col cols="12" class="py-0">
                <span class="font-weight-bold">People Involved</span>
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                <EventPersonMultiSelector
                  v-model="eventData.volunteers.data"
                  label="Volunteers Involved"
                  type="volunteers"
                  :projectId="eventData.project_id"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col class="py-0">
                <EventPersonMultiSelector
                  v-model="eventData.pwas.data"
                  label="PWAs Involved"
                  type="pwas"
                  :projectId="eventData.project_id"
                />
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
              <EditConfirmation v-if="event" :event="event" :newEventData="eventData" @editEvent="editEvent" :loading="isSubmitting"/>
              <v-btn v-else color="primary" class="my-3 mr-3" type="submit" :loading="isSubmitting">
                Add
              </v-btn>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
</template>
<script>
import InsertEventOrRecurring from './../../../graphql/event/InsertEventOrRecurring.graphql'
import UpdateEventOrRecurring from './../../../graphql/event/UpdateEventOrRecurring.graphql'

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
      isSubmitting: false,
      eventData: {
        project_id: this.$route.query.id,
        name: this.event ? this.event.name : '',
        note: this.event ? this.event.note : '',
        start_date: this.event ? this.event.date : '',
        start_time: this.event ? this.event.start_time.slice(0, 5) : '',
        end_time: this.event ? this.event.end_time.slice(0, 5) : '',
        recurringData: {
          end_date: this.event && this.event.recurring ? this.event.recurring.end_date : '',
          frequency: this.event && this.event.recurring ? this.event.recurring.frequency : 'None',
          interval: this.event && this.event.recurring ? this.event.recurring.interval : -1,
          week: this.event && this.event.recurring ? this.event.recurring.week : -1,
          day: this.event && this.event.recurring ? this.event.recurring.day : -1
        },
        volunteers: {
          data: this.event ? (this.event.recurring ? this.event.recurring.volunteers.map(item => item.volunteer.general_info.id) : this.event.volunteers.map(item => item.volunteer.general_info.id)) : []
        },
        pwas: {
          data: this.event ? (this.event.recurring ? this.event.recurring.pwas.map(item => item.pwa.general_info.id) : this.event.pwas.map(item => item.pwa.general_info.id)) : []
        }
      }
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
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        const _ = require('lodash')
        const newEventData = _.cloneDeep(this.eventData)
        newEventData.pwas.data = newEventData.pwas.data.map((item) => { return { pwa_id: item } })
        newEventData.volunteers.data = newEventData.volunteers.data.map((item) => { return { vol_id: item } })
        this.$apollo.mutate({
          mutation: InsertEventOrRecurring,
          variables: { newEventData },
          update: (store, data) => {
            setTimeout(this.$apollo.vm.$apolloProvider.defaultClient.resetStore, 2000)
          }
        }).then((data) => {
          this.isSubmitting = false
          this.eventData = {
            project_id: this.$route.query.id,
            name: '',
            note: '',
            start_date: '',
            start_time: '',
            end_time: '',
            recurringData: {
              end_date: '',
              frequency: 'None',
              interval: -1,
              week: -1,
              day: -1
            },
            volunteers: { data: [] },
            pwas: { data: [] }
          }
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['Event successfully created', 'success'])
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    editEvent (eventOption) {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        const _ = require('lodash')
        const updatedEventData = _.cloneDeep(this.eventData)
        updatedEventData.id = this.event.id
        updatedEventData.project_id = this.event.project_id
        updatedEventData.date = updatedEventData.start_date
        delete updatedEventData.start_date
        updatedEventData.pwas.data = this.eventData.pwas.data.map((item) => { return { pwa_id: item } })
        updatedEventData.volunteers.data = this.eventData.volunteers.data.map((item) => { return { vol_id: item } })
        updatedEventData.recurringData.id = this.event.recurring ? this.event.recurring.id : null
        updatedEventData.recurringData.name = updatedEventData.name
        updatedEventData.recurringData.note = updatedEventData.note
        updatedEventData.recurringData.start_date = updatedEventData.date
        updatedEventData.recurringData.start_time = updatedEventData.start_time
        updatedEventData.recurringData.end_time = updatedEventData.end_time
        updatedEventData.recurringData.is_all = eventOption

        updatedEventData.recurringData.pwas = this.eventData.pwas.data
        updatedEventData.recurringData.volunteers = this.eventData.volunteers.data

        console.log(JSON.stringify(updatedEventData))
        this.$apollo.mutate({
          mutation: UpdateEventOrRecurring,
          variables: { updateEventData: updatedEventData },
          update: (store, data) => {
            setTimeout(this.$apollo.vm.$apolloProvider.defaultClient.resetStore, 2000)
          }
        }).then((data) => {
          this.isSubmitting = false
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['Event successfully Updated', 'success'])
          this.$router.push(`/projects?id=${this.event.project_id}&tab=2`)
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    }
  }
}
</script>
