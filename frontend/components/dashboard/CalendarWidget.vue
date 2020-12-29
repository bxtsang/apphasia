<template>
  <v-card class="px-6 py-3 mb-6">
    <v-toolbar flat>
      <v-btn
        fab
        text
        small
        color="grey darken-2"
        @click="prev"
      >
        <v-icon small>
          mdi-chevron-left
        </v-icon>
      </v-btn>
      <v-spacer></v-spacer>
      <v-toolbar-title v-if="$refs.calendar">
        {{ $refs.calendar.title }}
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        fab
        text
        small
        color="grey darken-2"
        @click="next"
      >
        <v-icon small>
          mdi-chevron-right
        </v-icon>
      </v-btn>
    </v-toolbar>
    <v-calendar
      ref="calendar"
      v-model="value"
      :weekdays="weekday"
      :type="type"
      :events="events"
      event-overlap-mode="stack"
      :event-overlap-threshold="30"
      :event-color="getEventColor"
      @change="getEvents"
    ></v-calendar>
  </v-card>
</template>
<script>
export default {
  data () {
    return {
      value: '',
      weekday: [0, 1, 2, 3, 4, 5, 6],
      type: 'month',
      events: [],
      colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
      names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party']
    }
  },
  mounted () {
    this.$refs.calendar.checkChange()
  },
  methods: {
    prev () {
      this.$refs.calendar.prev()
    },
    next () {
      this.$refs.calendar.next()
    },
    getEvents ({ start, end }) {
      const events = []

      const min = new Date(`${start.date}T00:00:00`)
      const max = new Date(`${end.date}T23:59:59`)
      const days = (max.getTime() - min.getTime()) / 86400000
      const eventCount = this.rnd(days, days + 20)

      for (let i = 0; i < eventCount; i++) {
        const allDay = this.rnd(0, 3) === 0
        const firstTimestamp = this.rnd(min.getTime(), max.getTime())
        const first = new Date(firstTimestamp - (firstTimestamp % 900000))
        const secondTimestamp = this.rnd(2, allDay ? 288 : 8) * 900000
        const second = new Date(first.getTime() + secondTimestamp)

        events.push({
          name: this.names[this.rnd(0, this.names.length - 1)],
          start: first,
          end: second,
          color: this.colors[this.rnd(0, this.colors.length - 1)],
          timed: !allDay
        })
      }

      this.events = events
    },
    getEventColor (event) {
      return event.color
    },
    rnd (a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    }
  }
}
</script>
