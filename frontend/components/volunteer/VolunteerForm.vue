<template>
  <v-card class="pa-8">
    <span class="section-title">Edit Volunteer</span>
    <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="updateVolunteer">
      <v-container class="pa-0">
        <v-row>
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
              v-model="generalInfo.nickname"
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
            <v-select
              :value="volunteer.project_vols.map(item => item.project.title)"
              :items="volunteer.project_vols.map(item => item.project.title)"
              label="Projects Interested"
              multiple
              readonly
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
            <LanguageInput
              :value="volunteerDetails.vol_languages.data.map(item => item.language)"
              :items="volunteerDetails.vol_languages.data.map(item => item.language)"
              label="Languages"
              multiple
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
            <ConsentInput
              v-model="generalInfo.consent"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-textarea
              v-model="generalInfo.notes"
              :label="'Notes'"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-select
              :value="volunteer.project_vols.map(item => item.project.title)"
              :items="volunteer.project_vols.map(item => item.project.title)"
              label="Projects Interested"
              multiple
              readonly
            />
          </v-col>
        </v-row>
        <v-row class="mt-8">
          <v-col cols="12" class="py-0">
            <span class="font-weight-bold">Volunteer Status</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <VolTypeInput
              :value="volunteerDetails.vol_voltypes.data.map(item => item.voltype)"
            />
          </v-col>
          <v-col>
            <VolunteerStatusInput
              v-model="volunteerDetails.status"
            />
          </v-col>
        </v-row>
        <v-row class="mt-8">
          <v-col cols="12" class="py-0">
            <span class="font-weight-bold">In-Charge Details</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            IC input
          </v-col>
        </v-row>
      </v-container>
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
      generalInfo: {
        address: this.volunteer.general_info.address,
        bio: this.volunteer.general_info.bio,
        channel: this.volunteer.general_info.channel,
        contact_num: this.volunteer.general_info.contact_num,
        consent: this.volunteer.general_info.consent,
        date_joined: this.volunteer.general_info.date_joined,
        dob: this.volunteer.general_info.dob,
        email: this.volunteer.general_info.email,
        gender: this.volunteer.general_info.gender,
        name: this.volunteer.general_info.name,
        nickname: this.volunteer.general_info.nickname,
        notes: this.volunteer.general_info.notes
      },
      volunteerDetails: {
        is_speech_therapist: this.volunteer.is_speech_therapist,
        profession: this.volunteer.profession,
        status_reason: this.volunteer.status_reason,
        rejected_date: this.volunteer.rejected_date,
        status: this.volunteer.status,
        ws_place: this.volunteer.ws_place,
        project_vols: {
          data: this.volunteer.project_vols.map(item => this.removeKey(item, 'project'))
        },
        vol_languages: { data: this.volunteer.vol_languages },
        vol_ic: {
          data: this.volunteer
        },
        vol_voltypes: { data: this.volunteer.vol_voltypes }
      }
    }
  },
  methods: {
    removeKey (item, excessKey) {
      return Object.keys(item)
        .filter(key => key !== excessKey)
        .reduce((newObj, key) => {
          newObj[key] = item[key]
          return newObj
        }, {})
    },
    updateVolunteer () {
      if (this.$refs.form.validate()) {
        // const languageChanges = this.getLanguageChanges()
        // const volIcChanges = this.getVolIcChanges()
        // const volTypeChanges = this.getVolTypeChanges()
        // const projectChanges = this.getProjectInterestChanges()
        this.$apollo.mutate({
          mutation: UpdateVol,
          variables: {
          //  to be added
          },
          update: (
            store, {
              data: {
                update_volunteers: {
                  returning: [updatedVolunteer]
                }
              }
            }
          ) => {
            store.writeQuery({
              query: GetSingleVol,
              data: { volunteers: [updatedVolunteer] },
              variables: {}
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
              // Handle if GetAllStaff query not in store
            }
          }
        }).then((data) => {
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['Volunteer successfully updated', 'successful'])
        }).catch((error) => {
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    getLanguageChanges () {
      const originalArray = this.volunteer.languages.map(item => item.language)
      const currentArray = this.volunteerData.languages
      const added = []
      const removed = []
      for (const language of originalArray) {
        if (!currentArray.find(item => item === language)) {
          removed.push(language)
        }
      }
      for (const language of currentArray) {
        if (!originalArray.find(item => item === language)) {
          added.push({ language, vol_id: this.volunteer.id })
        }
      }
      return { added, removed }
    },
    getVolIcChanges () {
      const originalArray = this.volunteer.vol_ic.map(item => item.ic)
      const currentArray = this.volunteerData.vol_ic
      const added = []
      const removed = []
      for (const ic of originalArray) {
        if (!currentArray.find(item => item === ic)) {
          removed.push(ic)
        }
      }
      for (const ic of currentArray) {
        if (!originalArray.find(item => item === ic)) {
          added.push({ ic, vol_id: this.volunteer.id })
        }
      }
      return { added, removed }
    },
    getVolTypeChanges () {
      const originalArray = this.volunteer.vol_voltypes.map(item => item.voltypes)
      const currentArray = this.volunteerData.vol_voltypes
      const added = []
      const removed = []
      for (const voltype of originalArray) {
        if (!currentArray.find(item => item === voltype)) {
          removed.push(voltype)
        }
      }
      for (const voltype of currentArray) {
        if (!originalArray.find(item => item === voltype)) {
          added.push({ voltype, vol_id: this.volunteer.id })
        }
      }
      return { added, removed }
    },
    getProjectInterestChanges () {
      const originalArray = this.volunteer.project_vols.map(item => item.project)
      const currentArray = this.volunteerData.projects_interested
      const added = []
      const removed = []
      for (const project of originalArray) {
        if (!currentArray.find(item => item === project)) {
          removed.push(project)
        }
      }
      for (const project of currentArray) {
        if (!originalArray.find(item => item === project)) {
          added.push({ project, vol_id: this.volunteer.id })
        }
      }
      return { added, removed }
    }
  }
}
</script>

<style>

</style>
