<template>
  <v-dialog
    v-model="isOpen"
    width="500"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        color="error"
        v-bind="attrs"
        v-on="on"
      >
        Delete
      </v-btn>
    </template>
    <v-card>
      <v-card-title class="headline">
        Confirm delete?
      </v-card-title>
      <v-divider />
      <v-card-text class="mt-4">
        Deleting {{ resourceType }}: <span class="font-weight-bold">{{ identifier }}</span>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="error"
          :loading="isLoading"
          @click="deleteResource()"
        >
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import DeleteVol from './../../graphql/volunteer/DeleteVol.graphql'
import GetSingleVol from './../../graphql/volunteer/GetSingleVol.graphql'
import GetAllVol from './../../graphql/volunteer/GetAllVol.graphql'

export default {
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
      isLoading: false
    }
  },
  computed: {
    identifier () {
      if (this.resourceType === 'volunteer' || this.resourceType === 'pwa') {
        return this.resource.general_info.name
      }
      return null
    }
  },
  methods: {
    deleteResource () {
      this.isLoading = true
      this.$apollo.mutate({
        mutation: DeleteVol,
        variables: {
          id: this.resource.id
        },
        update: (store, { data: { delete_volunteers_by_pk: deletedVolunteer } }) => {
          store.writeQuery({
            query: GetSingleVol,
            data: { volunteers_by_pk: null },
            variables: { id: this.resource.id }
          })
          try {
            const allVol = store.readQuery({
              query: GetAllVol,
              variables: {}
            })
            allVol.volunteers = allVol.volunteers.filter(item => item.id !== this.resource.id)
            store.writeQuery(({
              query: GetAllVol,
              allVol,
              variables: {}
            }))
            console.log(store)
          } catch (error) {
          //  handle if GetAllVols query is not in store
          }
        }
      }).then((data) => {
        this.isLoading = false
        this.isOpen = false
        this.$emit('deleteSuccess')
        this.$store.commit('notification/newNotification', ['Volunteer successfully deleted', 'success'])
      }).catch((error) => {
        this.$store.commit('notification/newNotification', [error.message, 'error'])
      })
    }
  }
}
</script>

<style scoped>

</style>
