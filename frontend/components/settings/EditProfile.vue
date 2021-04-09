<template>
  <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="submitForm">
    <v-container class="pa-0">
      <v-row class="mt-8">
        <v-col col="12" class="py-0">
          <span class="font-weight-bold">Personal Details</span>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <NameInput
            v-model="profileData.name"
            :required="true"
          />
        </v-col>
        <v-col class="py-0">
          <AliasInput
            v-model="profileData.nickname"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <DateOfBirthInput
            v-model="profileData.dob"
            :required="true"
          />
        </v-col>
        <v-col class="py-0">
          <ContactInput
            v-model="profileData.contact_num"
            :required="true"
          />
        </v-col>
        <v-col class="py-0">
          <GenderInput
            v-model="profileData.gender"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0" cols="4">
          <EmailInput
            v-model="profileData.email"
            :required="true"
            :disabled="true"
          />
        </v-col>
        <v-col class="py-0" cols="8">
          <AddressInput
            v-model="profileData.address"
            :required="true"
          />
        </v-col>
      </v-row>
      <v-row class="mt-8">
        <v-col col="12" class="py-0">
          <span class="font-weight-bold">Additional Information</span>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <BioInput
            v-model="profileData.bio"
          />
        </v-col>
        <v-col class="py-0">
          <ProjectInput
            v-model="profileData.projects_in"
            :disabled="true"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <LanguageInput
            v-model="profileData.languages"
            :required="true"
          />
        </v-col>
        <v-col class="py-0">
          <WorkplaceInput
            v-model="profileData.ws_place"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <ProfessionInput
            v-model="profileData.profession"
          />
        </v-col>
        <v-col class="py-0">
          <SpeechTherapistInput
            v-model="profileData.is_speech_therapist"
            :readonly="$auth.user['custom:role'] !== 'core_team'"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6" class="py-0">
          <v-text-field
            v-model="profileData.date_joined"
            label="Date Joined"
            disabled
          />
        </v-col>
        <v-col cols="6" class="py-0">
          <v-text-field
            :value="userRole(profileData.role)"
            label="Role"
            disabled
          />
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row>
        <v-spacer />
        <v-btn color="primary" class="my-3" type="submit" :loading="isSubmitting">
          Save
        </v-btn>
      </v-row>
    </v-container>
  </v-form>
</template>
<script>
import { ROLE_OPTIONS, GENDER_OPTIONS } from './../../assets/data'
import UpdateStaff from './../../graphql/staff/UpdateStaff.graphql'
import GetSingleStaff from './../../graphql/staff/GetSingleStaff.graphql'

import NameInput from './../input/NameInput'
import AliasInput from './../input/AliasInput'
import DateOfBirthInput from './../input/DateOfBirthInput'
import ContactInput from './../input/ContactInput'
import GenderInput from './../input/GenderInput'
import EmailInput from './../input/EmailInput'
import AddressInput from './../input/AddressInput'
import BioInput from './../input/BioInput'
import ProjectInput from './../input/ProjectInput'
import LanguageInput from './../input/LanguageInput'
import WorkplaceInput from './../input/WorkplaceInput'
import ProfessionInput from './../input/ProfessionInput'
import SpeechTherapistInput from './../input/SpeechTherapistInput'

export default {
  components: {
    NameInput,
    AliasInput,
    DateOfBirthInput,
    ContactInput,
    GenderInput,
    EmailInput,
    AddressInput,
    BioInput,
    ProjectInput,
    LanguageInput,
    WorkplaceInput,
    ProfessionInput,
    SpeechTherapistInput
  },
  props: {
    profile: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      valid: true,
      isSubmitting: false,
      ROLE_OPTIONS,
      GENDER_OPTIONS,
      profileData: {
        role: this.profile.role_description.role,
        name: this.profile.name,
        nickname: this.profile.nickname,
        dob: this.profile.dob,
        contact_num: this.profile.contact_num.toString(),
        gender: this.profile.gender,
        email: this.profile.email,
        address: this.profile.address,
        bio: this.profile.bio,
        ws_place: this.profile.ws_place,
        profession: this.profile.profession,
        is_speech_therapist: this.profile.is_speech_therapist,
        date_joined: this.profile.date_joined,
        projects_in: ['None'],
        languages: this.profile.languages.map(item => item.language)
      }
    }
  },
  methods: {
    submitForm () {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        const languageChanges = this.findChangesInLanguages()
        this.$apollo.mutate({
          mutation: UpdateStaff,
          variables: {
            staff_id: this.$auth.user['custom:hasura_id'],
            address: this.profileData.address,
            bio: this.profileData.bio,
            contact_num: this.profileData.contact_num,
            dob: this.profileData.dob,
            gender: this.profileData.gender,
            is_speech_therapist: this.profileData.is_speech_therapist,
            is_active: true,
            name: this.profileData.name,
            nickname: this.profileData.nickname,
            profession: this.profileData.profession,
            role: this.profileData.role,
            ws_place: this.profileData.ws_place,
            supervisors_to_add: [],
            supervisors_to_remove: [],
            languages_to_add: languageChanges.added,
            languages_to_remove: languageChanges.removed,
            projects_to_add: [],
            projects_to_remove: [],
            updateNotification: {
              old: this.profile,
              new: {
                staff_id: this.$auth.user['custom:hasura_id'],
                address: this.profileData.address,
                bio: this.profileData.bio,
                contact_num: this.profileData.contact_num,
                dob: this.profileData.dob,
                gender: this.profileData.gender,
                is_speech_therapist: this.profileData.is_speech_therapist,
                is_active: true,
                name: this.profileData.name,
                nickname: this.profileData.nickname,
                profession: this.profileData.profession,
                role: this.profileData.role,
                ws_place: this.profileData.ws_place,
                supervisors_to_add: [],
                supervisors_to_remove: [],
                languages_to_add: languageChanges.added,
                languages_to_remove: languageChanges.removed,
                projects_to_add: [],
                projects_to_remove: []
              }
            }
          },
          update: (store, { data: { update_staffs: { returning: [updatedStaff] } } }) => {
            store.writeQuery({ query: GetSingleStaff, data: { staffs: [updatedStaff] }, variables: { id: this.$auth.user['custom:hasura_id'], isCoreTeam: true } })
          }
        }).then((data) => {
          this.$store.commit('notification/newNotification', ['Profile successfully updated', 'success'])
        }).catch((error) => {
          console.log(error.message)
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        }).then(() => {
          this.isSubmitting = false
        })
      }
    },
    findChangesInLanguages () {
      const originalArray = this.profile.languages.map(item => item.language)
      const currentArray = this.profileData.languages
      const added = []
      const removed = []
      for (const language of originalArray) {
        if (!currentArray.find(item => item === language)) {
          removed.push(language)
        }
      }
      for (const language of currentArray) {
        if (!originalArray.find(item => item === language)) {
          added.push({ language, staff_id: this.$auth.user['custom:hasura_id'] })
        }
      }
      return { added, removed }
    },
    userRole (role) {
      const filteredRoles = ROLE_OPTIONS.filter(item => item.value === role)
      if (filteredRoles.length > 0) {
        return filteredRoles[0].label
      } else {
        return 'Admin'
      }
    }
  }
}
</script>
