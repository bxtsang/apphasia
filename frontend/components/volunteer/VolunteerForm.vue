<template>
  <v-card class="pa-8">
    <span class="section-title">Edit Volunteer</span>
    <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="updateVolunteer">
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
              v-model="project_vols"
              label="*Projects Interested In"
            />
          </v-col>
          <v-col class="py-0">
            <ProjectInput
              v-model="projects_interested"
              label="*Projects Involved"
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
            v-if="$auth.user['custom:role'] === 'core_team'"
            :resource="volunteer"
            :resourceType="'volunteers'"
            @deleteSuccess="$emit('closeForm')"
          />
          <v-spacer />
          <v-btn color="primary" class="my-3" type="submit" :loading="isSubmitting">
            Save
          </v-btn>
        </v-row>
      </v-container>

      {{ project_vols }}
    </v-form>
  </v-card>
</template>

<script>
import UpdateVol from './../../graphql/volunteer/UpdateVol.graphql'
import GetSingleVol from './../../graphql/volunteer/GetSingleVol.graphql'
import GetAllVol from './../../graphql/volunteer/GetAllVol.graphql'

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
        voltypes: [],
        vol_ic: [],
        project_vols: [],
        projects_interested: []
      },
      languages: this.volunteer ? this.volunteer.vol_languages.map(item => item.language) : [],
      voltypes: this.volunteer ? this.volunteer.vol_voltypes.map(item => item.voltype) : [],
      volIc: this.volunteer ? this.volunteer.vol_ic.map(item => item.staff_id) : [],
      project_vols: this.volunteer ? this.volunteer.project_vols.map(item => item.project.id) : [],
      projects_interested: this.volunteer ? this.volunteer.project_vols.filter(project => project.interested).map(item => item.project.id) : [],
      isSubmitting: false
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
          data: newValue.map((item) => { return { project_id: item.project_id } })
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
                is_active: true
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
            store.writeQuery({
              query: GetSingleVol,
              data: { volunteers_by_pk: updatedVolunteer },
              variables: { id: this.volunteerDetails.id }
            })
            try {
              const allVol = store.readQuery({
                query: GetAllVol,
                variables: {}
              })
              allVol.volunteers = allVol.volunteers.filter(item => item.id !== this.volunteer.id)
              allVol.volunteers.push(updatedVolunteer)
              store.writeQuery({
                query: GetAllVol,
                allVol,
                variables: {}
              })
            } catch (error) {
              // Handle if GetAllVols query not in store
            }
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
