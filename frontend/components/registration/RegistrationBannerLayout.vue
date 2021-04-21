<template>
  <v-container class="pb-12">
    <v-row>
      <v-col>
        <v-img src="/asg.png" max-width="400" contain/>
      </v-col>
    </v-row>
    <v-row>
      <SuccessView v-if="submitSuccessful" />
      <v-card v-else max-width="1200" class="pt-6">
        <RegistrationBanner :resource-type="resourceType" />
        <v-container class="py-0" style="background-color: #D8E5FF;">
          <v-row class="py-0 px-12">
            <v-col class="px-6 d-flex align-center">
              <v-icon>mdi-hand-pointing-right</v-icon>
              <b class="pl-6">{{ formHeader }}</b>
            </v-col>
          </v-row>
        </v-container>

        <slot :registerSuccessful="registerSuccessful" />
      </v-card>
    </v-row>
  </v-container>
</template>
<script>
import SuccessView from './../../components/registration/SuccessView'

export default {
  layout: 'none',
  components: { SuccessView },
  props: {
    resourceType: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      submitSuccessful: false,
      title: {
        pwas: 'Aphasia SG Person with Aphasia (PWA) or Caregiver Registration Form',
        volunteers: 'Aphasia SG Volunteer Registration Form'
      },
      header: {
        pwas: 'I AM A PERSON WITH APHASIA (PWA) / CAREGIVER',
        volunteers: 'I AM A VOLUNTEER!'
      }
    }
  },
  methods: {
    registerSuccessful () {
      this.submitSuccessful = true
    }
  },
  computed: {
    formTitle () {
      return this.title[this.resourceType]
    },
    formHeader () {
      return this.header[this.resourceType]
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
