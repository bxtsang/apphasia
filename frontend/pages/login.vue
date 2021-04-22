<template>
  <div>
    <v-card class="pa-6">
      <v-img src="/asg.png" max-width="350" />
        <div v-if="!flipped">
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
            <p class="tiny-link primary--text" @click="flipped = !flipped">Forget Password</p>
          </v-form>
        </div>
        <div v-else>
          <div v-if="!codeSent">
            <v-subheader class="justify-center font-weight-bold">
              Forgot your password?
            </v-subheader>
            <v-form ref="formForgot" v-model="validForgot" @submit.prevent="forgotPassword">
              <v-text-field
                  v-model="emailForgot"
                  :rules="emailRules"
                  label="Email"
                  required
                  data-cy="cy-login-email-forgot-input"
                />
              <v-btn block color="primary" class="my-3" type="submit" :loading="isRequestingReset">Request for Reset</v-btn>
            </v-form>
            <p class="tiny-link primary--text" @click="flipped = !flipped">Return to Login</p>
          </div>
          <div v-else>
            <v-subheader class="justify-center font-weight-bold text-center" style="max-width:350px">
              A reset code has been sent to your email. Complete the password reset by keying in the reset code and your new password
            </v-subheader>
            <v-form ref="formReset" v-model="validReset" @submit.prevent="resetPassword">
              <v-text-field
                v-model="code"
                :rules="codeRules"
                label="Reset Code"
                required
              />
              <v-text-field
                v-model="newPassword"
                :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showNewPassword ? 'text' : 'password'"
                :rules="newPasswordRules"
                label="New Password"
                required
                @click:append="showNewPassword = !showNewPassword"
                data-cy="cy-login-new-password-input"
              />
              <v-btn block color="primary" class="my-3" type="submit" :loading="isResettingPassword">Reset Password</v-btn>
            </v-form>
          </div>
        </div>
    </v-card>
  </div>
</template>
<script>
export default {
  layout: 'none',
  data () {
    return {
      flipped: false,
      codeSent: false,
      isLoggingIn: false,
      isRequestingReset: false,
      isResettingPassword: false,
      valid: true,
      validForgot: true,
      validReset: true,
      code: '',
      codeRules: [v => !!v || 'Reset code required', v => !isNaN(v) || 'Only numbers allowed'],
      email: '',
      emailForgot: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
      ],
      password: '',
      passwordRules: [
        v => !!v || 'Password is required'
      ],
      newPassword: '',
      newPasswordRules: [
        v => !!v || 'Field Required',
        v => (v && v.length > 8) || 'Password should be longer than 8 characters',
        v => /(?=.*[A-Z])/.test(v) || 'Password should have at least one uppercase letter',
        v => /(?=.*[a-z])/.test(v) || 'Password should have at least one lowercase letter',
        v => /(?=.*\d)/.test(v) || 'Password should have at least one digit',
        v => /(?=.*[-+_!@#$%^&*.,?])/.test(v) || 'Password should have at least one special character'
      ],
      showPassword: false,
      showNewPassword: false
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
    },
    forgotPassword () {
      if (this.$refs.formForgot.validate()) {
        this.isRequestingReset = true
        const postBody = {
          email: this.emailForgot
        }
        const postHeader = {
          'Content-Type': 'application/json'
        }
        this.$axios
          .post(
            'https://api.apphasia.cf/resetpassword',
            JSON.stringify(postBody),
            { postHeader }
          )
          .then((response) => {
            console.log(response)
            this.codeSent = true
            this.$nextTick(() => {
              this.$refs.formReset.reset()
            })
          })
          .catch((error) => {
            console.log(error.response.data.message)
            this.$store.commit('notification/newNotification', [error.response.data.message, 'error'])
            this.emailForgot = ''
            this.$nextTick(() => {
              this.$refs.formForgot.reset()
            })
          })
          .then(() => {
            this.isRequestingReset = false
          })
      }
    },
    resetPassword () {
      if (this.$refs.formReset.validate()) {
        this.isResettingPassword = true
        const postBody = {
          email: this.emailForgot,
          password: this.newPassword,
          code: this.code
        }
        const postHeader = {
          'Content-Type': 'application/json'
        }
        this.$axios
          .post(
            'https://api.apphasia.cf/setpassword',
            JSON.stringify(postBody),
            { postHeader }
          )
          .then((response) => {
            this.code = ''
            this.newPassword = ''
            this.emailForgot = ''
            this.codeSent = false
            this.flipped = false
            this.$store.commit('notification/newNotification', [response.data.message, 'success'])
          })
          .catch((error) => {
            console.log(error.response.data.message)
            this.$store.commit('notification/newNotification', [error.response.data.message, 'error'])
            this.code = ''
            this.newPassword = ''
            this.$nextTick(() => {
              this.$refs.formReset.reset()
            })
          })
          .then(() => {
            this.isResettingPassword = false
          })
      }
    }
  }
}
</script>
<style scoped>
.tiny-link {
  font-size: 0.8rem;
  text-decoration: underline;
  cursor: pointer;
  text-align: center;
}
</style>
