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
                  <!-- add edit modal -->
                </v-row>
                <v-row>
                  <v-col cols="12" class="py-0">
                    <span>Status</span>
                  </v-col>
                </v-row>
                <v-row class="mt-2">
                  <v-col cols="2" class="py-0">
                    <VolunteerStatusChip :value="data.volunteers[0].status"/>
                  </v-col>
                  <v-col class="py-0 mt-1" v-if="data.volunteers[0].rejection_reason">
                    <span>Reason for rejection: </span>
                    <span>{{ data.volunteers[0].rejection_reason }}</span>
                  </v-col>
                </v-row>
                <v-row class="mt-4">
                  <v-col cols="12" class="py-0">
                    <span>Personal Details</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers[0].name"
                      label="Full Name"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers[0].nickname"
                      label="Nickname / Alias"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers[0].dob"
                      label="Date of Birth"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers[0].contact_num"
                      label="Contact"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-select
                      :value="data.volunteers[0].gender"
                      :items="GENDER_OPTIONS"
                      label="Gender"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0" cols="4">
                    <v-text-field
                      :value="data.volunteers[0].email"
                      label="Email Address"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0" cols="8">
                    <v-text-field
                      :value="data.volunteers[0].address || 'Not Available'"
                      label="Home Address"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row class="mt-3">
                  <v-col cols="12" class="py-0">
                    <span>Additional Information</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-select
                      :value="data.volunteers[0].project_vols.map(item => item.project.title)"
                      :items="data.volunteers[0].project_vols.map(item => item.project.title)"
                      label="Projects Interested"
                      multiple
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-select
                      :value="data.volunteers[0].project_vols.filter(item => item.approved).map(item => item.project.title)"
                      :items="data.volunteers[0].project_vols.filter(item => item.approved).map(item => item.project.title)"
                      label="Projects Involved"
                      multiple
                      readonly
                    />
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
import { GENDER_OPTIONS } from './../../assets/data'
import VolunteerStatusChip from './../common/components/VolunteerStatusChip'

export default {
  components: { VolunteerStatusChip },
  props: {
    resourceType: {
      type: String,
      default: null
    }
  },
  data () {
    return {
      volunteerId: Number(this.$route.query.id),
      GENDER_OPTIONS
    }
  }
}
</script>
