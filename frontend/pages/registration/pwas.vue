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
              <NameInput v-model="pwa.general_info.data.name" :label="'Full Name of PWA'" :outlined="true"/>
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
                :label="'Contact Number (please provide number of caregiver if PWA is not using his/her phone)'"
                :outlined="true"
              />
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <EmailInput
                v-model="pwa.general_info.data.email"
                :label="'Email Address of PWA'"
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

            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <span class="section-title">👉🏻 More information about you</span>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <span class="section-title">👥 Caregiver or Next-of-Kin Details</span>
              <p class="pt-3">You can include more caregiver / next-of-kin details (up to three)</p>
            </v-col>
          </v-row>
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
// import WorkplaceInput from './../../components/input/WorkplaceInput.vue'
// import BioInput from './../../components/input/BioInput.vue'
// import LanguageInput from './../../components/input/LanguageInput.vue'
// import VolunteerProjectInterestInput from './../../components/input/VolunteerProjectInterestInput'
// import ChannelInput from './../../components/input/ChannelInput'
// import ConsentInput from './../../components/input/ConsentInput'
// import MultiProfessionInput from './../../components/input/MultiProfessionInput'
import RegistrationBanner from './../../components/registration/RegistrationBanner'

export default {
  components: {
    NameInput,
    DateOfBirthInput,
    GenderInput,
    ContactInput,
    EmailInput,
    AddressInput,
    // WorkplaceInput,
    // BioInput,
    // VolunteerProjectInterestInput,
    // LanguageInput,
    // ChannelInput,
    // ConsentInput,
    // MultiProfessionInput,
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
        }
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
