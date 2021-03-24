<template>
  <ApolloQuery
    :query="LIST_QUERY_PATHS['notification']['read']"
    :variables="{
      staff: $auth.user['custom:hasura_id']
    }"
    >
     <ApolloSubscribeToMore
      :document="LIST_QUERY_PATHS['notification']['readSubscription']"
      :variables="{ staff: $auth.user['custom:hasura_id'] }"
    />
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
        <v-list>
          <NotificationItem v-for="item in data.notifications" :notification="item" v-bind:key="item.id" />
        </v-list>
      </div>
    </template>
  </ApolloQuery>
</template>
<script>
import { LIST_QUERY_PATHS } from './../../assets/data.js'
export default {
  data () {
    return {
      LIST_QUERY_PATHS
    }
  }
}
</script>
