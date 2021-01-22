<template>
  <v-row>
    <v-col>
      <v-card class="px-6 py-3">
        <ApolloQuery
          :query="require('./../../graphql/staff/GetSingleStaff.graphql')"
          :variables="{ id: staffId }"
        >
          <template v-slot="{ result: { error, data }, isLoading }">
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
            <div v-else-if="data && data.staffs.length > 0">
              <v-container class="pa-0 ma-0">
                <v-row>
                  <v-col>
                    <h1 class="title hover-underline">
                      <NuxtLink to="/staff">Staff</NuxtLink>
                      <span>/ {{ data.staffs[0].name }}</span>
                    </h1>
                  </v-col>
                  <v-col class="d-flex justify-end">
                    <EditStaffModal :staff="data.staffs[0]" :text="true" />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col col="12" class="py-0">
                    <span>Role</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-radio-group v-model="data.staffs[0].role" readonly row>
                      <v-radio v-for="role in ROLE_OPTIONS.filter(item => item.value == data.staffs[0].role)" :key="role.value" :label="role.label" :value="role.value" />
                    </v-radio-group>
                  </v-col>
                </v-row>
                <v-row class="mt-3">
                  <v-col col="12" class="py-0">
                    <span>Personal Details</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      v-model="data.staffs[0].name"
                      label="Full Name"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      v-model="data.staffs[0].nickname"
                      label="Nickname / Alias"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      v-model="data.staffs[0].nric"
                      label="NRIC"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      v-model="data.staffs[0].dob"
                      label="Date of Birth"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      v-model="data.staffs[0].contact_num"
                      label="Contact"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-select
                      v-model="data.staffs[0].gender"
                      :items="GENDER_OPTIONS"
                      label="Gender"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0" cols="4">
                    <v-text-field
                      v-model="data.staffs[0].email"
                      label="Email Address"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0" cols="8">
                    <v-text-field
                      v-model="data.staffs[0].address"
                      label="Home Address"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row class="mt-3">
                  <v-col col="12" class="py-0">
                    <span>Additional Information</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      v-model="data.staffs[0].bio"
                      label="Hobbies / Interests"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-select
                      v-model="data.staffs[0].projects_in"
                      :items="data.staffs[0].projects_in"
                      label="Projects Involved"
                      multiple
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-select
                      :value="data.staffs[0].languages.map(item => item.language)"
                      :items="data.staffs[0].languages.map(item => item.language)"
                      label="Languages understand and/or speak"
                      multiple
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      v-model="data.staffs[0].ws_place"
                      label="Current Place of Work / Study"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      v-model="data.staffs[0].profession"
                      label="Profession"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-switch
                      v-model="data.staffs[0].is_speech_therapist"
                      label="Speech Therapist?"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6" class="py-0">
                    <v-text-field
                      v-model="data.staffs[0].date_joined"
                      label="Date Joined"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row v-if="data.staffs.role != '' && data.staffs.role != 'core_team'" class="mt-3">
                  <v-col col="12" class="py-0">
                    <span>Supervisor Details</span>
                  </v-col>
                </v-row>
                <v-row v-if="data.staffs.role != '' && data.staffs.role != 'core_team'">
                  <v-col cols="6" class="py-0">
                    <v-select
                      :value="data.staffs[0].supervisors.map(item => item.supervisor.name)"
                      :items="data.staffs[0].supervisors.map(item => item.supervisor.name)"
                      label="Tag Supervisor(s)"
                      multiple
                      readonly
                    />
                  </v-col>
                </v-row>
              </v-container>
            </div>

            <div v-else>Staff Not Found</div>
          </template>
        </ApolloQuery>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import { ROLE_OPTIONS, GENDER_OPTIONS } from './../../assets/data'
import EditStaffModal from './modals/EditStaffModal'

export default {
  components: { EditStaffModal },
  data () {
    return {
      staffId: Number(this.$route.query.id),
      ROLE_OPTIONS,
      GENDER_OPTIONS
    }
  }
}
</script>
<style scoped>
.hover-underline > a {
  color: inherit;
  text-decoration: none !important;
}
.hover-underline > a:hover {
  text-decoration: underline !important;
}
</style>
