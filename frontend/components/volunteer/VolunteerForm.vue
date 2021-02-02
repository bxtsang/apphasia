<template>
  <v-card>
    <span v-if="volunteer" class="section-title">Edit Volunteer</span>
    <span v-else class="section-title">Add Volunteer</span>
    <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="updateVolunteer">
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
      volunteerData: {
        address: this.volunteer.address,
        bio: this.volunteer.bio,
        channel: this.volunteer.channel_description.channel,
        consent: this.volunteer.consent,
        contact_num: this.volunteer.contact_num,
        date_joined: this.volunteer.date_joined,
        dob: this.volunteer.dob,
        email: this.volunteer.email,
        gender: this.volunteer.gender,
        is_active: this.volunteer.is_active,
        is_speech_therapist: this.volunteer.is_speech_therapist,
        name: this.volunteer.name,
        nickname: this.volunteer.nickname,
        notes: this.volunteer.notes,
        profession: this.volunteer.profession,
        rejection_reason: this.volunteer.rejection_reason,
        rejected_date: this.volunteer.rejected_date,
        status: this.volunteer.status_description.status,
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
        const languageChanges = this.getLanguageChanges()
        const volIcChanges = this.getVolIcChanges()
        const volTypeChanges = this.getVolTypeChanges()
        const projectChanges = this.getProjectInterestChanges()
        this.$apollo.mutate({
          mutation: UpdateVol,
          variables: {
            address: this.volunteerData.address,
            bio: this.volunteerData.bio,
            channel: this.volunteerData.channel,
            consent: this.volunteerData.consent,
            contact_num: this.volunteerData.contact_num,
            dob: this.volunteerData.dob,
            gender: this.volunteerData.gender,
            is_active: this.volunteerData.is_active,
            is_speech_therapist: this.volunteerData.is_speech_therapist,
            name: this.volunteerData.name,
            nickname: this.volunteerData.nickname,
            notes: this.volunteerData.notes,
            profession: this.volunteerData.profession,
            rejection_reason: this.volunteerData.rejection_reason,
            rejection_date: this.volunteerData.rejection_date,
            status: this.volunteerData.status,
            ws_place: this.volunteerData.ws_place,
            languages_to_add: languageChanges.added,
            languages_to_remove: languageChanges.removed,
            projects_to_add: projectChanges.added,
            projects_to_remove: projectChanges.removed,
            ic_to_add: volIcChanges.added,
            ic_to_remove: volIcChanges.removed,
            voltypes_to_add: volTypeChanges.added,
            voltypes_to_remove: volTypeChanges.removed
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
