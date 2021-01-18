<template>
  <v-card class="pa-8">
    <span class="section-title">Add Staff</span>
    <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="submitStaff">
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
              v-model="staffData.name"
              :rules="nameRules"
              label="Full Name"
              required
            />
          </v-col>
          <v-col class="py-0">
            <v-text-field
              v-model="staffData.nickname"
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
              :close-on-content-click="false"
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
              v-model="staffData.contact_num"
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
              v-model="staffData.address"
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
              v-model="staffData.bio"
              label="Hobbies / Interests"
            />
          </v-col>
          <v-col class="py-0">
            <v-select
              v-model="staffData.projects_in"
              :items="projects"
              label="Projects Involved"
              multiple
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-select
              v-model="staffData.languages"
              :items="languages"
              label="Languages understand and/or speak"
              multiple
            />
          </v-col>
          <v-col class="py-0">
            <v-text-field
              v-model="staffData.ws_place"
              label="Current Place of Work / Study"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-text-field
              v-model="staffData.profession"
              :rules="professionRules"
              label="Profession"
            />
          </v-col>
          <v-col class="py-0">
            <v-switch
              v-model="staffData.is_speech_therapist"
              label="Speech Therapist?"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <v-menu
              transition="scale-transition"
              offset-y
              :close-on-content-click="false"
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="staffData.date_joined"
                  label="Date Joined"
                  v-bind="attrs"
                  readonly
                  required
                  :rules="dateJoinedRules"
                  v-on="on"
                />
              </template>
              <v-date-picker
                ref="picker"
                v-model="staffData.date_joined"
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
              v-model="staffData.supervisors"
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
import GetAllStaff from './../../graphql/staff/GetAllStaff.graphql'
import CreateUser from './../../graphql/staff/CreateUser.graphql'

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
        role: 'core_team',
        name: 'Arix Phua Si Yu',
        nickname: 'Arix',
        nric: 'S9625151C',
        dob: '1996-08-18',
        contact_num: '91714378',
        gender: 'M',
        email: 'arixgg@gmail.com',
        address: 'Blk 1 Beach Road',
        bio: '',
        projects_in: [],
        languages: ['English'],
        ws_place: 'SMU',
        profession: 'Student',
        is_speech_therapist: false,
        date_joined: '2021-01-10',
        supervisors: []
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
      dateJoinedRules: [v => !!v || 'Date Joined is required']
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
    },
    supervisors: {
      query () {
        return gql`query getCoreTeamMembers {
          staffs(where: {role: {_eq: core_team}}){
            id
            name
          }
        }`
      },
      update: data => data.staffs.map((item) => { return { text: item.name, value: item.id } })
    }
  },
  methods: {
    submitStaff () {
      if (this.$refs.form.validate()) {
        this.$apollo.mutate({
          mutation: CreateUser,
          variables: {
            address: this.staffData.address,
            bio: this.staffData.bio,
            contact_num: this.staffData.contact_num,
            date_joined: this.staffData.date_joined,
            dob: this.staffData.dob,
            email: this.staffData.email,
            gender: this.staffData.gender,
            is_speech_therapist: this.staffData.is_speech_therapist,
            name: this.staffData.name,
            nickname: this.staffData.nickname,
            nric: this.staffData.nric,
            profession: this.staffData.profession,
            role: this.staffData.role,
            ws_place: this.staffData.ws_place
            // languages: this.staffData.languages.map((item) => { return { language: item } }),
            // supervisors: this.staffData.supervisors,
            // projects_in: this.staffData.projects_in,
          },
          update: (store, { data: { insert_staffs_one: newStaff } }) => {
            const data = store.readQuery({ query: GetAllStaff })
            data.staffs.push(newStaff)
            store.writeQuery({ query: GetAllStaff, data })
            console.log('create cognito account')
          }
        }).then((data) => {
          this.$emit('closeForm')
        }).catch((error) => {
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    }
  }
}
</script>
