<template>
  <v-dialog
    v-model="isOpen"
    width="600"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        color="error"
        class="my-3 mr-3"
        v-bind="attrs"
        v-on="on"
        :loading="loading"
      >
        Archive
      </v-btn>
    </template>
    <v-card>
      <v-form ref="form" v-model="valid" @submit.prevent="triggerEdit">
        <v-card-title class="headline">
          Archive {{ resourceType.charAt(0).toUpperCase() + resourceType.substr(1, resourceType.length-2) }}
        </v-card-title>
        <v-divider />
        <div class="mt-4 pa-3">
          Archiving {{ resourceType.substr(0, resourceType.length - 1) }}: <span class="font-weight-bold">{{ resource.name }}</span>
          <div class="mt-4">
            <v-text-field
              v-model="archiveReason"
              label="Reason for archiving: "
            />
          </div>
        </div>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="error"
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
export default {
  name: 'ArchiveResourceDialog',

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
      archiveReason: ''
    }
  }
}
</script>

<style scoped>

</style>
