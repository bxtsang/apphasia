<template>
  <v-card elevation="2" outlined class="px-6 py-6 mb-6 text-center">
    <v-card-title class="justify-center">
      Verify your email address
    </v-card-title>
    <v-card-text>
      Click on send verification code to receive your code. Once it is verified you will be able to receive notifications!
    </v-card-text>
    <v-card-text>
      <CodeInput :loading="loading" class="input" @change="onChange" @complete="onComplete" />
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
      loading: false
    }
  },
  mounted () {
    const accessToken = localStorage.getItem(`auth.CognitoIdentityServiceProvider.${this.$auth.strategies.cognito.options.clientId}.${this.$auth.user.sub}.accessToken`)
    this.accessToken = accessToken
  },
  methods: {
    async sendCode () {
      //   console.log(this.$store.state.email_verified.isVerified)
      const postBody = {
        access_token: this.accessToken
      }
      const postHeader = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
      //   this.$axios.post('https://4ygth88tu2.execute-api.ap-southeast-1.amazonaws.com/dev', {
      //     body: postBody
      //   }, {
      //     headers: {
      //       'Access-Control-Allow-Origin': '*'
      //     }
      //   })
      //     .then(response => () => { console.log(response) })
      //     .catch(e => () => {
      //     // this.errors.push(e)
      //       console.log(e)
      //     })
      try {
        const resp = await this.$axios.post('https://4ygth88tu2.execute-api.ap-southeast-1.amazonaws.com/dev', postBody, { postHeader })
        console.log(resp)
      } catch (e) {
        console.log(e)
      }
    },
    verify () {
      const body = {
        access_token: this.accessToken,
        code: this.code
      }
      console.log(body)
    },
    onChange (v) {
      console.log('onChange ', v)
    },
    onComplete (v) {
      console.log('onComplete ', v)
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
