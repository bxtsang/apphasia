<template>
  <v-dialog
    v-model="isOpen"
    width="500"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        color="primary"
        class="my-3 mr-3"
        v-bind="attrs"
        v-on="on"
      >
        Edit
      </v-btn>
    </template>
    <v-card>
      <v-form ref="form" v-model="valid" @submit.prevent="triggerEdit">
      <v-card-title class="headline">
        Confirm changes?
      </v-card-title>
      <v-divider />
      <div class="mt-4 pa-3">
        Editing Event: <span class="font-weight-bold">{{ event.name }}</span>
        <div class="mt-4">
          <span v-if="event.recurring === null && newEventData.recurringData.frequency !== 'None'">Converting to a recurring event</span>
          <span v-else-if="event.recurring !== null && newEventData.recurringData.frequency === 'None'">Converting to a single event</span>
          <v-radio-group v-else-if="event.recurring !== null" v-model="eventOption" class="mt-0">
            <v-radio
              v-for="option in EDIT_OPTIONS"
              :key="option.value"
              :label="option.text"
              :value="option.value"
            />
          </v-radio-group>
        </div>
      </div>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="primary"
          :loading="isLoading"
          type="submit"
        >
          Confirm
        </v-btn>
      </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>

export default {
  props: {
    event: {
      type: Object,
      default: null
    },
    newEventData: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      isOpen: false,
      isLoading: false,
      eventOption: 0,
      valid: true,
      EDIT_OPTIONS: [
        { text: 'This event', value: 0 },
        { text: 'This and future recurring events', value: 1 },
        { text: 'All recurring events', value: 2 }
      ]
    }
  },
  methods: {
    triggerEdit () {
      if (this.$refs.form.validate()) {
        this.isOpen = false
        this.$emit('editEvent', this.eventOption)
      }
    }
  }
}
</script>
