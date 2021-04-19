<template>
  <div>

    <div v-for="(nok, index) in data" :key="index">
      <v-row class="mt-3 px-12" >
        <v-col cols="12" class="py-0 d-flex px-6">
          <span class="font-weight-bold">({{ index + 1 }}) {{ isSpeechTherapist ? 'Speech Therapist' : 'Caregiver' }} Information</span>
          <v-spacer />
          <v-btn color="error" depressed fab small @click="() => { removeNOK(index) }"><v-icon>mdi-close</v-icon></v-btn>
        </v-col>
      </v-row>
      <v-row class="mt-3 px-12">
        <v-col cols="6" class="py-0 pl-6">
          <v-text-field
            v-model="data[index].name"
            :label="`Full Name of ${ isSpeechTherapist ? 'Speech Therapist' : 'caregiver / next-of-kin'}`"
            outlined
          />
        </v-col>
        <v-col cols="6" class="py-0 pr-6">
          <v-text-field
            v-model="data[index].contact_num"
            :label="`*Contact Number of ${ isSpeechTherapist ? 'Speech Therapist' : 'caregiver / next-of-kin'}`"
            outlined
            :rules="[INPUT_VALIDATION.contact.valid]"
          />
        </v-col>
      </v-row>
      <v-row class="mt-3 px-12">
        <v-col cols="6" class="py-0 pl-6">
          <v-text-field
            v-model="data[index].email"
            :label="`${ isSpeechTherapist ? 'Email Address of Speech Therapist' : '*Email Address of  caregiver / next-of-kin'}`"
            outlined
            :rules="[INPUT_VALIDATION.email.valid]"
          />
        </v-col>
      </v-row>
      <v-row class="mt-3 px-12" v-if="!isSpeechTherapist">
        <v-col cols="12" class="py-0 px-6">
          <v-card class="card-input pa-6" outlined>
            <span class="input-label">What is your relationship with the PWA</span>
            <v-radio-group v-model="data[index].relationship">
              <v-radio v-for="r in RELATIONSHIP_OPTIONS" :key="r" :label="r" :value="r" />
              <div class="d-flex">
                <v-radio
                  key="others"
                  :value="othersValue[index]"
                  label="Others: "
                />
                <v-text-field
                  class="pl-3"
                  :disabled="!(data[index].relationship === 7 || data[index].relationship === othersValue[index]) || data[index].relationship === ''"
                  v-model="othersValue[index]"
                  v-on:input="data[index].relationship = othersValue[index]"
                />
              </div>
            </v-radio-group>
          </v-card>
        </v-col>
      </v-row>
    </div>

    <v-row class="mt-3" v-if="(data.length < 3 && !isSpeechTherapist) || (data.length < 1 && isSpeechTherapist)">
      <v-col cols="12" class="py-0 d-flex justify-center">
        <v-btn color="warning" class="my-3" @click="addNOK">Add {{ isSpeechTherapist ? 'Speech Therapist' : 'Caregiver' }}</v-btn>
      </v-col>
    </v-row>

  </div>
</template>
<script>
import { INPUT_VALIDATION } from './../../assets/data'

export default {
  props: {
    value: {
      type: Array,
      default () {
        return []
      }
    },
    readonly: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    isSpeechTherapist: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      data: this.value,
      INPUT_VALIDATION,
      RELATIONSHIP_OPTIONS: [
        'Spouse',
        'Parent',
        'Child',
        'Sibling',
        'Friend',
        'Domestic Helper',
        'Healthcare professional'
      ],
      othersValue: ['', '', '']
    }
  },

  methods: {
    addNOK () {
      if (this.data.length < 3) {
        this.data.push({
          contact_num: '',
          email: '',
          name: '',
          relationship: ''
        })
      }
    },
    removeNOK (removeIndex) {
      this.data = this.data.filter((item, index) => index !== removeIndex)
    }
  },

  watch: {
    data: {
      immediate: true,
      handler (newValue, oldValue) {
        this.$emit('input', newValue)
      }
    },
    value: {
      handler (newValue, oldValue) {
        this.data = this.value
      }
    }
  }
}
</script>
<style>
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
