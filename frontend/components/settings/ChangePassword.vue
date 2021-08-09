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
      :rules="newPasswordRules"
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
      passwordRules: [v => !!v || 'Field Required'],
      newPasswordRules: [
        v => !!v || 'Field Required',
        v => (v && v.length > 8) || 'Password should be longer than 8 characters',
        v => /(?=.*[A-Z])/.test(v) || 'Password should have at least one uppercase letter',
        v => /(?=.*[a-z])/.test(v) || 'Password should have at least one lowercase letter',
        v => /(?=.*\d)/.test(v) || 'Password should have at least one digit',
        v => /(?=.*[-+_!@#$%^&*.,?])/.test(v) || 'Password should have at least one special character'
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
          'Content-Type': 'application/json',
          Authorization: accessToken
        }
        this.$axios
          .post(
            'https://api.apphasia.com/changepassword',
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
              error.response.data.message.charAt(0).toUpperCase() + error.response.data.message.slice(1),
              'error'
            ])
          })
          .then(() => {
            this.isSubmitting = false
            this.$refs.passwordform.reset()
          })
      }
    }
  },
  mounted () {
    // Set append icon to be non selectable via tab
    for (const button of document.querySelectorAll('[aria-label="append icon"]')) {
      button.setAttribute('tabindex', '-1')
    }
  }
}
</script>
