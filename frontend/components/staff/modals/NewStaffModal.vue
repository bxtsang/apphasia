<template>
  <v-dialog
    v-model="isOpen"
    width="800"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" v-bind="attrs" v-on="on">
        Add Staff
      </v-btn>
    </template>
    <v-card class="pa-8">
      <span class="section-title">Add Staff</span>
      <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="submitProject">
        <v-subtitle>Role</v-subtitle>
        <v-radio-group v-model="staffData.role" row>
          <v-radio v-for="role in ROLE_OPTIONS" :key="role.value" :label="role.label" :value="role.value" />
        </v-radio-group>
        <v-subtitle>Personal Details</v-subtitle>
        <v-container class="px-0">
          <v-row>
            <v-col>
              <v-text-field
                v-model="staffData.fullname"
                :rules="fullnameRules"
                label="Full Name"
                required
              />
            </v-col>
            <v-col>
              <v-text-field
                v-model="staffData.nickname"
                :rules="nicknameRules"
                label="Nickname / Alias"
                required
              />
            </v-col>
            <v-col>
              <v-text-field
                v-model="staffData.nric"
                :rules="nricRules"
                label="NRIC"
                required
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <input type="date" />
            </v-col>
            <v-col>
              <v-text-field
                v-model="staffData.contact_number"
                :rules="contactRules"
                label="Contact"
                required
              />
            </v-col>
            <v-col>
              <v-text-field
                v-model="staffData.gender"
                :rules="nricRules"
                label="NRIC"
                required
              />
            </v-col>
          </v-row>
        </v-container>
        <v-btn color="primary" class="my-3" type="submit">
          Save
        </v-btn>
      </v-form>
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  data () {
    return {
      isOpen: false,
      valid: true,
      ROLE_OPTIONS: [
        { label: 'Core Team', value: 'core_team' },
        { label: 'Intern', value: 'intern' },
        { label: 'Core Volunteer', value: 'core_volunteer' }
      ],
      staffData: {
        role: '',
        fullname: '',
        nickname: '',
        nric: '',
        dob: '',
        contact_number: '',
        gender: '',
        email: '',
        home_address: ''
      },
      additionalData: {
        bio: '',
        languages: [],
        work_location: '',
        profession: '',
        isST: false,
        data_joined: '',
        supervisor: ''
      },
      fullnameRules: [v => !!v || 'Fullname is required'],
      nicknameRules: [v => !!v || 'Nickname is required'],
      nricRules: [
        v => !!v || 'NRIC is required',
        v => /^[STFG]\d{7}[A-Z]$/.test(v) || 'Not a valid NRIC'
      ]
    }
  },
  methods: {
    submitProject () {
      return this.$refs.form.validate()
    }
  }
}
</script>
