<template>
  <ApolloQuery
    :query = "query"
    :variables="{
      'isCoreTeam': $auth.user['custom:role'] === 'core_team'
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
      <div v-else-if="data">
        <v-data-table
          :headers="TABLE_HEADERS[resourceType]"
          :items="filterItems(data[resourceType])"
          :search="search"
          item-key="id"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-container class="py-0" fluid>
              <v-row>
                <v-col>
                  <h1 class="title pt-3 px-3">Manage Staff</h1>
                </v-col>
              </v-row>
              <v-row v-if="resourceType === 'staffs'">
                <v-col>
                  <v-tabs>
                    <v-tab
                      v-for="role in ROLE_OPTIONS"
                      :key="role.value"
                      @click="staffRoleFilter = role.value"
                    >
                      {{ role.label}}
                    </v-tab>
                  </v-tabs>
                </v-col>
              </v-row>
              <v-row>
                <v-text-field
                  v-model="search"
                  label="Search"
                  append-icon="mdi-magnify"
                  solo
                  dense
                  class="mx-3"
                />
              </v-row>
            </v-container>
          </template>
          <template v-if="resourceType === 'staffs'" v-slot:[`item.is_speech_therapist`]="{ item }">
            <v-chip v-if="item.is_speech_therapist" color="success">Yes</v-chip>
            <v-chip v-else color="error">No</v-chip>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <EditResourceModal v-if="$auth.user['custom:role'] === 'core_team'" :resourceType="resourceType" :resource="item" :text="false" />
            <v-btn :to="`/${resourceType}?id=${item.id}`" icon>
              <v-icon large>
                mdi-chevron-right
              </v-icon>
            </v-btn>
          </template>
        </v-data-table>
      </div>

    </template>
  </ApolloQuery>
</template>

<script>
import { LIST_QUERY_PATHS, TABLE_HEADERS, ROLE_OPTIONS } from '../../assets/data'
import EditResourceModal from '~/components/modals/EditResourceModal'

export default {
  components: { EditResourceModal },
  props: {
    resourceType: {
      type: String,
      default: null
    }
  },

  data () {
    return {
      LIST_QUERY_PATHS,
      TABLE_HEADERS,
      ROLE_OPTIONS,
      staffRoleFilter: 'core_team',
      search: ''
    }
  },

  computed: {
    query () {
      return LIST_QUERY_PATHS[this.resourceType]
    }
  },

  methods: {
    filterItems (data) {
      if (this.resourceType === 'staffs') {
        return data.filter(item => item.role === this.staffRoleFilter && item.is_active)
      } else {
        return data
      }
    }
  }
}
</script>

<style scoped>

</style>
