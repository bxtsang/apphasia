<template>
  <div>
    <v-card class="pa-6">
      <v-img src="/asg.png" max-width="350" />
      <v-subheader class="justify-center font-weight-bold">
        Welcome Back!
      </v-subheader>
      <v-form ref="form" v-model="valid">
        <v-text-field
          v-model="email"
          :rules="emailRules"
          label="Email"
          required
        />
        <v-text-field
          v-model="password"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPassword ? 'text' : 'password'"
          :rules="passwordRules"
          label="Password"
          required
          @click:append="showPassword = !showPassword"
        />
        <v-btn block color="primary" class="my-3" @click="login">
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
  methods: {
    async login () {
      if (this.email === '' || this.password === '') { return }

      const loginData = { email: this.email, password: this.password }
      try {
        await this.$auth.loginWith('local', { data: loginData })
      } catch (error) {
        // console.log(error.message);
        // this.$store.commit('notification/newNotification', ["Login Error", "error"]);
      } finally {
        this.email = ''
        this.password = ''
      }
    }
  }
}
</script>
<style scoped>

</style>
