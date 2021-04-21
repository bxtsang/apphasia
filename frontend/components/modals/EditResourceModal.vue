<template>
  <v-dialog
    v-model="isOpen"
    :width="800"
    persistent
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        v-if="text"
        color="primary"
        v-bind="attrs"
        v-on="on"
        data-cy="cy-edit-button"
      >
        <v-icon left>
          mdi-pencil
        </v-icon>
        Edit
      </v-btn>
      <v-btn
        v-else
        icon
        v-bind="attrs"
        v-on="on"
      >
        <v-icon>
          mdi-pencil
        </v-icon>
      </v-btn>
    </template>
    <StaffForm v-if="resourceType === 'staffs'" :staff="resource" v-on:closeForm="isOpen = false" />
    <VolunteerForm v-if="resourceType === 'volunteers'" :volunteer="resource" v-on:closeForm="isOpen = false" />
    <PWAForm v-if="resourceType === 'pwas'" :pwa="resource" v-on:closeForm="isOpen = false" />
    <ProjectForm v-if="resourceType === 'projects'" :project="resource" @closeForm="isOpen = false" />
    <EventForm v-if="resourceType === 'events'" :event="resource" @closeForm="isOpen = false" />
  </v-dialog>
</template>
<script>
import StaffForm from './../staff/StaffForm'
import VolunteerForm from './../volunteer/VolunteerForm'
import PWAForm from './../pwa/PWAForm'
import ProjectForm from './../project/ProjectForm'

export default {
  components: { StaffForm, VolunteerForm, PWAForm, ProjectForm },
  props: {
    text: Boolean,
    resource: {
      default: null,
      type: Object
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
  }
}
</script>
