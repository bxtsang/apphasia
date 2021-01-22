<template>
  <v-form ref="passwordform" v-model="passwordFormValid" class="mt-6 d-flex flex-column" @submit.prevent="changePassword">
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
    <v-btn color="primary" class="my-3 align-self-end" type="submit">
      Save
    </v-btn>
  </v-form>
</template>
<script>
export default {
  data () {
    return {
      passwordFormValid: true,
      showCurrentPassword: false,
      showNewPassword: false,
      password: {
        current: '',
        new: ''
      },
      passwordRules: [v => !!v || 'Field Required']
    }
  },
  methods: {
    changePassword () {
      if (this.$refs.passwordform.validate()) {
        const accessToken = localStorage.getItem(`auth.CognitoIdentityServiceProvider.${this.$auth.strategies.cognito.options.clientId}.${this.$auth.user.sub}.accessToken`)
        const postBody = {
          access_token: accessToken,
          proposed_password: this.password.new,
          previous_password: this.password.current
        }
        const postHeader = {
          'Content-Type': 'application/json'
        }
        this.$axios.post(
          'https://jqi5g2tgj2.execute-api.ap-southeast-1.amazonaws.com/dev',
          JSON.stringify(postBody),
          { postHeader }
        ).then((response) => {
          this.$store.commit('notification/newNotification', ['Password has been updated', 'success'])
        }).catch((error) => {
          console.log('error: ' + error.response.data.error)
          this.$store.commit('notification/newNotification', [error.response.data.message, 'error'])
        }).then(() => {
          this.$refs.passwordform.reset()
        })
      }
    }
  }
}
</script>
