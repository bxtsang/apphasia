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
      <v-form ref="form" v-model="valid" @submit.prevent="deleteResource">
      <v-card-title class="headline">
        Confirm delete?
      </v-card-title>
      <v-divider />
      <div class="mt-4 pa-3">
        Deleting {{ resourceType.substr(0, resourceType.length - 1) }}: <span class="font-weight-bold">{{ identifier }}</span>
        <div class="mt-4" v-if="resourceType === 'events' && resource.recurring !== null">
          <v-radio-group v-model="eventOption" class="mt-0">
            <v-radio
              v-for="option in DELETE_OPTIONS"
              :key="option.value"
              :label="option.text"
              :value="option.value"
            />
          </v-radio-group>
        </div>
      </div>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="error"
          :loading="isLoading"
          type="submit"
        >
          Confirm
        </v-btn>
      </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script>
import DeleteVol from './../../graphql/volunteer/DeleteVol.graphql'
import GetSingleVol from './../../graphql/volunteer/GetSingleVol.graphql'
import GetAllVol from './../../graphql/volunteer/GetAllVol.graphql'
import DeletePWA from './../../graphql/pwa/DeletePWA.graphql'
import GetSinglePWA from './../../graphql/pwa/GetSinglePWA.graphql'
import GetAllPWA from './../../graphql/pwa/GetAllPWA.graphql'
import DeleteProject from './../../graphql/project/DeleteProject.graphql'
import GetSingleProject from './../../graphql/project/GetSingleProject.graphql'
import GetAllProject from './../../graphql/project/GetAllProject.graphql'
import DeleteEvents from './../../graphql/event/DeleteEvents.graphql'

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
      isLoading: false,
      eventOption: 0,
      valid: true,
      DELETE_OPTIONS: [
        { text: 'This event', value: 0 },
        { text: 'This and future recurring events', value: 1 },
        { text: 'All recurring events', value: 2 }
      ]
    }
  },
  computed: {
    identifier () {
      if (this.resourceType === 'volunteers' || this.resourceType === 'pwas') {
        return this.resource.general_info.name
      }
      if (this.resourceType === 'projects') {
        return this.resource.title
      }
      if (this.resourceType === 'events') {
        return this.resource.name
      }
      return null
    },
    deleteMutation () {
      if (this.resourceType === 'volunteers') {
        return DeleteVol
      } else if (this.resourceType === 'pwas') {
        return DeletePWA
      } else if (this.resourceType === 'projects') {
        return DeleteProject
      } else if (this.resourceType === 'events') {
        return DeleteEvents
      }
      return null
    },
    getSingleMutation () {
      if (this.resourceType === 'volunteers') {
        return GetSingleVol
      } else if (this.resourceType === 'pwas') {
        return GetSinglePWA
      } else if (this.resourceType === 'projects') {
        return GetSingleProject
      }
      return null
    },
    getAllMutation () {
      if (this.resourceType === 'volunteers') {
        return GetAllVol
      } else if (this.resourceType === 'pwas') {
        return GetAllPWA
      } else if (this.resourceType === 'projects') {
        return GetAllProject
      }
      return null
    }
  },
  methods: {
    deleteResource () {
      if (this.$refs.form.validate()) {
        this.isLoading = true
        let variables = {
          id: this.resource.id
        }
        if (this.resourceType === 'events') {
          switch (this.eventOption) {
            case 1:
              variables = {
                eventData: {
                  recurrence_id: this.resource.recurring.id,
                  date: this.resource.date,
                  event_id: null
                }
              }
              break
            case 2:
              variables = {
                eventData: {
                  recurrence_id: this.resource.recurring.id,
                  date: null,
                  event_id: null
                }
              }
              break
            default:
              variables = {
                eventData: {
                  event_id: this.resource.id,
                  recurrence_id: null,
                  date: null
                }
              }
          }
        }
        this.$apollo.mutate({
          mutation: this.deleteMutation,
          variables,
          update: (store, data) => {
            // this.updateCache(store)
            this.$apollo.vm.$apolloProvider.defaultClient.resetStore()
          }
        }).then((data) => {
          this.isLoading = false
          this.isOpen = false
          this.$emit('deleteSuccess')
          const displayResourceName = this.resourceType.charAt(0).toUpperCase() + this.resourceType.slice(1)
          this.$store.commit('notification/newNotification', [`${displayResourceName.slice(0, -1)} successfully deleted`, 'success'])
        }).catch((error) => {
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    },
    updateCache (store) {
      const singleResourceData = {}
      if (this.resourceType === 'volunteers') {
        singleResourceData.volunteers_by_pk = null
      } else if (this.resourceType === 'pwas') {
        singleResourceData.pwas_by_pk = null
      } else if (this.resourceType === 'projects') {
        singleResourceData.projects_by_pk = null
      }

      store.writeQuery({
        query: this.getSingleMutation,
        data: singleResourceData,
        variables: { id: this.resource.id }
      })
      try {
        const allResource = store.readQuery({
          query: this.getAllMutation,
          variables: {}
        })
        allResource[this.resourceType] = allResource[this.resourceType].filter(item => item.id !== this.resource.id)
        store.writeQuery(({
          query: this.getAllMutation,
          allResource,
          variables: {}
        }))
      } catch (error) {
        //  handle if GetAllVols query is not in store
      }
    }
  }
}
</script>
