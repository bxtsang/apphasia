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
              v-model="pwaData.general_info.gender"
              :required="true"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4" class="py-0">
            <EmailInput
              v-model="pwaData.general_info.data.email"
              :required="true"
            />
          </v-col>
          <v-col cols="8" class="py-0">
            <AddressInput
              v-model="pwaData.general_info.data.address"
            />
          </v-col>
        </v-row>
        <v-row class="mt-3">
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
          <v-col :cols="contactedButNoResponse ? 12 : 6" class="py-0">
            <GeneralOptionalText
              v-model="pwaData.general_info.data.notes"
              label="Notes"
            />
          </v-col>
        </v-row>
        <v-row class="mt-3">
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
        <v-row class="mt-3">
          <v-col cols="12" class="py-0">
            <span class="font-weight-bold">Next-of-Kin Information</span>
          </v-col>
        </v-row>
        {{ pwaData }}
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
    GeneralOptionalText
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
        befrienders: { data: [] },
        comm_diff: {
          data: []
        },
        contact_status: null,
        last_contact_details: '',
        hospital: '',
        languages: { data: [] },
        media_engagement_details: '',
        media_willingness: null,
        nok: {
          data: [
            {
              contact_num: '',
              email: '',
              name: '',
              relationship: ''
            }
          ]
        },
        projects: { data: [] },
        pwa_befriender_cores: { data: [] },
        speech_therapist: '',
        stroke_date: '',
        wheelchair: null,
        general_info: {
          data: {
            address: '',
            bio: '',
            channel: '',
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
    }
  },
  computed: {
    formSubmitMethod () {
      if (this.pwa) {
        return this.editPWA
      } else {
        return this.submitStaff
      }
    },
    contactedButNoResponse () {
      return this.pwaData.contact_status === 'Contacted but no response'
    }
  },
  methods: {

  }
}
</script>
