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
      email: '',
      password: '',
      showPassword: false
    }
  },
  methods: {
    login () {
      console.log('login')
    }
  }
}
</script>
<style scoped>

</style>
