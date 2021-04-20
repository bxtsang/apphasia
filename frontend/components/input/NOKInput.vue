<template>
  <div>
    <div v-for="(nok, index) in data" :key="index">
      <v-row>
        <v-col cols="12" class="py-0 d-flex">
          <span class="font-weight-bold">({{ index + 1 }}) Caregiver Information</span>
          <v-spacer />
          <v-btn color="error" depressed fab small @click="() => { removeNOK(index) }"><v-icon>mdi-close</v-icon></v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" class="py-0">
          <v-text-field
            v-model="data[index].name"
            label="Name of Caregiver / NOK"
            :readonly="readonly"
            :disabled="disabled"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4" class="py-0">
          <v-text-field
            v-model="data[index].relationship"
            label="Relationship with PWA"
            :readonly="readonly"
            :disabled="disabled"
          />
        </v-col>
        <v-col cols="4" class="py-0">
          <v-text-field
            v-model="data[index].contact_num"
            label="*Contact Number"
            :readonly="readonly"
            :disabled="disabled"
            :rules="[INPUT_VALIDATION.contact.valid]"
          />
        </v-col>
        <v-col cols="4" class="py-0">
          <v-text-field
            v-model="data[index].email"
            label="*Email Address"
            :readonly="readonly"
            :disabled="disabled"
            :rules="[INPUT_VALIDATION.email.valid]"
          />
        </v-col>
      </v-row>
    </div>

    <v-row class="mt-3" v-if="data.length < 3">
      <v-col cols="12" class="py-0 d-flex justify-center">
        <v-btn color="primary" outlined class="my-3" @click="addNOK">Add Caregiver</v-btn>
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
    }
  },
  data () {
    return {
      data: this.value,
      INPUT_VALIDATION
    }
  },

  methods: {
    addNOK () {
      if (this.data.length < 4) {
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
