<template>
  <v-container class="pb-12">
    <v-row>
      <v-col class="d-flex justify-center">
        <div class="fixed-size">
          <v-img src="/asg.png" max-width="400" contain/>
        </div>
      </v-col>
    </v-row>
    <v-row class="d-flex justify-center">
      <SuccessView v-if="registerSuccessful" />
      <v-card v-else max-width="1200" width="100%">

        <v-container v-bind:class="{ hide: currStep === 1 }" class="py-0 mt-6 rounded-0" style="background-color: #D8E5FF;">
          <v-row class="py-0 px-12">
            <v-col class="px-6 d-flex align-center">
              <v-icon>mdi-hand-pointing-right</v-icon>
              <b class="pl-6">I AM A PERSON WITH APHASIA (PWA) / CAREGIVER</b>
            </v-col>
          </v-row>
        </v-container>

        <v-stepper v-model="currStep">
          <v-stepper-header v-bind:class="{ hide: currStep === 1 }" class="mt-6">

            <template v-for="n in steps">
              <v-stepper-step
                :key="`${n}-step`"
                :complete="currStep > n"
                :step="n"
                :rules="n == 1 ? [] : [() => stepParts[n - 2]]"
                editable
              >
                {{ stepperTitle(n) }}
              </v-stepper-step>
            </template>
          </v-stepper-header>
          <v-stepper-items>
            <!-- FIRST PAGE -->
            <v-stepper-content :step="1">
              <div class="d-flex align-center flex-column">
                <RegistrationBanner :resourceType="resourceType" />
                <v-btn color="primary px-12" @click="currStep = 2">Start</v-btn>
              </div>
            </v-stepper-content>

            <!-- SECOND PAGE -->
            <v-stepper-content :step="2">
              <v-form ref="registrationForm-part-1" v-model="validParts[0]" @submit.prevent="">
                <v-container fluid>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <span class="section-title">👋🏻 Let's get to know you better!</span>
                      <p class="pt-3">We need this information to better match you with other peers in the community 😁</p>
                    </v-col>
                  </v-row>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <NameInput v-model="pwa.general_info.data.name" label="*Full Name of PWA" :outlined="true"/>
                    </v-col>
                    <v-col class="px-6">
                      <DateOfBirthInput v-model="pwa.general_info.data.dob" :outlined="true" label="*Date of Birth" required/>
                    </v-col>
                  </v-row>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <GenderInput v-model="pwa.general_info.data.gender" :outlined="true" label="*Gender"/>
                    </v-col>
                    <v-col class="px-6">
                      <ContactInput
                        v-model="pwa.general_info.data.contact_num"
                        label="Contact Number (or caregiver's contact number)"
                        :outlined="true"
                        hint="^ Please provide number of caregiver if PWA is not using his/her phone"
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
                      <PWAPreferredCommInput
                        v-model="pwa.comm_mode"
                        label="*What is your preferred mode of communication"
                        :required="true"
                        :outlined="true"
                        hint="^ We will be contacting you through this mode of communication"
                      />
                    </v-col>
                    <v-col class="px-6">
                      <BioInput
                        v-model="pwa.general_info.data.bio"
                        label="Hobbies / Interests"
                        :outlined="true"/>
                    </v-col>
                  </v-row>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <ChannelInput v-model="pwa.general_info.data.channel" outlined/>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col class="d-flex justify-center"><v-btn color="primary px-12" @click="stepperClick(2)">Next</v-btn></v-col>
                  </v-row>
                </v-container>
              </v-form>
            </v-stepper-content>

            <!-- THIRD PAGE -->
            <v-stepper-content :step="3">
              <v-form ref="registrationForm-part-2" v-model="validParts[1]" @submit.prevent="">
                <v-container fluid>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <span class="section-title">👉🏻 More information about you</span>
                    </v-col>
                  </v-row>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <v-card class="card-input pa-6" outlined>
                        <span class="input-label">* Which activity will you like to attend(Can select more than one)</span>
                        <PWAProjectInterestInput
                          v-model="pwa.projects.data"
                          :required="true"
                        />
                      </v-card>
                    </v-col>
                  </v-row>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <v-card class="card-input pa-6" outlined>
                        <span class="input-label">* When did your stroke / brain injury happen?</span>
                        <PWAStrokeDateRegistrationInput
                          v-model="pwa.stroke_date"
                          :required="true"
                        />
                      </v-card>
                    </v-col>
                  </v-row>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <v-card class="card-input pa-6" outlined>
                        <span class="input-label">* What are your communication difficulties? (Can select more than one)</span>
                        <CommDiffInput v-model="pwa.comm_diff.data" :placeholderOnly="true" :required="true" />
                      </v-card>
                    </v-col>
                  </v-row>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <v-card class="card-input pa-6" outlined>
                        <span class="input-label">* What language(s) can you speak or understand? (Can select more than one)</span>
                        <LanguageInput v-model="pwa.languages.data" :placeholderOnly="true" />
                      </v-card>
                    </v-col>
                  </v-row>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <v-card class="card-input pa-6" outlined>
                        <span class="input-label">* Do you need a wheelchair?</span>
                        <WheelChairInput
                          v-model="pwa.wheelchair"
                          :required="true"
                          type="radio"
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
                  <v-row>
                    <v-col class="d-flex justify-center"><v-btn color="primary px-12" @click="stepperClick(3)">Next</v-btn></v-col>
                  </v-row>
                </v-container>
              </v-form>
            </v-stepper-content>
            <!-- FOURTH PAGE -->
            <v-stepper-content :step="4">
              <v-form ref="registrationForm-part-3" v-model="validParts[2]" @submit.prevent="">
                <v-container fluid>
                  <v-row class="px-12">
                    <v-col class="px-6">
                      <span class="section-title">👥 Caregiver or Next-of-Kin Details</span>
                      <p class="pt-3">You can include more caregiver / next-of-kin details (up to three)</p>
                    </v-col>
                  </v-row>
                  <NOKRegistrationInput v-model="pwa.nok.data" />
                  <v-row>
                    <v-col class="d-flex justify-center"><v-btn color="primary px-12" @click="stepperClick(4)">Next</v-btn></v-col>
                  </v-row>
                </v-container>
              </v-form>
            </v-stepper-content>
          </v-stepper-items>

          <!-- FIFTH PAGE -->
          <v-stepper-content :step="5">
            <v-form ref="registrationForm-part-4" v-model="validParts[3]" @submit.prevent="">
              <v-container fluid>
                <v-row class="px-12">
                  <v-col class="px-6">
                    <span class="section-title">👥 Therapist Details</span>
                  </v-col>
                </v-row>
                <NOKRegistrationInput isSpeechTherapist v-model="speech_therapist.data" />
                <v-row>
                  <v-col class="d-flex justify-center"><v-btn color="primary px-12" @click="stepperClick(5)">Next</v-btn></v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-stepper-content>

          <!-- SIXTH PAGE -->
          <v-stepper-content :step="6">
            <v-form ref="registrationForm-part-5" v-model="validParts[4]" @submit.prevent="() => submitForm(registerSuccessful)">
              <v-container fluid>
                <v-row class="px-12">
                  <v-col class="px-6">
                    <span class="section-title">✏️ Your Consent</span>
                  </v-col>
                </v-row>
                <v-row class="px-12">
                  <v-col class="px-6">
                    <v-card class="card-input pa-6" outlined>
                      <span class="input-label">Would you like to receive updates about Aphasia SG events and programmes?</span>
                      <ConsentInput v-model="pwa.general_info.data.consent" />
                    </v-card>
                  </v-col>
                </v-row>
                <v-row class="px-12">
                  <v-col class="px-6">
                    <v-card class="card-input dark pa-6" outlined>
                      <span class="input-label">Consent</span>
                      <p class="pt-3">By submitting this form, you agree to receive whatsapp messages and emails from the Aphasia SG. WhatsApp is a main mode of communication for timely dissemination of event info to participants and volunteers. Your privacy is very important to us and we do not share any information with 3rd party sites or affiliate companies.</p>
                    </v-card>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="d-flex justify-center">
                    <v-btn color="primary" class="px-12" type="submit" :loading="isSubmitting">
                      submit
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-stepper-content>
        </v-stepper>
      </v-card>
    </v-row>
  </v-container>
</template>
<script>
import PWAPreferredCommInput from './../../components/input/PWAPreferredCommInput'
import PWAProjectInterestInput from './../../components/input/PWAProjectInterestInput'
import PWAStrokeDateRegistrationInput from './../../components/input/PWAStrokeDateRegistrationInput'
import NOKRegistrationInput from './../../components/input/NOKRegistrationInput'
import RegistrationBanner from './../../components/registration/RegistrationBanner'
import RegisterPWA from './../../graphql/pwa/RegisterPWA'
import InsertNotifications from './../../graphql/notifications/InsertNotifications.graphql'

export default {
  components: {
    PWAPreferredCommInput,
    PWAProjectInterestInput,
    PWAStrokeDateRegistrationInput,
    RegistrationBanner,
    NOKRegistrationInput
  },
  layout: 'none',
  middleware: 'clearLoginCache',
  data () {
    return {
      currStep: 1,
      steps: 6,
      validParts: [true, true, true, true, true],
      stepParts: [true, true, true, true, true],
      isSubmitting: false,
      resourceType: 'pwas',
      registerSuccessful: false,
      speech_therapist: {
        data: [
          {
            contact_num: '',
            email: '',
            name: '',
            relationship: 'Speech Therapist'
          }
        ]
      },
      pwa: {
        general_info: {
          data: {
            dob: '1980-01-01'
          }
        },
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
        comm_diff: {
          data: []
        },
        languages: {
          data: []
        },
        projects: {
          data: []
        }
      }
    }
  },
  methods: {
    submitForm (registerSuccessful) {
      if (this.stepperClick(2) && this.stepperClick(3) && this.stepperClick(4) && this.stepperClick(5) && this.stepperClick(6)) {
        this.isSubmitting = true
        const _ = require('lodash')
        const newPwaData = _.cloneDeep(this.pwa)
        newPwaData.comm_diff.data = this.pwa.comm_diff.data.map((item) => { return { difficulty: item } })
        newPwaData.languages.data = this.pwa.languages.data.map((item) => { return { language: item } })
        newPwaData.projects.data = this.pwa.projects.data.map((item) => { return { project_id: item } })
        newPwaData.stroke_date = `${this.pwa.stroke_date}-01`
        newPwaData.nok.data = [...this.speech_therapist.data, ...newPwaData.nok.data]
        this.$apollo.mutate({
          mutation: RegisterPWA,
          variables: { pwa: newPwaData },
          update: (store, { data: { insert_pwas_one: newPWA } }) => {
            this.$apollo.mutate({
              mutation: InsertNotifications,
              variables: {
                insertNotifications: {
                  table: 'pwas',
                  entity_id: newPWA.id
                }
              }
            }).catch((error) => {
              console.log(error)
            })
          }
        }).then((data) => {
          this.isSubmitting = false
          this.registerSuccessful = true
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    stepperTitle (step) {
      switch (step) {
        case 2:
          return 'Your Details'
        case 3:
          return 'Additional Details'
        case 4:
          return 'NOK/Caregiver Details'
        case 5:
          return 'Therapist Details'
        case 6:
          return 'Your Consent'
        default:
          return 'Welcome'
      }
    },
    stepperClick (step) {
      switch (step) {
        case 2:
          if (this.$refs['registrationForm-part-1'].validate()) {
            this.currStep = 3
            this.stepParts[0] = true
            window.scrollTo(0, 0)
            return true
          } else {
            this.currStep = 2
            this.stepParts[0] = false
            return false
          }
        case 3:
          if (this.$refs['registrationForm-part-2'].validate()) {
            this.currStep = 4
            this.stepParts[1] = true
            window.scrollTo(0, 0)
            return true
          } else {
            this.currStep = 3
            this.stepParts[1] = false
            return false
          }
        case 4:
          if (this.$refs['registrationForm-part-3'].validate()) {
            this.currStep = 5
            this.stepParts[2] = true
            window.scrollTo(0, 0)
            return true
          } else {
            this.currStep = 4
            this.stepParts[2] = false
            return false
          }
        case 5:
          if (this.$refs['registrationForm-part-4'].validate()) {
            this.currStep = 6
            this.stepParts[3] = true
            window.scrollTo(0, 0)
            return true
          } else {
            this.currStep = 5
            this.stepParts[3] = false
            return false
          }
        case 6:
          if (this.$refs['registrationForm-part-4'].validate()) {
            this.stepParts[4] = true
            window.scrollTo(0, 0)
            return true
          } else {
            this.stepParts[4] = false
            return false
          }
        default:
          this.currStep = 2
          window.scrollTo(0, 0)
          break
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

.hide {
  display: none;
}
.v-stepper__header {
  flex-wrap: nowrap;
}
.fixed-size{
  width: 100%;
  max-width: 1200px;
}
</style>
