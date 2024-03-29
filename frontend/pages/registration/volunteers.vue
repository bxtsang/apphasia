<template>
  <RegistrationBannerLayout :resourceType="resourceType">
    <template slot-scope="{ registerSuccessful }">
      <v-form ref="registrationForm" v-model="valid" @submit.prevent="() => submitForm(registerSuccessful)">
        <v-container>
          <v-row class="px-12">
            <v-col class="px-6">
              <span class="section-title">Let's get to know you better!</span>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <NameInput v-model="volunteer.general_info.data.name" :outlined="true" label="*Full Name"/>
            </v-col>
            <v-col class="px-6">
              <AliasInput v-model="volunteer.nickname" :outlined="true"/>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <ContactInput v-model="volunteer.general_info.data.contact_num" :outlined="true" label="*Contact Number"/>
            </v-col>
            <v-col class="px-6 px-6">
              <EmailInput v-model="volunteer.general_info.data.email" :outlined="true"/>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <DateOfBirthInput v-model="volunteer.general_info.data.dob" :outlined="true"/>
            </v-col>
            <v-col class="px-6">
              <GenderInput v-model="volunteer.general_info.data.gender" :outlined="true" label="*Gender"/>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <AddressInput v-model="volunteer.general_info.data.address" :outlined="true"/>
            </v-col>
            <v-col class="px-6">
              <WorkplaceInput v-model="volunteer.ws_place" :outlined="true"/>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <BioInput v-model="volunteer.general_info.data.bio" :outlined="true"/>
            </v-col>
            <v-col class="px-6">
              <ChannelInput v-model="volunteer.general_info.data.channel" outlined/>
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
                <span class="input-label">* How will you like to volunteer with us? (Tick all that applies)</span>
                <VolunteerProjectInterestInput v-model="interested_projects" />
              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input pa-6" outlined>
                <span class="input-label">* What language(s) can you speak? (Tick all that applies)</span>
                <LanguageInput v-model="languages" :placeholderOnly="true" />
              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input pa-6" outlined>
                <span class="input-label">* What is your profession?</span>
                <MultiProfessionInput v-model="profession" />
              </v-card>
            </v-col>
          </v-row>
          <v-row class="px-12">
            <v-col class="px-6">
              <v-card class="card-input pa-6" outlined>
                <span class="input-label">Would you like to receive updates about Aphasia SG events and programmes?</span>
                <ConsentInput v-model="volunteer.general_info.data.consent" />
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
          <v-row class="px-12">
            <v-col class="px-6 d-flex justify-end">
              <v-btn color="primary" class="my-3" type="submit" :loading="isSubmitting">
                submit
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </template>
  </RegistrationBannerLayout>
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
import RegisterVol from './../../graphql/volunteer/RegisterVol.graphql'
import RegistrationBannerLayout from './../../components/registration/RegistrationBannerLayout'
import InsertNotifications from './../../graphql/notifications/InsertNotifications.graphql'

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
    MultiProfessionInput,
    RegistrationBannerLayout
  },
  layout: 'none',
  middleware: 'clearLoginCache',
  data () {
    return {
      valid: true,
      isSubmitting: false,
      resourceType: 'volunteers',
      volunteer: {
        general_info: {
          data: {}
        },
        interested_projects: {
          data: []
        },
        vol_languages: {
          data: []
        }
      },
      profession: [],
      interested_projects: [],
      languages: []
    }
  },
  methods: {
    submitForm (registerSuccessful) {
      if (this.$refs.registrationForm.validate()) {
        this.transformData()
        this.isSubmitting = true
        this.$apollo.mutate({
          mutation: RegisterVol,
          variables: {
            volunteer: this.volunteer
          },
          update: (store, { data: { insert_volunteers_one: newVol } }) => {
            this.$apollo.mutate({
              mutation: InsertNotifications,
              variables: {
                insertNotifications: {
                  table: 'volunteers',
                  entity_id: newVol.id
                }
              }
            }).catch((error) => {
              console.log(error)
            })
          }
        }).then((data) => {
          this.isSubmitting = false
          registerSuccessful()
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    transformData () {
      this.volunteer.interested_projects = { data: this.interested_projects.map((item) => { return { project_id: item } }) }
      this.volunteer.vol_languages = { data: this.languages.map((item) => { return { language: item } }) }
      this.volunteer.profession = this.profession.join(',')
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
