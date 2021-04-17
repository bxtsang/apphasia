<template>
  <div>
    <v-card elevation="2" outlined class="px-6 py-6 mb-6 text-center">
      <v-card-title class="justify-center">
        Verify your email address
      </v-card-title>
      <v-card-text>
        Click on send verification code to receive your code. Once it is
        verified you will be able to reset your password!
      </v-card-text>
      <v-card-text class="d-flex justify-center">
        <OtpInput
          input-classes="otp-input"
          :num-inputs="6"
          separator="-"
          :is-input-num="true"
          :should-auto-focus="true"
          @on-complete="handleOnComplete"
          @on-change="handleOnChange"
        />
      </v-card-text>
      <v-card-text>
        <v-btn elevation="2" rounded color="secondary" @click="sendCode">
          Send verification code
        </v-btn>
      </v-card-text>
      <v-btn
        v-if="completed"
        elevation="2"
        rounded
        color="primary"
        @click="verify"
      >
        Verify
      </v-btn>
    </v-card>
  </div>
</template>

<script>
import OtpInput from '@bachdgvn/vue-otp-input'
export default {
  components: {
    OtpInput
  },
  data () {
    return {
      accessToken: '',
      loading: false,
      email: '',
      code: '',
      completed: false,
      snackbar: false,
      text: '',
      color: '',
      timeout: 2000
    }
  },
  mounted () {
    const accessToken = localStorage.getItem(
      `auth.CognitoIdentityServiceProvider.${this.$auth.strategies.cognito.options.clientId}.${this.$auth.user.sub}.accessToken`
    )
    this.accessToken = accessToken
    const email = this.$store.$auth.$state.user.email
    this.email = email
  },
  methods: {
    async sendCode () {
      if (this.checkVerified()) {
        return
      }
      const postBody = {
        access_token: this.accessToken
      }
      const postHeader = {
        'Content-Type': 'application/json'
      }
      this.loading = true
      await this.$axios
        .post(
          'https://3swx2qnvu9.execute-api.ap-southeast-1.amazonaws.com/dev',
          JSON.stringify(postBody),
          { postHeader }
        )
        .then((resp) => {
          console.log(resp)
          if (resp.data.status === 'success') {
            this.codeSent()
          } else if (resp.data.status === 'failed') {
            this.reject()
          }
        })
        .catch((error) => {
          this.reject()
          console.log(error)
        })
      this.loading = false
    },
    async verify () {
      if (this.checkVerified()) {
        return
      }
      const postBody = {
        access_token: this.accessToken,
        code: this.code,
        email: this.email
      }
      const postHeader = {
        'Content-Type': 'application/json'
      }
      this.loading = true
      await this.$axios
        .post(
          'https://65vbyychn5.execute-api.ap-southeast-1.amazonaws.com/dev',
          JSON.stringify(postBody),
          { postHeader }
        )
        .then((resp) => {
          console.log(resp)
          if (resp.data.status === 'success') {
            this.$store.$auth.$state.user.email_verified = 'true'
            this.emailVerified()
            this.$router.push('/')
          } else if (resp.data.status === 'failed') {
            this.reject()
          }
        })
        .catch((error) => {
          this.reject()
          console.log(error)
        })
      this.loading = false
    },
    handleOnComplete (value) {
      this.completed = true
      this.code = value
      console.log('OTP: ', value)
    },
    handleOnChange (value) {
      this.completed = false
      console.log('OTP: ', value)
    },
    checkVerified () {
      if (this.$store.$auth.$state.user.email_verified === 'true') {
        this.$store.commit('notification/newNotification', [
          'Email already verified!',
          'success'
        ])
        return true
      }
      this.snackbar = false
      return false
    },
    codeSent () {
      this.$store.commit('notification/newNotification', [
        'Verification code sent to email',
        'success'
      ])
    },
    emailVerified () {
      this.$store.commit('notification/newNotification', [
        'Email successfully verified!',
        'success'
      ])
    },
    reject () {
      this.$store.commit('notification/newNotification', [
        'Email verification failed, please try again.',
        'error'
      ])
    }
  }
}
</script>
<style>
.otp-input {
  width: 40px;
  height: 40px;
  padding: 5px;
  margin: 0 10px;
  font-size: 20px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.3);
  text-align: center;
  font-family: 'Roboto', sans-serif;
}
.error {
  border: 1px solid red !important;
}
</style>
