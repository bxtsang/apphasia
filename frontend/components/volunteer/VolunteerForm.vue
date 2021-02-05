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
            <v-select
              :value="volunteer.project_vols.filter(item => item.interested).map(item => item.project.title)"
              :items="volunteer.project_vols.filter(item => item.interested).map(item => item.project.title)"
              label="Projects Interested"
              multiple
              readonly
            />
          </v-col>
          <v-col class="py-0">
            <v-select
              :value="volunteer.project_vols.filter(item => item.approved).map(item => item.project.title)"
              :items="volunteer.project_vols.filter(item => item.approved).map(item => item.project.title)"
              label="Projects Involved In"
              multiple
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
        </v-row>
        <v-row class="mt-8">
          <v-col cols="12" class="py-0">
            <span class="font-weight-bold">Volunteer Status</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <VolTypeInput
              v-model="voltypes"
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
            <VolunteerIcInput
              v-model="vol_ic"
            />
          </v-col>
        </v-row>
      </v-container>
      <v-container>
        <v-row>
          <v-btn v-if="volunteer" color="error" class="my-3" @click="deleteVolunteer()">
            Delete
          </v-btn>
          <v-spacer />
          <v-btn color="primary" class="my-3" type="submit" :loading="isSubmitting">
            Save
          </v-btn>
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
      generalInfo: this.removeKey(this.volunteer.general_info, '__typename'),
      volunteerDetails: this.removeKey(this.removeKey(this.volunteer, 'general_info'), '__typename'),
      languages: this.volunteer.vol_languages.map(item => item.language),
      voltypes: this.volunteer.vol_voltypes.map(item => item.voltype),
      vol_ic: this.volunteer.vol_ic.map(item => item.ic.id),
      isSubmitting: false
    }
  },
  watch: {
    languages: {
      immediate: true,
      handler (newValue, oldValue) {
        this.volunteerDetails.languages = {
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
    vol_ic: {
      immediate: true,
      handler (newValue, oldValue) {
        this.volunteerDetails.vol_ic = {
          data: newValue.map((item) => { return { ic: item } })
        }
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
    deleteVolunteer () {
    //  to implement
    },
    updateVolunteer () {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        // const languageChanges = this.getLanguageChanges()
        // const volIcChanges = this.getVolIcChanges()
        // const volTypeChanges = this.getVolTypeChanges()
        // const projectChanges = this.getProjectInterestChanges()
        this.$apollo.mutate({
          mutation: UpdateVol,
          variables: {
            volunteer: this.volunteerDetails,
            id: this.volunteerDetails.id,
            general_info: this.generalInfo
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
          console.log('success')
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
