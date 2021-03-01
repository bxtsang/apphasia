<template>
  <v-form
    ref="passwordform"
    v-model="passwordFormValid"
    class="mt-6 d-flex flex-column"
    @submit.prevent="changePassword"
  >
    <v-text-field
      v-model="password.current"
      :append-icon="showCurrentPassword ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="passwordRules"
      :type="showCurrentPassword ? 'text' : 'password'"
      label="Current Password"
      @click:append="showCurrentPassword = !showCurrentPassword"
    />
    <v-text-field
      v-model="password.new"
      :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="passwordRules"
      :type="showNewPassword ? 'text' : 'password'"
      label="New Password"
      @click:append="showNewPassword = !showNewPassword"
    />
    <v-btn
      color="primary"
      class="my-3 align-self-end"
      type="submit"
      :loading="isSubmitting"
    >
      Save
    </v-btn>
  </v-form>
</template>
<script>
export default {
  data () {
    return {
      isSubmitting: false,
      passwordFormValid: true,
      showCurrentPassword: false,
      showNewPassword: false,
      password: {
        current: '',
        new: ''
      },
      passwordRules: [
        v => !!v || 'Password is required',
        v => (v && v.length >= 8) || 'Password must have 8 or more characters',
        v => /(?=.*[A-Z])/.test(v) || 'Must have one uppercase character',
        v => /(?=.*[a-z])/.test(v) || 'Must have one lower character',
        v => /(?=.*\d)/.test(v) || 'Must have one number',
        v => /([!@$%])/.test(v) || 'Must have one special character [!@#$%]'
      ]
    }
  },
  methods: {
    changePassword () {
      if (this.$refs.passwordform.validate()) {
        this.isSubmitting = true
        const accessToken = localStorage.getItem(
          `auth.CognitoIdentityServiceProvider.${this.$auth.strategies.cognito.options.clientId}.${this.$auth.user.sub}.accessToken`
        )
        const postBody = {
          access_token: accessToken,
          proposed_password: this.password.new,
          previous_password: this.password.current
        }
        const postHeader = {
          'Content-Type': 'application/json'
        }
        this.$axios
          .post(
            'https://jqi5g2tgj2.execute-api.ap-southeast-1.amazonaws.com/dev',
            JSON.stringify(postBody),
            { postHeader }
          )
          .then((response) => {
            this.$store.commit('notification/newNotification', [
              'Password has been updated',
              'success'
            ])
          })
          .catch((error) => {
            console.log('error: ' + error.response.data.error)
            this.$store.commit('notification/newNotification', [
              error.response.data.message,
              'error'
            ])
          })
          .then(() => {
            this.isSubmitting = false
            this.$refs.passwordform.reset()
          })
      }
    }
  }
}
</script>
