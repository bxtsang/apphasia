<template>
  <v-row>
    <v-col>
      <v-card class="px-6 py-3">
        <ApolloQuery
          :query="require('./../../graphql/volunteer/GetSingleVol.graphql')"
          :variables="{ id: volunteerId }"
        >
          <template v-slot="{ result: { error, data }, isLoading }">
            <div v-if="isLoading" class="d-flex justify-center">
              <v-progress-circular
                :size="50"
                color = "primary"
                indeterminate
              />
            </div>

            <!-- Error -->
            <div v-else-if="error">
              An error occurred
            </div>

            <!-- Display on success -->
            <div v-else-if="data && data.volunteers.length > 0">
              <v-container class="pa-0 ma-0">
                <v-row>
                  <v-col>
                    <h1 class="title hover-underline">
                      <NuxtLink to="/volunteers">
                        Volunteers
                      </NuxtLink>
                      <span>/ {{ data.volunteers[0].name }}</span>
                    </h1>
                  </v-col>
                </v-row>
              </v-container>
            </div>
          </template>
        </ApolloQuery>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  props: {
    resourceType: {
      type: String,
      default: null
    }
  },
  data () {
    return {
      volunteerId: Number(this.$route.query.id)
    }
  }
}
</script>
