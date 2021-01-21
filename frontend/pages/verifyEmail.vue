<template>
  <v-card elevation="2" outlined class="px-6 py-6 mb-6 text-center">
    <v-card-title class="justify-center">
      Verify your email address
    </v-card-title>
    <v-card-text>
      Click on send verification code to receive your code. Once it is verified you will be able to receive notifications!
    </v-card-text>
    <v-card-text>
      <CodeInput v-model="code" :loading="loading" class="input" @change="onChange" @complete="onComplete" />
    </v-card-text>
    <v-card-text>
      <v-btn elevation="2" rounded color="secondary" @click="sendCode">
        Send verification code
      </v-btn>
      <v-btn elevation="2" rounded color="primary" @click="verify">
        Verify
      </v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
import CodeInput from 'vue-verification-code-input'
export default {
  components: {
    CodeInput
  },
  data () {
    return {
      accessToken: '',
      loading: false,
      email: '',
      code: '',
      completed: false
    }
  },
  mounted () {
    const accessToken = localStorage.getItem(`auth.CognitoIdentityServiceProvider.${this.$auth.strategies.cognito.options.clientId}.${this.$auth.user.sub}.accessToken`)
    this.accessToken = accessToken
    const email = this.$store.$auth.$state.user.email
    this.email = email
  },
  methods: {
    async sendCode () {
      const postBody = {
        access_token: this.accessToken
      }
      const postHeader = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
      try {
        const resp = await this.$axios.post('https://4ygth88tu2.execute-api.ap-southeast-1.amazonaws.com/dev', JSON.stringify(postBody), { postHeader })
        console.log(resp)
      } catch (e) {
        console.log(e)
      }
    },
    async verify () {
      if (!this.completed) {
        console.log('incomplete code')
        return
      }
      const postBody = {
        access_token: this.accessToken,
        code: this.code,
        email: this.email
      }
      const postHeader = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
      try {
        this.loading = true
        const resp = await this.$axios.post('https://65vbyychn5.execute-api.ap-southeast-1.amazonaws.com/dev', JSON.stringify(postBody), { postHeader })
        console.log(resp)
      } catch (e) {
        console.log(e)
      }
      this.loading = false
    },
    onChange (v) {
      this.completed = false
    },
    onComplete (v) {
      this.completed = true
      this.code = v
    }
  }
}
</script>
<style>
  .input {
    justify-content: center;
    text-align: center;
  }
</style>
