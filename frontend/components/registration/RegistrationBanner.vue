<template>
  <v-container>
    <h1 class="text-center pb-3">
      {{ formTitle }}
    </h1>
    <v-row>
      <v-col cols="12" class="d-flex align-center justify-center pa-6" sm="12" md="5">
        <v-img src="/clip-social-networks.svg" contain/>
      </v-col>
      <v-col class="d-flex flex-column justify-center" cols="12" sm="12" md="7">
        <span class="section-title">
          <i class="pb-3 d-block">About Aphasia SG</i>
        </span>
        <p>Welcome to Aphasia SG, a non-profit organisation that supports persons with aphasia (PWA) and their caregivers. Our mission is to empower PWA while advocating for an aphasia-friendly, inclusive Singapore. </p>
        <p>Our flagship programmes include Chit Chat Cafe - a free pop-up cafe event for PWA to interact and have meaningful supported conversations - and the Aphasia SG Choir which rehearses weekly at a central location in Singapore. Since the start of the COVID pandemic, our community programmes have all gone virtual - we now run Chit Chat Online (every 2nd & 4th Sat mornings), Aphasia SG Virtual Choir (2nd & 4th Tues evenings), Aphasia Games/ Craft Night (Wed evenings) and special training workshops for caregivers!</p>
        <p>
          <span v-if="resourceType === 'pwas'">If you are a PWA, or a caregiver for a PWA, we invite you to join us by registering!</span>
          <span v-if="resourceType === 'volunteers'">If you believe in our cause and wish to help out in one way or another, we will love to have you on our team. No prior knowledge or experience is necessary to be an Aphasia SG volunteer. Join us by registering here!</span>
        </p>
        <p>Thank you for being a part of the aphasia movement in Singapore! 😊</p>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>

export default {
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
