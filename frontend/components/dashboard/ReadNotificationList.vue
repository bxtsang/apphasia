<template>
  <ApolloQuery
    :query="LIST_QUERY_PATHS['notification']['read']"
    :variables="{
      staff: $auth.user['custom:hasura_id'],
      limit: $options.fetchLimit,
      offset: 0
    }"
    >
    <template v-slot="{ result: { error, data , loading}, isLoading, query }">
      <!-- Loading -->
      <div v-if="loading" class="d-flex justify-center">
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
          <NotificationItem v-for="item in data.notifications" :notification="item" v-bind:key="item.id" :query="query"/>
          <v-list-item v-if="data.notifications.length < data.notifications_aggregate.aggregate.totalCount" class="d-flex justify-center">
            <v-btn @click="fetchMore(query)" :loading="isLoading === 1" color="primary">Load more</v-btn>
          </v-list-item>
          <v-list-item v-if="data.notifications && data.notifications.length === 0" class="d-flex justify-center">
            No notifications
          </v-list-item>
        </v-list>
      </div>

    </template>
  </ApolloQuery>
</template>
<script>
import { LIST_QUERY_PATHS } from './../../assets/data.js'
export default {
  fetchLimit: 5,
  data () {
    return {
      LIST_QUERY_PATHS,
      offset: 0
    }
  },
  methods: {
    async fetchMore (query) {
      this.offset += this.$options.fetchLimit
      await query.fetchMore({
        variables: {
          staff: this.$auth.user['custom:hasura_id'],
          limit: this.$options.fetchLimit,
          offset: this.offset
        },
        updateQuery: (prev, { fetchMoreResult }) => {
          console.log(prev)
          console.log(fetchMoreResult)
          return Object.assign({}, prev, {
            notifications: [...prev.notifications, ...fetchMoreResult.notifications],
            notifications_aggregate: fetchMoreResult.notifications_aggregate
          })
        }
      })
    }
  }
}
</script>
