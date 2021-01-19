<template>
  <v-card class="pa-8">
    <span v-if="staff" class="section-title">Edit Staff</span>
    <span v-else class="section-title">Add Staff</span>
    <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="formSubmitMethod">
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
          <v-col class="py-0" cols="4">
            <v-text-field
              v-model="staffData.email"
              :rules="emailRules"
              label="Email Address"
              required
            />
          </v-col>
          <v-col class="py-0" cols="8">
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
              :rules="languagesRules"
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
        {{ staff ? 'Edit' : 'Save' }}
      </v-btn>
    </v-form>
  </v-card>
</template>
<script>
import gql from 'graphql-tag'
import GetAllStaff from './../../graphql/staff/GetAllStaff.graphql'
import CreateUser from './../../graphql/staff/CreateUser.graphql'
import CreateCognitoUser from './../../graphql/staff/CreateCognitoUser.graphql'
import { ROLE_OPTIONS, GENDER_OPTIONS } from './../../assets/data'

export default {
  props: {
    staff: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      valid: true,
      ROLE_OPTIONS,
      GENDER_OPTIONS,
      projects: ['Project1', 'Project 2'],
      staffData: {
        role: this.staff ? this.staff.role : '',
        name: this.staff ? this.staff.name : '',
        nickname: this.staff ? this.staff.nickname : '',
        nric: this.staff ? this.staff.nric : '',
        dob: this.staff ? this.staff.dob : '',
        contact_num: this.staff ? this.staff.contact_num : '',
        gender: this.staff ? this.staff.gender : '',
        email: this.staff ? this.staff.email : '',
        address: this.staff ? this.staff.address : '',
        bio: this.staff ? this.staff.bio : '',
        ws_place: this.staff ? this.staff.ws_place : '',
        profession: this.staff ? this.staff.profession : '',
        is_speech_therapist: this.staff ? this.staff.is_speech_therapist : false,
        date_joined: this.staff ? this.staff.date_joined : '',
        projects_in: [],
        languages: this.staff ? this.staff.languages.map(item => item.language) : [],
        supervisors: this.staff ? this.staff.supervisors.map(item => item.supervisor_id) : []
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
      dateJoinedRules: [v => !!v || 'Date Joined is required'],
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
  computed: {
    formSubmitMethod () {
      if (this.staff) {
        return this.editStaff
      } else {
        return this.submitStaff
      }
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
            ws_place: this.staffData.ws_place,
            languages: { data: this.staffData.languages.map((item) => { return { language: item } }) },
            supervisors: { data: this.staffData.supervisors.map((item) => { return { supervisor_id: item } }) }
            // projects_in: this.staffData.projects_in,
          },
          update: (store, { data: { insert_staffs_one: newStaff } }) => {
            const data = store.readQuery({ query: GetAllStaff })
            data.staffs.push(newStaff)
            store.writeQuery({ query: GetAllStaff, data })
            this.$apollo.mutate({
              mutation: CreateCognitoUser,
              variables: {
                email: newStaff.email,
                password: 'aphasiapassword',
                role: newStaff.role,
                user_id: newStaff.id
              },
              update: (store, response) => {
                // Success
              }
            }).catch((error) => {
              console.log(error)
            })
          }
        }).then((data) => {
          this.staffData = {
            role: 'core_team',
            name: '',
            nickname: '',
            nric: '',
            dob: '',
            contact_num: '',
            gender: '',
            email: '',
            address: '',
            bio: '',
            projects_in: [],
            languages: [],
            ws_place: '',
            profession: '',
            is_speech_therapist: false,
            date_joined: '',
            supervisors: []
          }
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['User successfully created', 'success'])
        }).catch((error) => {
          console.log(error.message)
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    editStaff () {
      // Change existing
      console.log('hi')
      console.log(this.staff.id)
      console.log(this.staff.supervisors)
      // update hasura
      // update GetSingleStaff
      // update GetAllStaff
    }
  }
}
</script>
