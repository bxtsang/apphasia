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
          <v-text-field
            v-model="profileData.name"
            :rules="nameRules"
            label="Full Name"
            required
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model="profileData.nickname"
            label="Nickname / Alias"
            required
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model="profileData.nric"
            :rules="nricRules"
            label="NRIC"
            required
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <v-menu
            transition="scale-transition"
            offset-y
            :close-on-content-click="false"
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="profileData.dob"
                label="Date of Birth"
                v-bind="attrs"
                readonly
                :rules="dobRules"
                required
                v-on="on"
              />
            </template>
            <v-date-picker
              ref="picker"
              v-model="profileData.dob"
              :max="new Date().toISOString().substr(0, 10)"
            />
          </v-menu>
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model="profileData.contact_num"
            :rules="contactRules"
            label="Contact"
            required
          />
        </v-col>
        <v-col class="py-0">
          <v-select
            v-model="profileData.gender"
            :items="GENDER_OPTIONS"
            :rules="genderRules"
            label="Gender"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0" cols="4">
          <v-text-field
            v-model="profileData.email"
            :rules="emailRules"
            label="Email Address"
            required
            disabled
          />
        </v-col>
        <v-col class="py-0" cols="8">
          <v-text-field
            v-model="profileData.address"
            :rules="addressRules"
            label="Home Address"
            required
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
          <v-text-field
            v-model="profileData.bio"
            label="Hobbies / Interests"
          />
        </v-col>
        <v-col class="py-0">
          <v-select
            :value="profileData.projects_in"
            :items="projects"
            label="Projects Involved"
            multiple
            readonly
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <v-select
            v-model="profileData.languages"
            :items="languages"
            label="Languages understand and/or speak"
            :rules="languagesRules"
            multiple
          />
        </v-col>
        <v-col class="py-0">
          <v-text-field
            v-model="profileData.ws_place"
            label="Current Place of Work / Study"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <v-text-field
            v-model="profileData.profession"
            :rules="professionRules"
            label="Profession"
          />
        </v-col>
        <v-col class="py-0">
          <v-switch
            v-model="profileData.is_speech_therapist"
            label="Speech Therapist?"
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
            required
          />
        </v-col>
        <v-col cols="6" class="py-0">
          <v-text-field
            :value="ROLE_OPTIONS.filter(item => item.value === profileData.role)[0].label"
            label="Role"
            disabled
            required
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
import gql from 'graphql-tag'
import { ROLE_OPTIONS, GENDER_OPTIONS } from './../../assets/data'
import UpdateStaff from './../../graphql/staff/UpdateStaff.graphql'
import GetSingleStaff from './../../graphql/staff/GetSingleStaff.graphql'

export default {
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
      projects: ['Project1', 'Project 2', 'None'],
      profileData: {
        role: this.profile.role,
        name: this.profile.name,
        nickname: this.profile.nickname,
        nric: this.profile.nric,
        dob: this.profile.dob,
        contact_num: this.profile.contact_num,
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
      },
      roleRules: [v => !!v || 'Role is required'],
      nameRules: [v => !!v || 'Fullname is required'],
      nricRules: [
        v => !!v || 'NRIC is required',
        v => /^[STFG]\d{7}[A-Z]$/.test(v) || 'Not a valid NRIC'
      ],
      dobRules: [v => !!v || 'Date of Birth is required'],
      contactRules: [
        v => !!v || 'Contact Number is required',
        v => /(6|8|9)\d{7}/g.test(v) || 'Not a valid Contact Number'
      ],
      genderRules: [
        v => !!v || 'Gender is required'
      ],
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
      ],
      addressRules: [v => !!v || 'Home Address is required'],
      professionRules: [v => !!v || 'Profession is required'],
      languagesRules: [v => v.length > 0 || 'Language is required']
    }
  },
  apollo: {
    languages: {
      query () {
        return gql`query getLanguages {
          languages {
            language
          }
        }`
      },
      update: data => data.languages.map(item => item.language)
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
            nric: this.profileData.nric,
            profession: this.profileData.profession,
            role: this.profileData.role,
            ws_place: this.profileData.ws_place,
            supervisors_to_add: [],
            supervisors_to_remove: [],
            languages_to_add: languageChanges.added,
            languages_to_remove: languageChanges.removed
            // projects_to_add: ,
            // projects_to_remove:
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
    }
  }
}
</script>
