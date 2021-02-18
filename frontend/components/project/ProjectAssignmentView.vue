<template>
  <div>
    <v-row class="d-flex align-center px-0">
      <v-col>
        <span>Project Assignment</span>
      </v-col>
      <v-col class="d-flex justify-end">
        <v-btn color="primary">Add Assignment</v-btn>
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
      class="elevation-1"
      :search="search"
    >
      <template v-slot:[`item.role`]="{ item }">
        {{ item.role.charAt(0).toUpperCase() + item.role.slice(1)}}
      </template>

      <template v-slot:[`item.pwas`]="{ item }">
        <v-chip v-for="(pwa, index) in item.pwas.split(',')" :key="index">
          {{ pwa }}
        </v-chip>
      </template>

      <template v-slot:[`item.actions`]="{ item }">
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn
        color="primary"
        @click="initialize"
      >
        Reset
      </v-btn>
    </template>
    </v-data-table>
  </div>
</template>
<script>
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
        } else {
          assignmentMapping[`staff-${staffAssignment.staff.id}`] = {
            name: staffAssignment.staff.name,
            pwas: [staffAssignment.pwa.general_info.name]
          }
        }
      }
      for (const volAssignment of this.project.pwa_assigned_vols) {
        if (assignmentMapping[`volunteer-${volAssignment.volunteer.general_info.id}`]) {
          assignmentMapping[`volunteer-${volAssignment.volunteer.general_info.id}`].pwas.push(volAssignment.pwa.general_info.name)
        } else {
          assignmentMapping[`volunteer-${volAssignment.volunteer.general_info.id}`] = {
            name: volAssignment.volunteer.general_info.name,
            pwas: [volAssignment.pwa.general_info.name]
          }
        }
      }
      console.log(assignmentMapping)
      const items = []
      for (const key in assignmentMapping) {
        const item = {
          id: key,
          role: key.split('-')[0],
          name: assignmentMapping[key].name,
          pwas: assignmentMapping[key].pwas.toString()
        }
        items.push(item)
      }
      return items
    }
  }
}
</script>
