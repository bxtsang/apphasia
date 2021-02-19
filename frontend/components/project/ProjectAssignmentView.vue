<template>
  <div>
    <v-row class="d-flex align-center px-0">
      <v-col>
        <span>Project Assignment</span>
      </v-col>
      <v-col class="d-flex justify-end">
        <ProjectAssignmentModal :project="project" />
      </v-col>
    </v-row>
    <v-row>
      <v-container class="ma-0 pb-0" fluid>
        <v-row>
          <v-text-field
            v-model="search"
            label="Search"
            append-icon="mdi-magnify"
            solo
            dense
            class="mx-3"

          />
        </v-row>
      </v-container>
    </v-row>
    <v-data-table
      :headers="headers"
      :items="assignmentItems"
      item-key="id"
      class="elevation-3"
      :search="search"
    >
      <template v-slot:[`item.role`]="{ item }">
        {{ item.role.charAt(0).toUpperCase() + item.role.slice(1)}}
      </template>

      <template v-slot:[`item.pwas`]="{ item }">
        <v-chip v-for="(pwa, index) in item.pwas.split(',')" :key="index" class="mr-1">
          {{ pwa }}
        </v-chip>
      </template>

      <template v-slot:[`item.actions`]="{ item }">
        <ProjectAssignmentModal :project="project" :assignment="item" />
        <v-btn icon v-on:click="() => deleteAssignment(item)" :loading="item.loading">
          <v-icon>
            mdi-delete
          </v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </div>
</template>
<script>
import DeleteVolProjectAssignment from './../../graphql/project/project_assignment/DeleteVolProjectAssignment.graphql'
import DeleteStaffProjectAssignment from './../../graphql/project/project_assignment/DeleteStaffProjectAssignment.graphql'

export default {
  props: {
    project: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      headers: [
        { text: 'Role', value: 'role' },
        { text: 'Name', value: 'name' },
        { text: 'PWA Assigned', value: 'pwas' },
        { text: 'Actions', value: 'actions', sortable: false, align: 'end' }
      ],
      search: ''
    }
  },
  computed: {
    assignmentItems () {
      const assignmentMapping = {}
      for (const staffAssignment of this.project.pwa_assigned_staffs) {
        if (assignmentMapping[`staff-${staffAssignment.staff.id}`]) {
          assignmentMapping[`staff-${staffAssignment.staff.id}`].pwas.push(staffAssignment.pwa.general_info.name)
          assignmentMapping[`staff-${staffAssignment.staff.id}`].pwas_id.push(staffAssignment.pwa.general_info.id)
        } else {
          assignmentMapping[`staff-${staffAssignment.staff.id}`] = {
            name: staffAssignment.staff.name,
            pwas: [staffAssignment.pwa.general_info.name],
            pwas_id: [staffAssignment.pwa.general_info.id]
          }
        }
      }
      for (const volAssignment of this.project.pwa_assigned_vols) {
        if (assignmentMapping[`volunteer-${volAssignment.volunteer.general_info.id}`]) {
          assignmentMapping[`volunteer-${volAssignment.volunteer.general_info.id}`].pwas.push(volAssignment.pwa.general_info.name)
          assignmentMapping[`volunteer-${volAssignment.volunteer.general_info.id}`].pwas_id.push(volAssignment.pwa.general_info.id)
        } else {
          assignmentMapping[`volunteer-${volAssignment.volunteer.general_info.id}`] = {
            name: volAssignment.volunteer.general_info.name,
            pwas: [volAssignment.pwa.general_info.name],
            pwas_id: [volAssignment.pwa.general_info.id]
          }
        }
      }
      const items = []
      for (const key in assignmentMapping) {
        const item = {
          id: key,
          role: key.split('-')[0],
          name: assignmentMapping[key].name,
          pwas: assignmentMapping[key].pwas.toString(),
          pwas_id: assignmentMapping[key].pwas_id,
          loading: false
        }
        items.push(item)
      }
      return items
    }
  },
  methods: {
    deleteAssignment (item) {
      item.loading = true
      const mutationQuery = item.role === 'staff' ? DeleteStaffProjectAssignment : DeleteVolProjectAssignment
      const variables = { project_id: this.project.id }
      variables[item.role === 'staff' ? 'staff_id' : 'vol_id'] = item.id.split('-')[1]
      console.log(variables)
      this.$apollo.mutate({
        mutation: mutationQuery,
        variables
      }).then((data) => {
        item.loading = false
        this.$store.commit('notification/newNotification', ['Project Assignment successfully removed', 'success'])
      }).catch((error) => {
        item.loading = false
        this.$store.commit('notification/newNotification', [error.message, 'error'])
      })
    }
  }
}
</script>
