<template>
  <div>
    <h1 class="title mb-3">
      Settings
    </h1>
    <v-card>
      <div class="d-flex">
        <div>
          <v-navigation-drawer permanent>
            <v-list class="pa-0" nav dense>
              <v-list-item
                v-for="(item, index) in items"
                :key="index"
                color="primary"
                :input-value="index == active"
                link
                class="py-2 px-6"
                @click="active = index"
              >
                <v-list-item-icon>
                  <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-navigation-drawer>
        </div>
        <div v-if="active === 0" class="px-8 py-6" style="width:100%;max-width:800px;">
          <h1 class="title mb-3">
            Edit Profile
          </h1>
          <ApolloQuery
            :query="require('./../graphql/staff/GetSingleStaff.graphql')"
            :variables="{
              'isCoreTeam': true,
              'id': $auth.user['custom:hasura_id']
            }"
          >
            <template v-slot="{ result: { error, data }, isLoading }">
              <div v-if="isLoading" class="d-flex justify-center">
                <v-progress-circular
                  :size="50"
                  color="primary"
                  indeterminate
                />
              </div>
              <div v-if="error" class="d-flex justify-center">
                Unable to Retrieve User Data
              </div>
              <EditProfile v-if="data" :profile="data.staffs[0]" />
            </template>
          </ApolloQuery>
        </div>
        <div v-else-if="active === 1" class="px-8 py-6" style="width:100%;max-width:500px;">
          <h1 class="title mb-3">
            Change Password
          </h1>
          <ChangePassword />
        </div>
      </div>
    </v-card>
  </div>
</template>
<script>
import EditProfile from './../components/settings/EditProfile'
import ChangePassword from './../components/settings/ChangePassword'

export default {
  components: { EditProfile, ChangePassword },
  data () {
    return {
      active: 0,
      items: [
        {
          icon: 'mdi-pencil',
          title: 'Edit Profile'
        },
        {
          icon: 'mdi-shield-check',
          title: 'Change Password'
        }
      ]
    }
  }
}
</script>
