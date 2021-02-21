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
          label="End Data"
          :value="event.date"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6" class="py-0">
        <v-text-field
          label="Start Time"
          :value="event.date"
        />
      </v-col>
      <v-col cols="6" class="py-0">
        <v-text-field
          label="End Time"
          :value="event.date"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <span>Custom Recurrence</span>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <span>People Involved</span>
      </v-col>
    </v-row>
    {{ event }}
  </v-container>
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
    return {}
  }
}
</script>
