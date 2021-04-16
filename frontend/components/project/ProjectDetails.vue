<template>
  <v-card>
    <v-row>

      <!-- left col -->
      <v-col lg="6" cols="12">
        <v-row class="d-flex align-center">
          <v-col>
            <span class="section-title">Project Details</span>
          </v-col>
          <v-col class="d-flex justify-end">
            <EditResourceModal
              v-if="editPermission"
              :resourceType="resourceType"
              :resource="project"
              :text="true"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-text-field
              :value="project.title"
              label="Project Name"
              readonly
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-textarea
              :value="project.description"
              label="Project Notes"
              readonly
              auto-grow
              rows="1"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <RegistrationAvailabilityInput
              resource-type="PWAs"
              :value="project.display_pwa_registration"
              readonly
            />
          </v-col>
          <v-col class="py-0">
            <RegistrationAvailabilityInput
              resource-type="Volunteers"
              :value="project.display_vol_registration"
              readonly
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <span class="section-title">People Involved</span>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-autocomplete
              label="Staff In-Charge"
              :value="project.owner.name"
              :items="[project.owner.name]"
              readonly
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-autocomplete
              label="Staff Involved"
              chips
              multiple
              :items="project.staffs"
              item-text="staff.name"
              item-value="staff.id"
              :value="project.staffs.map(item => item.staff.id)"
              readonly
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-autocomplete
              :value="VOLUNTEER_TYPES[project.voltypes]"
              label="Project Volunteer Types"
              :items="[VOLUNTEER_TYPES[project.voltypes]]"
              readonly
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-autocomplete
              label="Volunteers Involved"
              chips
              multiple
              :items="project.volunteers"
              item-text="volunteer.general_info.name"
              item-value="volunteer.general_info.id"
              :value="project.volunteers.map(item => item.volunteer.general_info.id)"
              readonly
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col class="py-0">
            <v-autocomplete
              label="PWAs Involved"
              chips
              multiple
              :items="project.pwas"
              item-text="pwa.general_info.name"
              item-value="pwa.general_info.id"
              :value="project.pwas.map(item => item.pwa.general_info.id)"
              readonly
            />
          </v-col>
        </v-row>
      </v-col>

      <!-- right col -->
      <v-col lg="6" cols="12">
        Task Component
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <ProjectAssignmentView :project="project" />
      </v-col>
    </v-row>
  </v-card>
</template>
<script>
import { EDIT_RESOURCE_PERMISSIONS, VOLUNTEER_TYPES } from './../../assets/data'

export default {
  props: {
    project: {
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
      VOLUNTEER_TYPES,
      EDIT_RESOURCE_PERMISSIONS
    }
  },
  computed: {
    editPermission () {
      return this.EDIT_RESOURCE_PERMISSIONS[this.resourceType].includes(this.$auth.user['custom:role'])
    }
  }
}
</script>
