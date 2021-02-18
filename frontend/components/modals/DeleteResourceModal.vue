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
        Deleting {{ resourceType.substr(0, resourceType.length - 1) }}: <span class="font-weight-bold">{{ identifier }}</span>
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
import DeletePWA from './../../graphql/pwa/DeletePWA.graphql'
import GetSinglePWA from './../../graphql/pwa/GetSinglePWA.graphql'
import GetAllPWA from './../../graphql/pwa/GetAllPWA.graphql'
import DeleteProject from './../../graphql/project/DeleteProject.graphql'
import GetSingleProject from './../../graphql/project/GetSingleProject.graphql'
import GetAllProject from './../../graphql/project/GetAllProject.graphql'

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
      if (this.resourceType === 'volunteers' || this.resourceType === 'pwas') {
        return this.resource.general_info.name
      }
      if (this.resourceType === 'projects') {
        return this.resource.title
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
      this.isLoading = true
      this.$apollo.mutate({
        mutation: this.deleteMutation,
        variables: {
          id: this.resource.id
        },
        update: (store, { data: obj }) => {
          this.updateCache(store)
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
