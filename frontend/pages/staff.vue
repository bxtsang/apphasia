<template>
  <div>
    <!-- <IndividualStaffView v-if="projectId" /> -->
    <!-- <v-container v-else class="pa-0" fluid> -->
    <v-container class="pa-0" fluid>
      <v-row>
        <v-col>
          <!-- <NewStaffModal /> -->
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card class="px-6 py-3">
            <h1 class="title">Manage Staff</h1>
            <v-row>
              <v-col>
                <ApolloQuery
                  :query="require('./../graphql/staff/Test.gql')"
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
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>
<script>
// import gql from 'graphql-tag'

export default {
  data () {
    return {
      staffId: this.$route.query.id,
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
  },
  watch: {
    '$route.query.id': {
      handler () {
        this.projectId = this.$route.query.id
      }
    }
  }
}
</script>
