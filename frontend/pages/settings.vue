<template>
  <div>
    <h1 class="title mb-3">
      Settings
    </h1>
    <v-card>
      <div class="d-flex">
        <div>
          <v-navigation-drawer permanent>
            <v-list class="pa-0" nav dense>
              <v-list-item
                v-for="(item, index) in items"
                :key="index"
                color="primary"
                :input-value="index == active"
                link
                class="py-2 px-6"
                @click="active = index"
              >
                <v-list-item-icon>
                  <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-navigation-drawer>
        </div>
        <div v-if="active === 0" class="px-8 py-6" style="width:100%;max-width:800px;">
          <h1 class="title mb-3">
            Edit Profile
          </h1>
        </div>
        <div v-else-if="active === 1" class="px-8 py-6" style="width:100%;max-width:500px;">
          <h1 class="title mb-3">
            Change Password
          </h1>
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
        </div>
      </div>
    </v-card>
  </div>
</template>
<script>
export default {
  data () {
    return {
      active: 0,
      items: [
        {
          icon: 'mdi-pencil',
          title: 'Edit Profile'
        },
        {
          icon: 'mdi-shield-check',
          title: 'Change Password'
        }
      ],
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
