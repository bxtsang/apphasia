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
            <div v-else-if="data && data.volunteers_by_pk">
              <v-container class="pa-0 ma-0">
                <v-row>
                  <v-col>
                    <h1 class="title hover-underline">
                      <NuxtLink to="/volunteers">
                        Volunteers
                      </NuxtLink>
                      <span>/ {{ data.volunteers_by_pk.general_info.name }}</span>
                    </h1>
                  </v-col>
                  <v-col class="d-flex justify-end">
                    <EditResourceModal
                      v-if="editPermission"
                      :resourceType="resourceType"
                      :resource="data.volunteers_by_pk"
                      :text="true"
                    />
                  </v-col>
                </v-row>
                <v-row class="mt-2">
                  <v-col cols="12" class="py-0">
                    <VolunteerStatusChip :value="data.volunteers_by_pk.status"/>
                  </v-col>
                </v-row>
                <v-row v-if="data.volunteers_by_pk.status === 'Rejected' || data.volunteers_by_pk.status === 'KIV'">
                  <v-col class="py-0 mt-1">
                    <span class="font-italic">Reason for {{ data.volunteers_by_pk.status }}: {{ data.volunteers_by_pk.status_reason }}</span>
                  </v-col>
                </v-row>
                <v-row v-else-if="data.volunteers_by_pk.status === 'Approved'">
                  <v-col class="py-0 mt-2" cols="4">
                    <VolTypeInput
                      :value="data.volunteers_by_pk.vol_voltypes.map(item => item.voltype)"
                      :readonly="true"
                    />
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
                      :value="data.volunteers_by_pk.general_info.name"
                      label="Full Name"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers_by_pk.general_info.nickname"
                      label="Nickname / Alias"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers_by_pk.general_info.dob"
                      label="Date of Birth"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers_by_pk.general_info.contact_num"
                      label="Contact"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-select
                      :value="data.volunteers_by_pk.general_info.gender"
                      :items="GENDER_OPTIONS"
                      label="Gender"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0" cols="4">
                    <v-text-field
                      :value="data.volunteers_by_pk.general_info.email"
                      label="Email Address"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0" cols="8">
                    <v-text-field
                      :value="data.volunteers_by_pk.general_info.address || 'Not Available'"
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
                  <v-col cols="12" class="py-0">
                    <v-text-field
                      :value="data.volunteers_by_pk.general_info.bio"
                      label="Self Description"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-select
                      :value="data.volunteers_by_pk.project_vols.map(item => item.project.title)"
                      :items="data.volunteers_by_pk.project_vols.map(item => item.project.title)"
                      label="Projects Interested"
                      multiple
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-select
                      :value="data.volunteers_by_pk.project_vols.filter(item => item.approved).map(item => item.project.title)"
                      :items="data.volunteers_by_pk.project_vols.filter(item => item.approved).map(item => item.project.title)"
                      label="Projects Involved"
                      multiple
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-select
                      :value="data.volunteers_by_pk.vol_languages.map(item => item.language)"
                      :items="data.volunteers_by_pk.vol_languages.map(item => item.language)"
                      label="Languages understand and/or speak"
                      multiple
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers_by_pk.ws_place"
                      label="Current Place of Work / Study"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers_by_pk.profession"
                      label="Profession"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-switch
                      :input-value="data.volunteers_by_pk.is_speech_therapist"
                      label="Speech Therapist?"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.volunteers_by_pk.general_info.channel"
                      label="Channel"
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-switch
                      :input-value="data.volunteers_by_pk.consent"
                      label="Consent to Updates?"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-select
                      :items="data.volunteers_by_pk.vol_ic.map(item => item.ic.name)"
                      :value="data.volunteers_by_pk.vol_ic.map(item => item.ic.name)"
                      label="In-Charge(s)"
                      multiple
                      readonly
                    />
                  </v-col>
                  <v-col class="py-0">
                    <v-textarea
                      label="Notes"
                      :value="data.volunteers_by_pk.general_info.notes"
                      rows="1"
                      auto-grow
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
import { GENDER_OPTIONS, EDIT_RESOURCE_PERMISSIONS } from './../../assets/data'
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
