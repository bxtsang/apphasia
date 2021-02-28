<template>
  <ApolloQuery
    :query="require('./../../../graphql/event/GetSingleEvent.graphql')"
    :variables="{ event_id: eventId }"
  >
    <template v-slot="{ result: { error, data }, isLoading }">
      <div v-if="isLoading" class="d-flex justify-center">
        <v-progress-circular
          :size="50"
          color="primary"
          indeterminate
        />
      </div>

      <!-- Error -->
      <div v-else-if="error">
        An error occurred
      </div>

      <div v-else-if="data && data.events_by_pk">
        <v-container class="pa-0 ma-0" style="width:800px">
          <v-row>
            <v-col class="d-flex align-center">
              <v-btn icon :to="`/projects?id=${data.events_by_pk.project_id}&tab=2`" @click="$emit('home')">
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
            </v-col>
            <v-col class="d-flex align-center justify-end">
              <EditResourceModal
                v-if="editPermission"
                :resourceType="resourceType"
                :resource="data.events_by_pk"
                :text="true"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <span class="section-title">Event Details</span>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="py-0">
              <v-text-field
                label="Event Name"
                :value="data.events_by_pk.name"
                readonly
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="py-0">
              <v-textarea
                :value="data.events_by_pk.note"
                label="Event Notes"
                readonly
                auto-grow
                rows="1"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" class="py-0">
              <v-text-field
                label="Start Date"
                :value="data.events_by_pk.date"
                readonly
              />
            </v-col>
            <v-col cols="6" class="py-0">
              <v-text-field
                label="End Date"
                :value="data.events_by_pk.recurring && data.events_by_pk.recurring.end_date ? data.events_by_pk.recurring.end_date : '-'"
                readonly
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" class="py-0">
              <v-text-field
                label="Start Time"
                :value="data.events_by_pk.start_time.slice(0, 5)"
                readonly
              />
            </v-col>
            <v-col cols="6" class="py-0">
              <v-text-field
                label="End Time"
                :value="data.events_by_pk.end_time.slice(0, 5)"
                readonly
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <span>Custom Recurrence</span>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" class="py-0">
              <v-select
                label="Repeat"
                :value="data.events_by_pk.recurring ? data.events_by_pk.recurring.frequency : 'None'"
                :items="[data.events_by_pk.recurring ? data.events_by_pk.recurring.frequency : 'None']"
                readonly
              />
            </v-col>
          </v-row>
          <v-row v-if="data.events_by_pk.recurring">
            <v-col cols="6" class="py-0">
              <v-select
                label="Every"
                :value="data.events_by_pk.recurring.interval"
                :items="[data.events_by_pk.recurring.interval]"
                readonly
              />
            </v-col>
          </v-row>
          <v-row v-if="data.events_by_pk.recurring">
            <v-col cols="6" class="py-0">
              <v-select
                label="On"
                :value="data.events_by_pk.recurring.day"
                :items="DAY"
                readonly
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <span>People Involved</span>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="py-0">
              <v-autocomplete
                label="Volunteers Involved"
                chips
                multiple
                :items="data.events_by_pk.volunteers"
                item-text="volunteer.general_info.name"
                item-value="volunteer.general_info.id"
                :value="data.events_by_pk.volunteers.map(item => item.volunteer.general_info.id)"
                readonly
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" class="py-0">
              <v-autocomplete
                label="PWAs Involved"
                chips
                multiple
                :items="data.events_by_pk.pwas"
                item-text="pwa.general_info.name"
                item-value="pwa.general_info.id"
                :value="data.events_by_pk.pwas.map(item => item.pwa.general_info.id)"
                readonly
              />
            </v-col>
          </v-row>
        </v-container>
      </div>
      <div v-else> Something Change</div>
    </template>
  </ApolloQuery>
</template>
<script>
import { DAY, EDIT_RESOURCE_PERMISSIONS } from './../../../assets/data'

export default {
  props: {
    resourceType: {
      type: String,
      default: null
    }
  },
  data () {
    return {
      EDIT_RESOURCE_PERMISSIONS,
      DAY,
      eventId: Number(this.$route.query.event)
    }
  },
  computed: {
    editPermission () {
      return this.EDIT_RESOURCE_PERMISSIONS[this.resourceType].includes(this.$auth.user['custom:role'])
    }
  }
}
</script>
