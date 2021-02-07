<template>
  <RegistrationBanner :resourceType="resourceType">
    <template slot-scope="{ registerSuccessful }">
      <v-form ref="registrationForm" v-model="valid" @submit.prevent="() => submitForm(registerSuccessful)">
        <v-container>
          <v-row class="px-12">
            <v-col class="px-6">
              <span class="section-title">👋🏻 Let's get to know you better!</span>
              <p class="pt-3">We need this information to better match you with other peers in the community 😁</p>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <NameInput v-model="pwa.general_info.data.name" label="Full Name of PWA" :outlined="true"/>
            </v-col>
            <v-col class="px-6">
              <DateOfBirthInput v-model="pwa.general_info.data.dob" :outlined="true" required/>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <GenderInput v-model="pwa.general_info.data.gender" :outlined="true"/>
            </v-col>
            <v-col class="px-6">
              <ContactInput
                v-model="pwa.general_info.data.contact_num"
                label="Contact Number (please provide number of caregiver if PWA is not using his/her phone)"
                :outlined="true"
              />
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <EmailInput
                v-model="pwa.general_info.data.email"
                label="Email Address of PWA"
                :outlined="true"
              />
            </v-col>
            <v-col class="px-6">
              <AddressInput v-model="pwa.general_info.data.address" :outlined="true"/>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">

            </v-col>
            <v-col class="px-6">
              <BioInput
                v-model="pwa.general_info.data.bio"
                label="What are your hobbies and interests? We want to get to know you better!"
                :outlined="true"/>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <span class="section-title">👉🏻 More information about you</span>
            </v-col>
          </v-row>
          PWA project interest<br />
          StrokeData<br />
          Comm Diff<br />
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input pa-6" outlined>
                <span class="input-label">What language(s) can you speak or understand? (Can select more than one)</span>
                <LanguageInput v-model="pwa.languages" :placeholderOnly="true" />
              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input pa-6" outlined>
                <span class="input-label">Do you need a wheelchair?</span>

              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input pa-6" outlined>
                <span class="input-label">What is the name of your speech therapist?</span>
                <GeneralOptionalText
                  v-model="pwa.speech_therapist"
                  label="Name of speech therapist"
                  :placeholderOnly="true"
                />
              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input pa-6" outlined>
                <span class="input-label">Which hospital were you discharged from?</span>
                <GeneralOptionalText
                  v-model="pwa.hospital"
                  label="Name of hospital"
                  :placeholderOnly="true"
                />
              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <span class="section-title">👥 Caregiver or Next-of-Kin Details</span>
              <p class="pt-3">You can include more caregiver / next-of-kin details (up to three)</p>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <span class="section-title">✏️ Lastly...</span>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input pa-6" outlined>
                <span class="input-label">How did you hear about Aphasia SG?</span>
                <ChannelInput v-model="pwa.general_info.data.channel" :placeholderOnly="true" />
              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input pa-6" outlined>
                <span class="input-label">Consent</span>
                <ConsentInput v-model="pwa.general_info.data.consent" />
              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input dark pa-6" outlined>
                <span class="input-label">Consent</span>
                <p class="pt-3">By submitting this form, you agree to receive whatsapp messages and emails from the Aphasia SG. WhatsApp is a main mode of communication for timely dissemination of event info to participants and volunteers. Your privacy is very important to us and we do not share any information with 3rd party sites or affiliate companies. You have the option to opt-out at any time.</p>
              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6 d-flex justify-end">
              <v-btn color="primary" class="my-3" type="submit" :loading="isSubmitting">
                submit
              </v-btn>
            </v-col>
          </v-row>
          <pre>{{ pwa }}</pre>
        </v-container>
      </v-form>
    </template>
  </RegistrationBanner>
</template>
<script>

import NameInput from './../../components/input/NameInput.vue'
import DateOfBirthInput from './../../components/input/DateOfBirthInput.vue'
import GenderInput from './../../components/input/GenderInput.vue'
import ContactInput from './../../components/input/ContactInput.vue'
import EmailInput from './../../components/input/EmailInput.vue'
import AddressInput from './../../components/input/AddressInput.vue'
import BioInput from './../../components/input/BioInput.vue'

import LanguageInput from './../../components/input/LanguageInput.vue'
import GeneralOptionalText from './../../components/input/GeneralOptionalText'
import ChannelInput from './../../components/input/ChannelInput'
import ConsentInput from './../../components/input/ConsentInput'
import RegistrationBanner from './../../components/registration/RegistrationBanner'

export default {
  components: {
    NameInput,
    DateOfBirthInput,
    GenderInput,
    ContactInput,
    EmailInput,
    AddressInput,
    BioInput,
    LanguageInput,
    GeneralOptionalText,
    ChannelInput,
    ConsentInput,
    RegistrationBanner
  },
  layout: 'none',
  middleware: 'clearLoginCache',
  data () {
    return {
      valid: true,
      isSubmitting: false,
      resourceType: 'pwas',
      pwa: {
        general_info: {
          data: {}
        },
        languages: []
      }
    }
  },
  methods: {
    submitForm (registerSuccessful) {
      if (this.$refs.registrationForm.validate()) {
        // this.transformData()
        // this.isSubmitting = true
        // this.$apollo.mutate({
        //   mutation: RegisterVol,
        //   variables: {
        //     volunteer: this.volunteer
        //   }
        // }).then((data) => {
        //   this.isSubmitting = false
        //   this.$store.commit('notification/newNotification', ['Your registration has been created', 'success'])
        //   registerSuccessful()
        // }).catch((error) => {
        //   this.isSubmitting = false
        //   this.$store.commit('notification/newNotification', [error.message, 'error'])
        // })
      }
    }
  }
}
</script>
<style scoped>
.v-card.card-input {
  border-color: rgba(0, 0, 0, 0.38);
}

.v-card.card-input .input-label {
  font-size: 1rem;
  font-weight: bold;
  color: #757575;
}

.v-card .card-input.dark {
  background-color: #F8F8F8;
  border: none;
}

.v-card .card-input.dark > * {
  color: black;
}

</style>
