<template>
  <v-container class="pa-0 ma-0" style="width:800px">
    <v-row>
      <v-col class="d-flex align-center">
        <v-btn icon @click="$emit('home')">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
      </v-col>
      <v-col class="d-flex align-center justify-end">
        <v-btn color="primary">Edit</v-btn>
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
          :value="event.name"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="py-0">
        <v-textarea
          :value="event.note"
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
          :value="event.date"
        />
      </v-col>
      <v-col cols="6" class="py-0">
        <v-text-field
          label="End Date"
          :value="event.recurring && event.recurring.end_date ? event.recurring.end_date : '-'"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6" class="py-0">
        <v-text-field
          label="Start Time"
          :value="event.start_time.split('+')[0]"
        />
      </v-col>
      <v-col cols="6" class="py-0">
        <v-text-field
          label="End Time"
          :value="event.end_time.split('+')[0]"
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
          :value="event.recurring ? event.recurring.frequency : 'None'"
          :items="[event.recurring ? event.recurring.frequency : 'None']"
        />
      </v-col>
    </v-row>
    <v-row v-if="event.recurring">
      <v-col cols="6" class="py-0">
        <v-select
          label="Every"
          :value="event.recurring.interval"
          :items="[event.recurring.interval]"
        />
      </v-col>
    </v-row>
    <v-row v-if="event.recurring">
      <v-col cols="6" class="py-0">
        <v-select
          label="On"
          :value="DAY[event.recurring.day]"
          :items="[DAY[event.recurring.day]]"
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
          :items="event.volunteers"
          item-text="volunteer.general_info.name"
          item-value="volunteer.general_info.id"
          :value="event.volunteers.map(item => item.volunteer.general_info.id)"
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
          :items="event.pwas"
          item-text="pwa.general_info.name"
          item-value="pwa.general_info.id"
          :value="event.pwas.map(item => item.pwa.general_info.id)"
          readonly
        />
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import { DAY } from './../../../assets/data'

export default {
  props: {
    event: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      DAY
    }
  }
}
</script>
