<template>
  <v-container class="pb-12">
    <v-row>
      <v-col>
        <v-img src="/asg.png" max-width="400" contain/>
      </v-col>
    </v-row>
    <v-row>
      <v-card>
        <v-container class="pa-12">
          <h1 class="text-center pb-3">Aphasia SG Volunteer Registration Form</h1>
          <v-row>
            <v-col cols="12" class="d-flex align-center justify-center pa-6" sm="12" md="5">
              <v-img src="/clip-social-networks.svg" contain/>
            </v-col>
            <v-col class="d-flex flex-column justify-center" cols="12" sm="12" md="7">
              <span class="section-title">
                <i class="pb-3 d-block">About Aphasia SG</i>
              </span>
              <p>Welcome to Aphasia SG, a non-profit organisation that supports persons with aphasia (PWA) and their caregivers. Our mission is to empower PWA while advocating for an aphasia-friendly, inclusive Singapore. </p>
              <p>Our flagship programmes include Chit Chat Cafe - a free pop-up cafe event for PWA to interact and have meaningful supported conversations - and the Aphasia SG Choir which rehearses weekly at a central location in Singapore. Since the start of the COVID pandemic, our community programmes have all gone virtual - we now run Chit Chat Online (every 2nd & 4th Sat morn), Aphasia SG Virtual Choir (2nd & 4th Tues evening), Aphasia Games/ Craft Night (Wed evenings) and special training workshops for caregivers!</p>
              <p>If you are a PWA, caregiver or volunteer, we invite you to join us! If you believe in our cause and wish to help out in one way or another, we will love to have you on our team. No prior knowledge or experience is necessary to be an Aphasia SG volunteer. Thank you for being a part of the aphasia movement in Singapore! 😊</p>
            </v-col>
          </v-row>
        </v-container>

        <v-container class="py-0" style="background-color: #D8E5FF;">
          <v-row class="py-0 px-12">
            <v-col class="px-6 d-flex align-center">
              <v-icon>mdi-hand-pointing-right</v-icon>
              <b class="pl-6">I AM A VOLUNTEER!</b>
            </v-col>
          </v-row>
        </v-container>

        <v-form ref="registrationForm" v-model="valid" @submit.prevent="submitForm">
          <v-container>
            <v-row class="px-12">
              <v-col class="px-6">
                <span class="section-title">Let's get to know you better!</span>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <NameInput v-model="volunteerData.name" :outlined="true"/>
              </v-col>
              <v-col class="px-6">
                <AliasInput v-model="volunteerData.nickname" :outlined="true"/>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <ContactInput v-model="volunteerData.contact_num" :outlined="true"/>
              </v-col>
              <v-col class="px-6 px-6">
                <EmailInput v-model="volunteerData.email" :outlined="true"/>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <DateOfBirthInput v-model="volunteerData.dob" :outlined="true"/>
              </v-col>
              <v-col class="px-6">
                <GenderInput v-model="volunteerData.gender" :outlined="true"/>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <AddressInput v-model="volunteerData.address" :outlined="true"/>
              </v-col>
              <v-col class="px-6">
                <WorkplaceInput v-model="volunteerData.ws_place" :outlined="true"/>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <BioInput v-model="volunteerData.bio" :outlined="true"/>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <span class="section-title">More information about you</span>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <v-card class="card-input pa-6" outlined>
                  <span class="input-label">How will you like to volunteer with us? (Tick all that applies)</span>
                  <VolunteerProjectInterestInput v-model="volunteerData.projects" />
                </v-card>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <v-card class="card-input pa-6" outlined>
                  <span class="input-label">What language(s) can you speak? (Tick all that applies)</span>
                  <LanguageInput v-model="volunteerData.languages" :placeholderOnly="true" />
                </v-card>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <v-card class="card-input pa-6" outlined>
                  <span class="input-label">What is your profession?</span>
                  <MultiProfessionInput v-model="volunteerData.profession" />
                </v-card>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <v-card class="card-input pa-6" outlined>
                  <span class="input-label">How did you hear about Aphasia SG?</span>
                  <ChannelInput v-model="volunteerData.channel" :placeholderOnly="true" />
                </v-card>
              </v-col>
            </v-row>
            <v-row class="px-12">
              <v-col class="px-6">
                <v-card class="card-input pa-6" outlined>
                  <span class="input-label">Consent</span>
                  <ConsentInput v-model="volunteerData.consent" />
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
          </v-container>
        </v-form>
      </v-card>
    </v-row>
  </v-container>
</template>
<script>
import AliasInput from './../../components/input/AliasInput.vue'
import NameInput from './../../components/input/NameInput.vue'
import ContactInput from './../../components/input/ContactInput.vue'
import EmailInput from './../../components/input/EmailInput.vue'
import DateOfBirthInput from './../../components/input/DateOfBirthInput.vue'
import GenderInput from './../../components/input/GenderInput.vue'
import AddressInput from './../../components/input/AddressInput.vue'
import WorkplaceInput from './../../components/input/WorkplaceInput.vue'
import BioInput from './../../components/input/BioInput.vue'
import LanguageInput from './../../components/input/LanguageInput.vue'
import VolunteerProjectInterestInput from './../../components/input/VolunteerProjectInterestInput'
import ChannelInput from './../../components/input/ChannelInput'
import ConsentInput from './../../components/input/ConsentInput'
import MultiProfessionInput from './../../components/input/MultiProfessionInput'

export default {
  components: {
    NameInput,
    AliasInput,
    ContactInput,
    EmailInput,
    DateOfBirthInput,
    GenderInput,
    AddressInput,
    WorkplaceInput,
    BioInput,
    VolunteerProjectInterestInput,
    LanguageInput,
    ChannelInput,
    ConsentInput,
    MultiProfessionInput
  },
  layout: 'none',
  middleware: 'clearLoginCache',
  data () {
    return {
      valid: true,
      isSubmitting: false,
      volunteerData: {
        name: '',
        nickname: '',
        contact_num: '',
        email: '',
        dob: '',
        gender: '',
        address: '',
        ws_place: '',
        bio: '',
        projects: [],
        languages: [],
        profession: [],
        channel: '',
        consent: null
      }
    }
  },
  methods: {
    submitForm () {
      if (this.$refs.registrationForm.validate()) {
        console.log('submit')
        console.log(this.volunteerData)
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
