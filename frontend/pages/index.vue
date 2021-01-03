<template>
  <div>
    <v-row>
      <v-col cols="7">
        <TimelineWidget></TimelineWidget>
        <TaskList></TaskList>
      </v-col>
      <v-col>
        <CalendarWidget></CalendarWidget>
        <NotificationList></NotificationList>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import TimelineWidget from './../components/dashboard/TimelineWidget'
import CalendarWidget from './../components/dashboard/CalendarWidget'
import TaskList from './../components/dashboard/TaskList'
import NotificationList from './../components/dashboard/NotificationList'

export default {
  components: { TimelineWidget, CalendarWidget, TaskList, NotificationList },
  data () {
    return {
      loading: false
    }
  }
}
</script>
