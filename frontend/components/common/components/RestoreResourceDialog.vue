<template>
  <v-dialog
    v-model="isOpen"
    width="600"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        color="success"
        class="my-3 mr-3"
        v-bind="attrs"
        v-on="on"
      >
        Restore
      </v-btn>
    </template>
    <v-card>
      <v-form ref="form" @submit.prevent="restoreResource">
        <v-card-title class="headline">
          Restore {{ resourceType.charAt(0).toUpperCase() + resourceType.substr(1, resourceType.length-2) }}
        </v-card-title>
        <v-divider />
        <div class="mt-4 pa-3">
          Restore {{ resourceType.substr(0, resourceType.length - 1) }}: <span class="font-weight-bold">{{ resource.name }}</span>?
        </div>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="success"
            type="submit"
            :loading="isSubmitting"
          >
            Confirm
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'UnarchiveResourceDialog',

  props: {
    resource: {
      type: Object,
      default: null
    },
    resourceType: {
      type: String,
      default: null
    }
  },

  data () {
    return {
      isOpen: false,
      isSubmitting: false
    }
  },

  methods: {
    restoreResource () {
      this.isSubmitting = true
      const mutation = require('./../../../graphql/staff/Archive.graphql')

      this.$apollo.mutate({
        mutation,
        variables: {
          id: this.resource.id,
          archive_reason: null,
          is_active: true
        },
        update: (store, { data: { id: resourceId } }) => {
          this.$apollo.vm.$apolloProvider.defaultClient.resetStore()
        }
      }).then((data) => {
        this.isSubmitting = false
        this.isOpen = false
        this.$store.commit('notification/newNotification', ['Staff successfully archived', 'success'])
      }).catch((error) => {
        this.isSubmitting = false
        this.$store.commit('notification/newNotification', [error.message, 'error'])
      })
    }
  }
}
</script>

<style scoped>

</style>
