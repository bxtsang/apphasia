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
      <v-card-title class="headline secondary white--text">
        Confirm delete?
      </v-card-title>

      <v-card-text class="mt-4">
        Deleting {{ resourceType }}: <span class="font-weight-bold">{{ identifier }}</span>
      </v-card-text>

      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="error"
          @click="deleteResource"
        >
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
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
      isOpen: false
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
    //  to Implement
    }
  }
}
</script>

<style scoped>

</style>
