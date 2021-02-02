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
            <RoleInput
              v-model="staffData.role"
            />
          </v-col>
        </v-row>
        <v-row class="mt-3">
          <v-col col="12" class="py-0">
            <span>Personal Details</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <NameInput
              v-model="staffData.name"
              :required="true"
            />
          </v-col>
          <v-col class="py-0">
            <AliasInput
              v-model="staffData.nickname"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <DateOfBirthInput
              v-model="staffData.dob"
              :required="true"
            />
          </v-col>
          <v-col class="py-0">
            <ContactInput
              v-model="staffData.contact_num"
              required="true"
            />
          </v-col>
          <v-col class="py-0">
            <GenderInput
              v-model="staffData.gender"
            />
          </v-col>
        </v-row>
        <v-row>
          <!--  hide from edit -->
          <v-col v-if="!staff" class="py-0" cols="4">
            <EmailInput
              v-model="staffData.email"
              :required="true"
            />
          </v-col>
          <v-col class="py-0" cols="8">
            <AddressInput
              v-model="staffData.address"
              :required="true"
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
            <BioInput
              v-model="staffData.bio"
            />
          </v-col>
          <v-col class="py-0">
            <ProjectInput
              v-model="staffData.projects_in"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <LanguageInput
              v-model="staffData.languages"
              :required="true"
            />
          </v-col>
          <v-col class="py-0">
            <WorkplaceInput
              v-model="staffData.ws_place"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <ProfessionInput
              v-model="staffData.profession"
            />
          </v-col>
          <v-col class="py-0">
            <SpeechTherapistInput
              v-model="staffData.is_speech_therapist"
            />
          </v-col>
        </v-row>
        <v-row v-if="!staff">
          <v-col cols="6" class="py-0">
            <DateJoinedInput
              v-model="staffData.date_joined"
              :required="true"
            />
          </v-col>
        </v-row>
        <v-row v-if="staffData.role != '' && staffData.role != 'core_team'" class="mt-3">
          <v-col col="12" class="py-0">
            <span>Supervisor Details</span>
          </v-col>
        </v-row>
        <v-row v-if="staffData.role != '' && staffData.role != 'core_team'">
          <v-col cols="6" class="py-0">
            <SupervisorInput
              v-model="staffData.supervisors"
            />
          </v-col>
        </v-row>
      </v-container>
      <v-container>
        <v-row>
          <v-btn v-if="staff" color="error" class="my-3" @click="() => {editStaff(true)}">
            Archive
          </v-btn>
          <v-spacer />
          <v-btn color="primary" class="my-3" type="submit" :loading="isSubmitting">
            {{ staff ? 'Edit' : 'Save' }}
          </v-btn>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
</template>
<script>
import GetAllStaff from './../../graphql/staff/GetAllStaff.graphql'
import CreateUser from './../../graphql/staff/CreateUser.graphql'
import CreateCognitoUser from './../../graphql/staff/CreateCognitoUser.graphql'
import UpdateCognitoUser from './../../graphql/staff/UpdateCognitoUser.graphql'
import UpdateStaff from './../../graphql/staff/UpdateStaff.graphql'
import GetSingleStaff from './../../graphql/staff/GetSingleStaff.graphql'

import RoleInput from './../input/RoleInput'
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
import SupervisorInput from './../input/SupervisorInput'

export default {
  components: {
    RoleInput,
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
    SpeechTherapistInput,
    SupervisorInput
  },
  props: {
    staff: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      valid: true,
      isSubmitting: false,
      staffData: {
        role: this.staff ? this.staff.role : '',
        name: this.staff ? `${this.staff.name}` : '',
        nickname: this.staff ? this.staff.nickname : '',
        dob: this.staff ? this.staff.dob : '',
        contact_num: this.staff ? this.staff.contact_num.toString() : '',
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
        supervisors: this.staff ? this.staff.supervisors.map(item => item.supervisor.id) : [],
        is_active: this.staff ? this.staff.is_active : true
      }
    }
  },
  computed: {
    formSubmitMethod () {
      if (this.staff) {
        return () => { this.editStaff(false) }
      } else {
        return this.submitStaff
      }
    }
  },
  methods: {
    submitStaff () {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
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
            profession: this.staffData.profession,
            role: this.staffData.role,
            ws_place: this.staffData.ws_place,
            languages: { data: this.staffData.languages.map((item) => { return { language: item } }) },
            supervisors: { data: this.staffData.supervisors.map((item) => { return { supervisor_id: item } }) }
            // projects_in: this.staffData.projects_in,
          },
          update: (store, { data: { insert_staffs_one: newStaff } }) => {
            const data = store.readQuery({ query: GetAllStaff, variables: { isCoreTeam: this.$auth.user['custom:role'] === 'core_team' } })
            data.staffs.push(newStaff)
            store.writeQuery({ query: GetAllStaff, data, variables: { isCoreTeam: this.$auth.user['custom:role'] === 'core_team' } })
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
          this.isSubmitting = false
          this.staffData = {
            role: 'core_team',
            name: '',
            nickname: '',
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
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    editStaff (archive) {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        const languageChanges = this.findChangesInLanguages()
        const supervisorChanges = this.findChangesInSupervisor()
        this.$apollo.mutate({
          mutation: UpdateStaff,
          variables: {
            staff_id: this.staff.id,
            address: this.staffData.address,
            bio: this.staffData.bio,
            contact_num: this.staffData.contact_num,
            dob: this.staffData.dob,
            gender: this.staffData.gender,
            is_speech_therapist: this.staffData.is_speech_therapist,
            is_active: !archive,
            name: this.staffData.name,
            nickname: this.staffData.nickname,
            profession: this.staffData.profession,
            role: this.staffData.role,
            ws_place: this.staffData.ws_place,
            supervisors_to_add: supervisorChanges.added,
            supervisors_to_remove: supervisorChanges.removed,
            languages_to_add: languageChanges.added,
            languages_to_remove: languageChanges.removed
            // projects_to_add: ,
            // projects_to_remove:
          },
          update: (store, { data: { update_staffs: { returning: [updatedStaff] } } }) => {
            store.writeQuery({ query: GetSingleStaff, data: { staffs: [updatedStaff] }, variables: { id: this.staff.id, isCoreTeam: this.$auth.user['custom:role'] === 'core_team' } })
            try {
              const dataAll = store.readQuery({ query: GetAllStaff, variables: { isCoreTeam: this.$auth.user['custom:role'] === 'core_team' } })
              dataAll.staffs = dataAll.staffs.filter(item => item.id !== this.staff.id)
              dataAll.staffs.push(updatedStaff)
              store.writeQuery({ query: GetAllStaff, dataAll, variables: { isCoreTeam: this.$auth.user['custom:role'] === 'core_team' } })
            } catch (error) {
              // GetAllStaff Query not in store
            }

            // Call UpdateCognitoUser action
            if (this.staffData.role !== this.staff.role) {
              this.$apollo.mutate({
                mutation: UpdateCognitoUser,
                variables: {
                  email: this.staff.email,
                  user_id: this.staff.id,
                  current_role: this.staff.role,
                  new_role: this.staffData.role
                },
                update: (store, response) => {
                  // Success
                }
              }).catch((error) => {
                console.log(error)
              })
            }
          }
        }).then((data) => {
          this.isSubmitting = false
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['User successfully updated', 'success'])
        }).catch((error) => {
          this.isSubmitting = false
          console.log(error.message)
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    findChangesInLanguages () {
      const originalArray = this.staff.languages.map(item => item.language)
      const currentArray = this.staffData.languages
      const added = []
      const removed = []
      for (const language of originalArray) {
        if (!currentArray.find(item => item === language)) {
          removed.push(language)
        }
      }
      for (const language of currentArray) {
        if (!originalArray.find(item => item === language)) {
          added.push({ language, staff_id: this.staff.id })
        }
      }
      return { added, removed }
    },
    findChangesInSupervisor () {
      const originalArray = this.staff.supervisors.map(item => item.supervisor.id)
      const currentArray = this.staffData.supervisors
      const added = []
      const removed = []
      for (const supervisor of originalArray) {
        if (!currentArray.find(item => item === supervisor)) {
          removed.push(supervisor)
        }
      }
      for (const supervisor of currentArray) {
        if (!originalArray.find(item => item === supervisor)) {
          added.push({ supervisor_id: supervisor, staff_id: this.staff.id })
        }
      }
      return { added, removed }
    }
  }
}
</script>
