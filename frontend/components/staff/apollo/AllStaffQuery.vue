<template>
  <ApolloQuery
    :query="require('./../../../graphql/staff/Test.gql')"
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
      <div v-else-if="data">
        <v-text-field
          v-model="search"
          label="Search"
          append-icon="mdi-magnify"
          filled
          rounded
        ></v-text-field>
        <v-data-table
          :headers="getHeaders"
          :items="testData"
          item-key="id"
          class="elevation-1"
          :search="search"
          :custom-filter="filterOnlyCapsText"
        >
          <template v-slot:top>
            <v-container fluid>
              <v-row>
                <v-col>
                  <v-tabs>
                    <v-tab>Core Team</v-tab>
                    <v-tab>Interns</v-tab>
                    <v-tab>Core Volunteers</v-tab>
                  </v-tabs>
                </v-col>
              </v-row>
            </v-container>
          </template>
        </v-data-table>
      </div>

      <!-- No result -->
      <div v-else>No result :(</div>
    </template>
  </ApolloQuery>
</template>
<script>
export default {
  data () {
    return {
      staffTypeFilter: null,
      testData: [
        {
          name: 'Person 1',
          id: 1
        }
      ]
    }
  },
  computed: {
    getHeaders () {
      return [
        { text: 'Id', value: 'id' },
        { text: 'Name', value: 'name' }
      ]
    }
  }
}
</script>
<style scoped>

</style>
