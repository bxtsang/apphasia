<template>
  <v-card class="pl-6 py-3 mb-6">
    <h1 class="title">Upcoming Events</h1>
      <div class="timeline-wrapper pr-6">
        <v-timeline :dense="$vuetify.breakpoint.smAndDown">
          <v-timeline-item
            v-for="event in events"
            :key="event.id"
            fill-dot
            small
          >
            <h2 slot="opposite" class="red200--text">{{ event.date }}</h2>
            <v-card class="elevation-2 item" color="primary" dark>
              <v-card-title class="title">
                {{ event.project.title }}
              </v-card-title>
              <v-card-text class="white text--primary">
                <span class="caption">{{ event.start_time }} - {{ event.end_time }}</span><br>
                {{ event.note }}
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
      </div>
  </v-card>
</template>
<script>
import gql from 'graphql-tag'

export default {
  data () {
    return {}
  },
  apollo: {
    events: {
      query () {
        return gql`query getUpcomingEvents{
          events (
            order_by: {date: asc},
            where: {
              _and: [
                { date: {_gte: "2021-05-01"} },
                { date: {_lte: "2021-05-30"} }
              ]
            }
          ) {
            id
            date
            project {
              title
            }
            note
            start_time
            end_time
          }
        }`
      }
    }
  }
}
</script>
<style scoped>
.timeline-wrapper{
  max-height: 550px;
  overflow-y: auto;
}
.v-timeline-item__body > .item::before, .v-timeline-item__body > .item::after {
  display: none !important;
}
</style>
