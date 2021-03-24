<template>
  <ApolloQuery
    :query="require('./../../graphql/notifications/GetNotificationOfStaffInitial.graphql')"
    :variables="{
      staff: $auth.user['custom:hasura_id']
    }"
    >
    <template v-slot="{ result: { error, data }, isLoading }">
      <!-- Loading -->
      <div v-if="isLoading" class="d-flex justify-center">
        <v-progress-circular
          :size="50"
          color="primary"
          indeterminate
          class="ma-6"
        />
      </div>

      <!-- Error -->
      <div v-else-if="error">An error occurred</div>
      <div v-else-if="data">
        {{ data.notifications[0]}}
        <v-list>
          <NotificationItem v-for="item in data.notifications" :notification="item" v-bind:key="item.id" />
        </v-list>
      </div>
    </template>
  </ApolloQuery>
</template>
<script>

export default {
  data () {
    return {
    }
  }
}
</script>
