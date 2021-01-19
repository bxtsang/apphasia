<template>
  <v-snackbar v-model="display" absolute :timeout="timeout">
    <v-icon :color="color" small class="mr-3">
      {{ icon }}
    </v-icon>
    {{ message }}
    <template v-slot:action="{ attrs }">
      <v-btn text :color="color" v-bind="attrs" @click="display = false">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>
<script>
export default {
  data () {
    return {
      display: false,
      message: '',
      status: '',
      timeout: 2500
    }
  },
  computed: {
    icon () {
      switch (this.status) {
        case 'success':
          return 'mdi-check-circle'
        case 'error':
          return 'mdi-alert-circle'
        default:
          return 'mdi-information'
      }
    },
    color () {
      switch (this.status) {
        case 'success':
          return 'success'
        case 'error':
          return 'error'
        default:
          return 'yellow'
      }
    }
  },
  created () {
    this.$store.watch(state => state.notification.message, () => {
      const msg = this.$store.state.notification.message
      const status = this.$store.state.notification.status
      if (msg !== '') {
        this.message = msg
        this.status = status
        this.display = true
        setTimeout(() => {
          this.display = false
          this.$store.commit('notification/newNotification', ['', ''])
        }, this.timeout)
      }
    })
  }
}
</script>
