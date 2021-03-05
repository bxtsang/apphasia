<template>
  <div>
    <v-card class="pa-6">
      <v-img src="/asg.png" max-width="350" />
      <v-subheader class="justify-center font-weight-bold">
        Welcome Back!
      </v-subheader>
      <v-form ref="form" v-model="valid" @submit.prevent="login">
        <v-text-field
          v-model="email"
          :rules="emailRules"
          label="Email"
          required
          data-cy="cy-login-email-input"
        />
        <v-text-field
          v-model="password"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          :rules="passwordRules"
          label="Password"
          required
          @click:append="showPassword = !showPassword"
          data-cy="cy-login-password-input"
        />
        <v-btn
          block
          color="primary"
          class="my-3"
          type="submit"
          :loading="isLoggingIn"
          data-cy="cy-login-submit-input">
          Login
        </v-btn>
      </v-form>
    </v-card>
  </div>
</template>
<script>
export default {
  layout: 'none',
  data () {
    return {
      isLoggingIn: false,
      valid: true,
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
      ],
      password: '',
      passwordRules: [
        v => !!v || 'Password is required'
      ],
      showPassword: false
    }
  },
  mounted () {
    const tokenExpiry = localStorage.getItem('token_expiry') ? new Date(Number(localStorage.getItem('token_expiry'))) : null

    if (tokenExpiry != null && tokenExpiry <= new Date()) {
      localStorage.removeItem('token_expiry')
      this.$store.commit('notification/newNotification', ['Token has expired. Please login again', 'error'])
    }
  },
  methods: {
    async login () {
      if (this.$refs.form.validate()) {
        this.isLoggingIn = true
        const loginData = { username: this.email, password: this.password }
        try {
          const response = await this.$auth.loginWith('cognito', { data: loginData })
          this.$store.commit('email_verified/updateVerification', response.idToken.payload.email_verified)
          this.$apolloHelpers.onLogin(response.idToken.jwtToken)
          localStorage.setItem('token_expiry', response.idToken.payload.exp * 1000)
        } catch (error) {
          this.$store.commit('notification/newNotification', [error.message, 'error'])
          this.email = ''
          this.password = ''
          this.$apolloHelpers.onLogout()
        } finally {
          this.isLoggingIn = false
        }
      }
    }
  }
}
</script>
<style scoped>

</style>
