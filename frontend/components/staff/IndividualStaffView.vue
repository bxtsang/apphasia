<template>
  <v-row>
    <v-col>
      <v-card class="px-6 py-3">
        <ApolloQuery
          :query="require('./../../graphql/staff/GetSingleStaff.graphql')"
          :variables="{ id: staffId , 'isCoreTeam': $auth.user['custom:role'] === 'core_team'}"
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
            <div v-else-if="error">
              An error occurred
            </div>

            <!-- Result -->
            <div v-else-if="data && data.staffs.length > 0">
              <v-container class="pa-0 ma-0">
                <v-row>
                  <v-col>
                    <h1 class="title hover-underline">
                      <NuxtLink to="/staffs">
                        Staffs
                      </NuxtLink>
                      <span>/ {{ data.staffs[0].name }}</span>
                    </h1>
                  </v-col>
                  <v-col class="d-flex justify-end">
                    <EditResourceModal
                      v-if="editPermission"
                      :resourceType="resourceType"
                      :resource="data.staffs[0]"
                      :text="true"
                    />
                  </v-col>
                </v-row>
                <v-row v-if="!data.staffs[0].is_active" class="mt-2">
                  <v-col class="py-0">
                    <v-chip color="error">
                      Archived
                    </v-chip>
                  </v-col>
                </v-row>
                <v-row v-if="!data.staffs[0].is_active">
                  <v-col class="py-0 mt-1">
                    <span class="font-italic">Reason for archiving: {{ data.staffs[0].archive_reason ? data.staffs[0].archive_reason : 'None' }}</span>
                  </v-col>
                </v-row>
                <v-row class="mt-4">
                  <v-col cols="12" class="py-0">
                    <span>Role</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-radio-group :value="data.staffs[0].role_description.role" readonly row>
                      <v-radio v-for="role in ROLE_OPTIONS.filter(item => item.value == data.staffs[0].role_description.role)" :key="role.value" :label="role.label" :value="role.value" />
                    </v-radio-group>
                  </v-col>
                </v-row>
                <v-row class="mt-8">
                  <v-col cols="12" class="py-0">
                    <span class="font-weight-bold">Personal Details</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.staffs[0].name"
                      label="Full Name"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.staffs[0].nickname"
                      label="Nickname / Alias"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.staffs[0].dob"
                      label="Date of Birth"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.staffs[0].contact_num"
                      label="Contact"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-select
                      :value="data.staffs[0].gender"
                      :items="GENDER_OPTIONS"
                      label="Gender"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0" cols="4">
                    <v-text-field
                      :value="data.staffs[0].email"
                      label="Email Address"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0" cols="8">
                    <v-text-field
                      :value="data.staffs[0].address || 'Not Available'"
                      label="Home Address"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row class="mt-8">
                  <v-col cols="12" class="py-0">
                    <span class="font-weight-bold">Additional Information</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.staffs[0].bio"
                      label="Hobbies / Interests"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-select
                      :value="data.staffs[0].projects_in.map(item => item.project.title)"
                      :items="data.staffs[0].projects_in.map(item => item.project.title)"
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
                      :value="data.staffs[0].ws_place"
                      label="Current Place of Work / Study"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.staffs[0].profession"
                      label="Profession"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <SpeechTherapistInput
                      :value="data.staffs[0].is_speech_therapist"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6" class="py-0">
                    <v-text-field
                      :value="data.staffs[0].date_joined"
                      label="Date Joined"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row v-if="data.staffs.role != '' && data.staffs.role != 'core_team'" class="mt-3">
                  <v-col cols="12" class="py-0">
                    <span>Supervisor Details</span>
                  </v-col>
                </v-row>
                <v-row v-if="data.staffs.role != '' && data.staffs.role != 'core_team'">
                  <v-col cols="6" class="py-0">
                    <v-select
                      :value="data.staffs[0].supervisors.map(item => item.supervisor.name)"
                      :items="data.staffs[0].supervisors.map(item => item.supervisor.name)"
                      label="Supervisor(s)"
                      multiple
                      readonly
                    />
                  </v-col>
                </v-row>
              </v-container>
            </div>

            <div v-else>
              Staff Not Found
            </div>
          </template>
        </ApolloQuery>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
import { ROLE_OPTIONS, GENDER_OPTIONS, EDIT_RESOURCE_PERMISSIONS } from './../../assets/data'
import EditResourceModal from './../modals/EditResourceModal'

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
      staffId: Number(this.$route.query.id),
      ROLE_OPTIONS,
      GENDER_OPTIONS,
      EDIT_RESOURCE_PERMISSIONS
    }
  },

  computed: {
    editPermission () {
      return this.EDIT_RESOURCE_PERMISSIONS[this.resourceType].includes(this.$auth.user['custom:role'])
    }
  }
}
</script>
