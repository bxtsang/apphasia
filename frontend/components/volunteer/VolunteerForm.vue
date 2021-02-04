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
        projects_interested: this.volunteer.project_vols,
        vol_languages: this.volunteer.vol_languages,
        vol_ic: this.volunteer.vol_ic,
        vol_voltypes: this.volunteer.vol_voltypes
      }
    }
  },
  methods: {
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
