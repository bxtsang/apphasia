<template>
  <v-card class="pl-6 py-3 mb-6" ref="timelineWidget">
    <h1 class="title">Upcoming Events</h1>
    <ApolloQuery
      :query="LIST_QUERY_PATHS[resourceType]"
      :variables="{
        fromDate: $moment().format('YYYY-MM-DD'),
        endDate: $moment().add(31, 'days').format('YYYY-MM-DD')
      }"
    >
      <template v-slot="{ result: { error, data }, isLoading }">
        <!-- Loading -->
        <div v-if="isLoading" class="d-flex justify-center">
          <v-progress-circular
            :size="50"
            color="primary"
            indeterminate
          />
        </div>

        <!-- Error -->
      <div v-else-if="error">An error occurred</div>

      <!-- Result -->
      <div v-else-if="data" class="timeline-wrapper pr-6">
        <v-timeline :dense="componentWidth < 675">
          <v-timeline-item
            v-for="event in data.events"
            :key="event.id"
            :color="event.project.colour"
            fill-dot
            small
          >
            <h2 slot="opposite" :class="`${event.project.colour}--text`">{{ $moment(event.date).format('DD MMM YYYY') }}</h2>
            <v-card class="elevation-2 item" :color="event.project.colour" dark>
              <v-card-title class="title">
                {{ event.project.title }}
              </v-card-title>
              <v-card-text class="white text--primary">
                <span class="caption pt-1 d-block grey--text font-weight-bold">
                  {{ $moment(`${event.date}T${event.start_time.slice(0,8)}`).format('LT') }} - {{ $moment(`${event.date}T${event.end_time.slice(0,8)}`).format('LT') }}
                </span>
                {{ event.note }}
              </v-card-text>
            </v-card>
          </v-timeline-item>
        </v-timeline>
      </div>
      </template>
    </ApolloQuery>
  </v-card>
</template>
<script>
import { LIST_QUERY_PATHS } from './../../assets/data.js'

export default {
  data () {
    return {
      LIST_QUERY_PATHS,
      resourceType: 'timeline',
      componentWidth: 0
    }
  },
  mounted () {
    this.componentWidth = this.$refs.timelineWidget.$refs.link.clientWidth
    addEventListener('resize', () => {
      if (this.$refs) {
        this.componentWidth = this.$refs.timelineWidget.$refs.link.clientWidth
      }
    })
  }
}
</script>
<style scoped>
.timeline-wrapper{
  max-height: 50vh;
  overflow-y: auto;
}
.v-timeline-item__body > .item::before, .v-timeline-item__body > .item::after {
  display: none !important;
}
</style>
