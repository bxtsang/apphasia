<template>
  <v-card class="pa-8">
    <span class="section-title">Add Staff</span>
    <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="submitProject">
      <v-container class="pa-0">
        <v-row>
          <v-col col="12" class="py-0">
            <span>Role</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-radio-group v-model="staffData.role" :rules="roleRules" row>
              <v-radio v-for="role in ROLE_OPTIONS" :key="role.value" :label="role.label" :value="role.value" />
            </v-radio-group>
          </v-col>
        </v-row>
        <v-row class="mt-3">
          <v-col col="12" class="py-0">
            <span>Personal Details</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-text-field
              v-model="staffData.fullname"
              :rules="fullnameRules"
              label="Full Name"
              required
            />
          </v-col>
          <v-col class="py-0">
            <v-text-field
              v-model="staffData.nickname"
              :rules="nicknameRules"
              label="Nickname / Alias"
              required
            />
          </v-col>
          <v-col class="py-0">
            <v-text-field
              v-model="staffData.nric"
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
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="staffData.dob"
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
                v-model="staffData.dob"
                :max="new Date().toISOString().substr(0, 10)"
              />
            </v-menu>
          </v-col>
          <v-col class="py-0">
            <v-text-field
              v-model="staffData.contact_number"
              :rules="contactRules"
              label="Contact"
              required
            />
          </v-col>
          <v-col class="py-0">
            <v-select
              v-model="staffData.gender"
              :items="GENDER_OPTIONS"
              :rules="genderRules"
              label="Gender"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4">
            <v-text-field
              v-model="staffData.email"
              :rules="emailRules"
              label="Email Address"
              required
            />
          </v-col>
          <v-col cols="8">
            <v-text-field
              v-model="staffData.home_address"
              :rules="addressRules"
              label="Home Address"
              required
            />
          </v-col>
        </v-row>
        <v-row class="mt-3">
          <v-col col="12" class="py-0">
            <span>Additional Information</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-text-field
              v-model="additionalData.bio"
              label="Hobbies / Interests"
            />
          </v-col>
          <v-col class="py-0">
            <v-select
              v-model="additionalData.projects"
              :items="projects"
              label="Projects Involved"
              multiple
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-select
              v-model="additionalData.languages"
              :items="languages"
              label="Languages understand and/or speak"
              multiple
            />
          </v-col>
          <v-col class="py-0">
            <v-text-field
              v-model="additionalData.work_location"
              label="Current Place of Work / Study"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-text-field
              v-model="additionalData.profession"
              label="Profession"
            />
          </v-col>
          <v-col class="py-0">
            <v-switch
              v-model="additionalData.isST"
              label="Speech Therapist?"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <v-menu
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="additionalData.date_joined"
                  label="Date Joined"
                  v-bind="attrs"
                  readonly
                  required
                  v-on="on"
                />
              </template>
              <v-date-picker
                ref="picker"
                v-model="additionalData.date_joined"
              />
            </v-menu>
          </v-col>
        </v-row>
        <v-row v-if="staffData.role != '' && staffData.role != 'core_team'" class="mt-3">
          <v-col col="12" class="py-0">
            <span>Supervisor Details</span>
          </v-col>
        </v-row>
        <v-row v-if="staffData.role != '' && staffData.role != 'core_team'">
          <v-col cols="6" class="py-0">
            <v-select
              v-model="additionalData.supervisor"
              :items="supervisors"
              label="Tag Supervisor(s)"
              multiple
            />
          </v-col>
        </v-row>
      </v-container>
      <v-btn color="primary" class="my-3" type="submit">
        Save
      </v-btn>
    </v-form>
  </v-card>
</template>
<script>
import gql from 'graphql-tag'

export default {
  data () {
    return {
      valid: true,
      ROLE_OPTIONS: [
        { label: 'Core Team', value: 'core_team' },
        { label: 'Intern', value: 'intern' },
        { label: 'Core Volunteer', value: 'core_volunteer' }
      ],
      GENDER_OPTIONS: [
        'M', 'F'
      ],
      projects: ['Project1', 'Project 2'],
      supervisors: ['person 1'],
      staffData: {
        role: '',
        fullname: '',
        nickname: '',
        nric: '',
        dob: '',
        contact_number: '',
        gender: '',
        email: '',
        home_address: ''
      },
      additionalData: {
        bio: '',
        projects: [],
        languages: [],
        work_location: '',
        profession: '',
        isST: false,
        data_joined: '',
        supervisor: []
      },
      roleRules: [v => !!v || 'Role is required'],
      fullnameRules: [v => !!v || 'Fullname is required'],
      nicknameRules: [v => !!v || 'Nickname is required'],
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
      addressRules: [v => !!v || 'Home Address is required']
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
    submitProject () {
      return this.$refs.form.validate()
    }
  }
}
</script>
