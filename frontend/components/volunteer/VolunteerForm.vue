<template>
  <v-card>
    <v-toolbar dark color="primary">
      <v-toolbar-title>
        {{ volunteer ? 'Edit Volunteer' : 'Add Volunteer'}}
      </v-toolbar-title>
      <v-spacer />
      <v-btn icon dark @click="$emit('closeForm')">
        <v-icon>mdi-close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-form ref="form" v-model="valid" class="pa-8" @submit.prevent="formSubmitMethod">
      <v-container class="pa-0">
        <v-row>
          <v-col cols="12" class="py-0">
            <span class="font-weight-bold">Volunteer Status</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <VolunteerStatusInput
              v-model="volunteerDetails.status"
            />
          </v-col>
          <v-col v-if="volunteerDetails.status === 'Approved'" class="py-0">
            <VolTypeInput
              v-model="voltypes"
            />
          </v-col>
        </v-row>
        <v-row v-if="volunteerDetails.status === 'Rejected' || volunteerDetails.status === 'KIV'">
          <v-col class="py-0">
            <GeneralOptionalText
              v-model="volunteerDetails.status_reason"
              :label="`Reason for ${ volunteerDetails.status }`"
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
            <NameInput
              v-model="generalInfo.name"
              :required="true"
            />
          </v-col>
          <v-col class="py-0">
            <AliasInput
              v-model="volunteerDetails.nickname"
            />
          </v-col>
          <v-col class="py-0">
            <DateOfBirthInput
              v-model="generalInfo.dob"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <ContactInput
              v-model="generalInfo.contact_num"
            />
          </v-col>
          <v-col class="py-0">
            <GenderInput
              v-model="generalInfo.gender"
            />
          </v-col>
          <v-col class="py-0">
            <EmailInput
              v-model="generalInfo.email"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="8" class="py-0">
            <AddressInput
              v-model="generalInfo.address"
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
            <BioInput
              v-model="generalInfo.bio"
            />
          </v-col>
          <v-col class="py-0">
            <ProfessionInput
              v-model="volunteerDetails.profession"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <ProjectInput
              v-model="interested_projects"
              label="*Projects Interested In"
            />
          </v-col>
          <v-col class="py-0">
            <ProjectInput
              v-model="project_vols"
              label="*Projects Involved (assign only in projects page)"
              readonly
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <LanguageInput
              v-model="languages"
              :required="true"
            />
          </v-col>
          <v-col class="py-0">
            <DateJoinedInput
              v-model="generalInfo.date_joined"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <ChannelInput
              v-model="generalInfo.channel"
            />
          </v-col>
          <v-col class="py-0">
            <WorkplaceInput
              v-model="volunteerDetails.ws_place"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <ConsentInput
              v-model="generalInfo.consent"
            />
          </v-col>
          <v-col>
            <SpeechTherapistInput
              v-model="volunteerDetails.is_speech_therapist"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-textarea
              v-model="generalInfo.notes"
              label="Any additional info of the Volunteer?"
              rows="1"
              auto-grow
            />
          </v-col>
        </v-row>
        <v-row class="mt-8">
          <v-col cols="12" class="py-0">
            <span class="font-weight-bold">In-Charge Details</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <VolunteerIcInput
              v-model="volIc"
            />
          </v-col>
        </v-row>
      </v-container>
      <v-container>
        <v-row>
          <DeleteResourceModal
            v-if="($auth.user['custom:role'] === 'core_team' || $auth.user['custom:role'] === 'admin') && volunteer"
            :resource="volunteer"
            :resourceType="'volunteers'"
            @deleteSuccess="$emit('closeForm')"
          />
          <v-spacer />
          <v-btn color="primary" type="submit" :loading="isSubmitting">
            Save
          </v-btn>
          <v-btn class="ml-1" dark color="grey" @click="$emit('closeForm')">Cancel</v-btn>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
</template>

<script>
import UpdateVol from './../../graphql/volunteer/UpdateVol.graphql'
import CreateVol from './../../graphql/volunteer/CreateVol.graphql'

export default {
  props: {
    volunteer: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      valid: true,
      generalInfo: this.volunteer ? this.removeKeys(this.volunteer.general_info, ['__typename']) : {},
      volunteerDetails: this.volunteer ? this.removeKeys(this.volunteer, ['general_info', '__typename', 'befrienders']) : {
        vol_languages: [],
        vol_voltypes: [],
        vol_ic: [],
        project_vols: [],
        interested_projects: []
      },
      languages: this.volunteer ? this.volunteer.vol_languages.map(item => item.language) : [],
      voltypes: this.volunteer ? this.volunteer.vol_voltypes.map(item => item.voltype) : [],
      volIc: this.volunteer ? this.volunteer.vol_ic.map(item => item.staff_id) : [],
      project_vols: this.volunteer ? this.volunteer.project_vols.map(item => item.project.id) : [],
      interested_projects: this.volunteer ? this.volunteer.interested_projects.map(item => item.project.id) : [],
      isSubmitting: false
    }
  },

  computed: {
    formSubmitMethod () {
      if (this.volunteer) {
        return this.updateVolunteer
      } else {
        return this.addVolunteer
      }
    }
  },

  watch: {
    languages: {
      immediate: true,
      handler (newValue, oldValue) {
        this.volunteerDetails.vol_languages = {
          data: newValue.map((item) => { return { language: item } })
        }
      }
    },
    voltypes: {
      immediate: true,
      handler (newValue, oldValue) {
        this.volunteerDetails.vol_voltypes = {
          data: newValue.map((item) => { return { voltype: item } })
        }
      }
    },
    volIc: {
      immediate: true,
      handler (newValue, oldValue) {
        this.volunteerDetails.vol_ic = {
          data: newValue.map((item) => { return { staff_id: item } })
        }
      }
    },
    project_vols: {
      immediate: true,
      handler (newValue, oldValue) {
        this.volunteerDetails.project_vols = {
          data: newValue.map((item) => { return { project_id: item } })
        }
      }
    },
    interested_projects: {
      immediate: true,
      handler (newValue) {
        this.volunteerDetails.interested_projects = {
          data: newValue.map((item) => { return { project_id: item } })
        }
      }
    }
  },
  methods: {
    removeKeys (item, excessKeys) {
      return Object.keys(item)
        .filter(key => !excessKeys.includes(key))
        .reduce((newObj, key) => {
          newObj[key] = item[key]
          return newObj
        }, {})
    },

    addVolunteer () {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        this.volunteerDetails.general_info = { data: this.generalInfo }

        this.$apollo.mutate({
          mutation: CreateVol,
          variables: { volunteer: this.volunteerDetails },
          update: (store, { data: { insert_volunteers_one: newVol } }) => {
            this.$apollo.vm.$apolloProvider.defaultClient.resetStore()
          }
        }).then((data) => {
          this.isSubmitting = false
          this.languages = []
          this.voltypes = []
          this.volIc = []
          this.project_vols = []
          this.interested_projects = []
          this.generalInfo = {}
          this.volunteerDetails = {
            vol_languages: [],
            vol_voltypes: [],
            vol_ic: [],
            project_vols: [],
            interested_projects: []
          }

          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['Volunteer successfully created', 'success'])
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },

    updateVolunteer () {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        this.$apollo.mutate({
          mutation: UpdateVol,
          variables: {
            volunteer: this.volunteerDetails,
            id: this.volunteerDetails.id,
            general_info: this.generalInfo,
            updateNotification: {
              old: this.volunteer,
              new: {
                id: this.volunteerDetails.id,
                ...this.volunteerDetails,
                is_active: true,
                archive_reason: ''
              },
              general_info: this.generalInfo
            }
          },
          update: (
            store, {
              data: {
                insert_volunteers_one: updatedVolunteer
              }
            }
          ) => {
            this.$apollo.vm.$apolloProvider.defaultClient.resetStore()
          }
        }).then((data) => {
          this.isSubmitting = false
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['Volunteer successfully updated', 'success'])
        }).catch((error) => {
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    }
  }
}
</script>

<style>

</style>
