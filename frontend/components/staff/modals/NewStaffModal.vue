<template>
  <v-dialog
    v-model="isOpen"
    width="700"
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
        <v-text-field
          v-model="staffData.fullname"
          :rules="fullnameRules"
          label="Fullname"
          required
        />
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
        { label: 'Core Team', value: 'coreteam' },
        { label: 'Intern', value: 'intern' },
        { label: 'Core Volunteer', value: 'corevolunteer' }
      ],
      staffData: {
        fullname: '',
        role: ''
      },
      fullnameRules: [
        v => !!v || 'E-mail is required'
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
