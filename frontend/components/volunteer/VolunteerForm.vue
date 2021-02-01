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
        is_active: this.staff.is_active,
        is_speech_therapist: this.staff.is_speech_therapist,
        name: this.staff.name,
        nickname: this.staff.nickname,
        notes: this.staff.notes,
        profession: this.staff.profession,
        rejection_reason: this.staff.rejection_reason,
        status: this.volunteer.status_description.description,
        ws_place: this.volunteer.ws_place,
        // projects_approved: this.volunteer.project_vols.filter(item => item.approved),
        // projects_interested: this.volunteer.project_vols,
        vol_languages: this.vol_languages,
        vol_ic: this.vol_ic,
        vol_voltypes: this.vol_voltypes
      }
    }
  },
  methods: {
    updateVolunteer () {
      if (this.$refs.form.validate()) {
        const languageChanges = this.getLanguageChanges()
        const volIcChanges = this.getVolIcChanges()
        this.$apollo.mutate({
          mutation: UpdateVol,
          variables: {

          }
        })
      }
    },
    getLanguageChanges () {

    },
    getVolIcChanges () {

    }
  }
}
</script>

<style>

</style>
