<template>
  <v-card class="pa-8">
    <span v-if="pwa" class="section-title">Edit PWA</span>
    <span v-else class="section-title">Add PWA</span>
    <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="formSubmitMethod">
      <v-container class="pa-0">
        <v-row class="mt-3">
          <v-col cols="12" class="py-0">
            <span class="font-weight-bold">Personal Details</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <NameInput
              v-model="pwaData.general_info.data.name"
              :required="true"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4" class="py-0">
            <DateOfBirthInput
              v-model="pwaData.general_info.data.dob"
              :required="true"
            />
          </v-col>
          <v-col cols="4" class="py-0">
            <ContactInput
              v-model="pwaData.general_info.data.contact_num"
              :required="true"
            />
          </v-col>
          <v-col cols="4" class="py-0">
            <GenderInput
              v-model="pwaData.general_info.data.gender"
              :required="true"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4" class="py-0">
            <EmailInput
              v-model="pwaData.general_info.data.email"
            />
          </v-col>
          <v-col cols="8" class="py-0">
            <AddressInput
              v-model="pwaData.general_info.data.address"
            />
          </v-col>
        </v-row>
        <v-row class="mt-8">
          <v-col cols="12" class="py-0">
            <span class="font-weight-bold">Additional Information</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <BioInput
              v-model="pwaData.general_info.data.bio"
            />
          </v-col>
          <v-col cols="6" class="py-0">
            <WheelChairInput
              v-model="pwaData.wheelchair"
              :required="true"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <ProjectInput
              v-model="pwaData.projects.data"
              :required="true"
            />
          </v-col>
          <v-col cols="6" class="py-0">
            <CommDiffInput
              v-model="pwaData.comm_diff.data"
              :required="true"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <LanguageInput
              v-model="pwaData.languages.data"
              :required="true"
            />
          </v-col>
          <v-col cols="6" class="py-0">
            <StrokeDateInput
              v-model="pwaData.stroke_date"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <ChannelInput
              v-model="pwaData.general_info.data.channel"
            />
          </v-col>
          <v-col cols="6" class="py-0">
            <ConsentInput
              v-model="pwaData.general_info.data.consent"
              :required="true"
              inputType="select"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <MediaWillingnessInput
              v-model="pwaData.media_willingness"
            />
          </v-col>
          <v-col cols="6" class="py-0">
            <GeneralOptionalText
              v-model="pwaData.media_engagement_details"
              label="Participated in any media project?"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <PWAContactStatusInput
              v-model="pwaData.contact_status"
            />
          </v-col>
          <v-col v-if="contactedButNoResponse" cols="6" class="py-0">
            <GeneralOptionalText
              v-model="pwaData.last_contact_details"
              label="Last Contact Details"
            />
          </v-col>
          <v-col cols="6" class="py-0">
            <PWAPreferredCommInput
              v-model="pwaData.comm_mode"
            />
          </v-col>
          <v-col cols="6" class="py-0">
            <GeneralOptionalText
              v-model="pwaData.general_info.data.notes"
              label="Notes"
            />
          </v-col>
        </v-row>
        <v-row class="mt-8">
          <v-col cols="12" class="py-0">
            <span class="font-weight-bold">Speech Therapist Details</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6" class="py-0">
            <GeneralOptionalText
              v-model="pwaData.speech_therapist"
              label="Name of Speech Therapist"
            />
          </v-col>
          <v-col cols="6" class="py-0">
            <GeneralOptionalText
              v-model="pwaData.hospital"
              label="Discharge from which hospital?"
            />
          </v-col>
        </v-row>
        <v-row class="mt-8">
          <v-col class="py-0">
            <NOKInput
              v-model="pwaData.nok.data"
            />
          </v-col>
        </v-row>
        <v-row>
          <DeleteResourceModal
            v-if="$auth.user['custom:role'] === 'core_team' && pwa"
            :resource="pwa"
            :resourceType="'pwas'"
            @deleteSuccess="$emit('closeForm')"
          />
          <v-spacer />
          <v-btn color="primary" class="my-3" type="submit" :loading="isSubmitting">
            {{ pwa ? 'Save' : 'Add' }}
          </v-btn>
        </v-row>
      </v-container>
    </v-form>
  </v-card>
</template>
<script>
import NameInput from './../input/NameInput'
import DateOfBirthInput from './../input/DateOfBirthInput'
import ContactInput from './../input/ContactInput'
import GenderInput from './../input/GenderInput'
import EmailInput from './../input/EmailInput'
import AddressInput from './../input/AddressInput'
import BioInput from './../input/BioInput'
import WheelChairInput from './../input/WheelChairInput.vue'
import ProjectInput from './../input/ProjectInput'
import CommDiffInput from './../input/CommDiffInput'
import LanguageInput from './../input/LanguageInput'
import StrokeDateInput from './../input/StrokeDateInput'
import ChannelInput from './../input/ChannelInput'
import ConsentInput from './../input/ConsentInput'
import MediaWillingnessInput from './../input/MediaWillingnessInput'
import PWAContactStatusInput from './../input/PWAContactStatusInput'
import GeneralOptionalText from './../input/GeneralOptionalText'
import NOKInput from './../input/NOKInput'
import PWAPreferredCommInput from './../input/PWAPreferredCommInput'
import CreatePWA from './../../graphql/pwa/CreatePWA.graphql'
import GetAllPWA from './../../graphql/pwa/GetAllPWA.graphql'
import GetSinglePWA from './../../graphql/pwa/GetSinglePWA.graphql'
import UpdatePWA from './../../graphql/pwa/UpdatePWA.graphql'
const _ = require('lodash')

export default {
  components: {
    NameInput,
    DateOfBirthInput,
    ContactInput,
    GenderInput,
    EmailInput,
    AddressInput,
    BioInput,
    WheelChairInput,
    ProjectInput,
    CommDiffInput,
    LanguageInput,
    StrokeDateInput,
    ChannelInput,
    ConsentInput,
    MediaWillingnessInput,
    PWAContactStatusInput,
    GeneralOptionalText,
    NOKInput,
    PWAPreferredCommInput
  },
  props: {
    pwa: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      valid: true,
      isSubmitting: false,
      pwaData: {
        comm_diff: {
          data: this.pwa ? this.pwa.comm_diff.map(item => item.difficulty) : []
        },
        comm_mode: this.pwa ? this.pwa.comm_mode : '',
        contact_status: this.pwa ? this.pwa.contact_status : 'Not Contacted',
        last_contact_details: this.pwa ? this.pwa.last_contact_details : '',
        hospital: this.pwa ? this.pwa.hospital : '',
        languages: { data: this.pwa ? this.pwa.languages.map(item => item.language) : [] },
        media_engagement_details: this.pwa ? this.pwa.media_engagement_details : '',
        media_willingness: this.pwa ? this.pwa.media_willingness : null,
        nok: { data: this.pwa ? _.cloneDeep(this.pwa.nok) : [] },
        projects: { data: this.pwa ? this.pwa.projects.map(item => item.project.id) : [] },
        speech_therapist: this.pwa ? this.pwa.speech_therapist : null,
        stroke_date: this.pwa ? this.pwa.stroke_date : null,
        wheelchair: this.pwa ? this.pwa.wheelchair : null,
        general_info: {
          data: {
            address: this.pwa ? this.pwa.general_info.address : '',
            bio: this.pwa ? this.pwa.general_info.bio : '',
            channel: this.pwa ? this.pwa.general_info.channel : null,
            consent: this.pwa ? this.pwa.general_info.consent : null,
            contact_num: this.pwa ? this.pwa.general_info.contact_num.toString() : '',
            dob: this.pwa ? this.pwa.general_info.dob : '',
            email: this.pwa ? this.pwa.general_info.email : '',
            gender: this.pwa ? this.pwa.general_info.gender : '',
            name: this.pwa ? this.pwa.general_info.name : '',
            notes: this.pwa ? this.pwa.general_info.notes : ''
          }
        }
      }
    }
  },
  computed: {
    formSubmitMethod () {
      if (this.pwa) {
        return this.editPWA
      } else {
        return this.submitPWA
      }
    },
    contactedButNoResponse () {
      return this.pwaData.contact_status === 'Contacted but no response'
    }
  },
  methods: {
    submitPWA () {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        const _ = require('lodash')
        const newPwaData = _.cloneDeep(this.pwaData)
        newPwaData.comm_diff.data = this.pwaData.comm_diff.data.map((item) => { return { difficulty: item } })
        newPwaData.languages.data = this.pwaData.languages.data.map((item) => { return { language: item } })
        newPwaData.projects.data = this.pwaData.projects.data.map((item) => { return { project_id: item } })
        this.$apollo.mutate({
          mutation: CreatePWA,
          variables: { pwa: newPwaData },
          update: (store, { data: { insert_pwas_one: newPWA } }) => {
            const data = store.readQuery({ query: GetAllPWA })
            data.pwas.push(newPWA)
            store.writeQuery({ query: GetAllPWA, data })
          }
        }).then((data) => {
          this.isSubmitting = false
          this.pwaData = {
            comm_diff: {
              data: []
            },
            contact_status: 'Not Contacted',
            last_contact_details: '',
            hospital: '',
            languages: { data: [] },
            media_engagement_details: '',
            media_willingness: null,
            nok: { data: [] },
            projects: { data: [] },
            speech_therapist: '',
            stroke_date: null,
            wheelchair: null,
            general_info: {
              data: {
                address: '',
                bio: '',
                channel: null,
                consent: null,
                contact_num: '',
                dob: '',
                email: '',
                gender: '',
                name: '',
                notes: ''
              }
            }
          }
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['PWA successfully created', 'success'])
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    editPWA () {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        const constructedData = this.constructUpdateVariables(this.pwaData)
        this.$apollo.mutate({
          mutation: UpdatePWA,
          variables: {
            id: this.pwa.id,
            general_info: constructedData.generalInfo.data,
            pwa: { id: this.pwa.id, ...constructedData.updatedPwaData }
          },
          update: (store, { data: { insert_pwas_one: updatedPWA } }) => {
            store.writeQuery({ query: GetSinglePWA, data: { pwas_by_pk: updatedPWA }, variables: { id: this.pwa.id } })
            try {
              const dataAll = store.readQuery({ query: GetAllPWA })
              dataAll.pwas = dataAll.pwas.filter(item => item.id !== this.pwa.id)
              dataAll.pwas.push(updatedPWA)
              store.writeQuery({ query: GetAllPWA, dataAll })
            } catch (error) {
              // GetAllPWA Query not in store
            }
          }
        }).then((data) => {
          this.isSubmitting = false
          this.$emit('closeForm')
          this.$store.commit('notification/newNotification', ['PWA successfully updated', 'success'])
        }).catch((error) => {
          this.isSubmitting = false
          console.log(error.message)
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    constructUpdateVariables (pwaData) {
      const _ = require('lodash')
      const updatedPwaData = _.cloneDeep(pwaData)
      updatedPwaData.comm_diff.data = pwaData.comm_diff.data.map((item) => { return { difficulty: item } })
      updatedPwaData.languages.data = pwaData.languages.data.map((item) => { return { language: item } })
      updatedPwaData.projects.data = pwaData.projects.data.map((item) => { return { project_id: item } })
      updatedPwaData.nok.data = updatedPwaData.nok.data.map((item) => {
        return {
          contact_num: item.contact_num,
          email: item.email,
          name: item.name,
          relationship: item.relationship
        }
      })

      delete updatedPwaData.general_info

      const generalInfo = _.cloneDeep(pwaData.general_info)

      return { updatedPwaData, generalInfo }
    }
  }
}
</script>
