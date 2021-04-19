<template>
  <v-row>
    <v-col>
      <v-card class="px-6 py-3">
        <ApolloQuery
          :query="require('./../../graphql/pwa/GetSinglePWA.graphql')"
          :variables="{ id: pwaId }"
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
              <ResourceNotFound />
            </div>

            <!-- Display on success -->
            <div v-else-if="data && data.pwas_by_pk">
              <v-container class="pa-0 ma-0">
                <v-row>
                  <v-col>
                    <h1 class="title hover-underline">
                      <NuxtLink to="/pwas">
                        PWAs
                      </NuxtLink>
                      <span>/ {{ data.pwas_by_pk.general_info.name }}</span>
                    </h1>
                  </v-col>
                  <v-col class="d-flex justify-end">
                    <EditResourceModal
                      v-if="editPermission"
                      :resourceType="resourceType"
                      :resource="data.pwas_by_pk"
                      :text="true"
                    />
                  </v-col>
                </v-row>
                <v-row class="mt-3">
                  <v-col cols="12" class="py-0">
                    <span class="font-weight-bold">Personal Details</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.general_info.name"
                      label="Full Name"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="4" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.general_info.dob"
                      label="Date of Birth"
                      readonly
                    />
                  </v-col>
                  <v-col cols="4" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.general_info.contact_num"
                      label="Contact Number"
                      readonly
                    />
                  </v-col>
                  <v-col cols="4" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.general_info.gender"
                      label="Gender"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="4" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.general_info.email"
                      label="Email Address"
                      readonly
                    />
                  </v-col>
                  <v-col cols="8" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.general_info.address"
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
                  <v-col cols="6" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.general_info.bio"
                      label="Hobbies / Interests"
                      readonly
                    />
                  </v-col>
                  <v-col cols="6" class="py-0">
                    <v-select
                      :value="data.pwas_by_pk.wheelchair"
                      :items="[{ value: true, text: 'Yes' }, { value: false, text: 'No' }]"
                      label="Wheelchair needed?"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6" class="py-0">
                    <v-select
                      :value="data.pwas_by_pk.projects.map(item => item.project.title)"
                      :items="data.pwas_by_pk.projects.map(item => item.project.title)"
                      label="Programmes Involved in"
                      multiple
                      readonly
                    />
                  </v-col>
                  <v-col cols="6" class="py-0">
                    <v-select
                      :value="data.pwas_by_pk.comm_diff.map(item => item.difficulty)"
                      :items="data.pwas_by_pk.comm_diff.map(item => item.difficulty)"
                      label="Communication Difficulties"
                      multiple
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6" class="py-0">
                    <v-select
                      :value="data.pwas_by_pk.languages.map(item => item.language)"
                      :items="data.pwas_by_pk.languages.map(item => item.language)"
                      label="Languages undestand and/or speak"
                      multiple
                      readonly
                    />
                  </v-col>
                  <v-col cols="6" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.stroke_date"
                      label="When did stroke/brain injury happen?"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.general_info.channel"
                      label="How did you hear about Aphasia SG"
                      readonly
                    />
                  </v-col>
                  <v-col cols="6" class="py-0">
                    <ConsentInput
                      :value="data.pwas_by_pk.general_info.consent"
                      :required="true"
                      input-type="select"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6" class="py-0">
                    <v-select
                      :value="data.pwas_by_pk.media_willingness"
                      :items="[{ value: true, text: 'Yes' }, { value: false, text: 'No' }]"
                      label="Agreeable to speak to Media?"
                      readonly
                    />
                  </v-col>
                  <v-col cols="6" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.media_engagement_details"
                      label="Participated in any media projects?"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6" class="py-0">
                    <v-select
                      :value="data.pwas_by_pk.contact_status"
                      :items="[data.pwas_by_pk.contact_status]"
                      label="Status"
                      readonly
                    />
                  </v-col>
                  <v-col v-if="contactedButNoResponse(data.pwas_by_pk.contact_status)" cols="6" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.last_contact_details"
                      label="Last Contacted Details"
                      readonly
                    />
                  </v-col>
                  <v-col cols="6" class="py-0">
                    <v-select
                      :value="data.pwas_by_pk.comm_mode"
                      :items="[data.pwas_by_pk.comm_mode]"
                      label="Preferred mode of communication"
                      readonly
                    />
                  </v-col>
                  <v-col cols="6" class="py-0">
                    <v-textarea
                      :value="data.pwas_by_pk.general_info.notes"
                      auto-grow
                      label="Any additional info of the PWA?"
                      rows="1"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row class="mt-8">
                  <v-col cols="12" class="py-0">
                    <span class="font-weight-bold">Speech Therapist Details</span>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="6" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.speech_therapist"
                      label="Name of Speech Therapist"
                      readonly
                    />
                  </v-col>
                  <v-col cols="6" class="py-0">
                    <v-text-field
                      :value="data.pwas_by_pk.hospital"
                      label="Discharge from which hospital?"
                      readonly
                    />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <div v-for="(nok, index) in data.pwas_by_pk.nok" :key="index">
                      <v-row>
                        <v-col cols="12" class="py-0 d-flex">
                          <span class="font-weight-bold">({{ index + 1 }}) Caregiver Information</span>
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="12" class="py-0">
                          <v-text-field
                            :value="nok.name"
                            label="Name of Caregiver / NOK"
                            readonly
                          />
                        </v-col>
                      </v-row>
                      <v-row>
                        <v-col cols="4" class="py-0">
                          <v-text-field
                            :value="nok.relationship"
                            label="Relationship with PWA"
                            readonly
                          />
                        </v-col>
                        <v-col cols="4" class="py-0">
                          <v-text-field
                            :value="nok.contact_num"
                            label="Contact Number"
                            readonly
                          />
                        </v-col>
                        <v-col cols="4" class="py-0">
                          <v-text-field
                            :value="nok.email"
                            label="Email Address"
                            readonly
                          />
                        </v-col>
                      </v-row>
                    </div>
                  </v-col>
                </v-row>
              </v-container>
            </div>

            <div v-else>
              <ResourceNotFound />
            </div>
          </template>
        </ApolloQuery>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { EDIT_RESOURCE_PERMISSIONS } from './../../assets/data'

export default {
  props: {
    resourceType: {
      type: String,
      default: null
    }
  },
  data () {
    return {
      pwaId: Number(this.$route.query.id),
      EDIT_RESOURCE_PERMISSIONS
    }
  },
  computed: {
    editPermission () {
      return this.EDIT_RESOURCE_PERMISSIONS[this.resourceType].includes(this.$auth.user['custom:role'])
    }
  },
  methods: {
    contactedButNoResponse (contactStatus) {
      return contactStatus === 'Contacted but no response'
    }
  }
}
</script>
