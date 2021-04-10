<template>
  <v-dialog
    v-model="isOpen"
    width="800"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" v-bind="attrs" v-on="on" data-cy="cy-add-resource-btn">
        Add {{ resource }}
      </v-btn>
    </template>
    <StaffForm v-if="resourceType === 'staffs'" @closeForm="isOpen = false" />
    <PWAForm v-if="resourceType === 'pwas'" @closeForm="isOpen = false" />
    <VolunteerForm v-if="resourceType === 'volunteers'" @closeForm="isOpen = false" />
    <ProjectForm v-if="resourceType === 'projects'" @closeForm="isOpen = false" />
    <EventForm v-if="resourceType === 'events'" @closeForm="isOpen = false" />
  </v-dialog>
</template>
<script>
import StaffForm from './../staff/StaffForm'
import PWAForm from './../pwa/PWAForm'
import ProjectForm from './../project/ProjectForm'
import VolunteerForm from './../volunteer/VolunteerForm'

export default {
  components: { StaffForm, PWAForm, ProjectForm, VolunteerForm },
  props: {
    text: Boolean,
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
    resource () {
      if (this.resourceType === 'staffs') {
        return 'Staff'
      }
      if (this.resourceType === 'pwas') {
        return 'PWA'
      }
      if (this.resourceType === 'projects') {
        return 'Project'
      }
      if (this.resourceType === 'events') {
        return 'Event'
      }
      if (this.resourceType === 'volunteers') {
        return 'Volunteer'
      }
      return 'Resource'
    }
  }
}
</script>
