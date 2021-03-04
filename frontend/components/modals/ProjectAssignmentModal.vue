<template>
  <v-dialog
    v-model="isOpen"
    width="500"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn v-if="!assignment" color="primary" v-bind="attrs" v-on="on">
        Add Assignment
      </v-btn>
      <v-btn v-else icon v-bind="attrs" v-on="on">
        <v-icon>
          mdi-pencil
        </v-icon>
      </v-btn>
    </template>
    <v-card class="pa-8">
      <v-form ref="form" v-model="valid" class="mt-6" @submit.prevent="formSubmitMethod">
        <v-container class="pa-0">
          <v-row>
            <v-col class="py-0">
              <span v-if="assignment" class="section-title">Edit Assignment</span>
              <span v-else class="section-title">Add Assignment</span>
            </v-col>
          </v-row>
          <v-row>
            <v-col class="py-0">
              <v-radio-group v-model="assignmentData.role" row>
                <v-radio
                  v-for="item in ASSIGNMENT_TYPE_OPTIONS"
                  :key="item.value"
                  :value="item.value"
                  :label="item.text"
                />
              </v-radio-group>
            </v-col>
          </v-row>
          <v-row v-if="assignmentData.role !== null">
            <v-col class="py-0">
              <v-autocomplete
                v-model="assignmentData.id"
                :label="vonlunteerLabel"
                :items="vonlunteerItems"
                item-text="name"
                item-value="id"
              />
            </v-col>
          </v-row>
          <v-row v-if="assignmentData.role !== null">
            <v-col class="py-0">
              <v-autocomplete
                v-model="assignmentData.pwas"
                label="PWAs"
                :items="pwaItems"
                multiple
                chips
                item-text="name"
                item-value="id"
              />
            </v-col>
          </v-row>
          <v-row v-if="assignmentData.id !== -1 && assignmentData.pwas.length > 0">
            <v-spacer/>
            <v-btn color="primary" class="my-3 mr-3" type="submit" :loading="isSubmitting">
              {{ assignment ? 'Edit' : 'Save' }}
            </v-btn>
            </v-row>
        </v-container>
      </v-form>
    </v-card>
  </v-dialog>
</template>
<script>
import CreateAndUpdateVolProjectAssignment from './../../graphql/project/project_assignment/CreateAndUpdateVolProjectAssignment.graphql'
import CreateAndUpdateStaffProjectAssignment from './../../graphql/project/project_assignment/CreateAndUpdateStaffProjectAssignment.graphql'

export default {
  props: {
    assignment: {
      type: Object,
      default: null
    },
    project: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      valid: true,
      isSubmitting: false,
      isOpen: false,
      ASSIGNMENT_TYPE_OPTIONS: [
        { text: 'Staff', value: 'staff' },
        { text: 'Volunteer', value: 'volunteer' }
      ],
      assignmentData: {
        role: this.assignment ? this.assignment.role : null,
        id: this.assignment ? Number(this.assignment.id.split('-')[1]) : -1,
        pwas: this.assignment ? this.assignment.pwas_id : []
      }
    }
  },
  methods: {
    CreateAndUpdateAssignment (update) {
      if (this.$refs.form.validate()) {
        this.isSubmitting = true
        const newAssignmentData = []
        for (const pwa of this.assignmentData.pwas) {
          const assignment = {
            project_id: this.project.id,
            pwa_id: pwa
          }
          assignment[this.assignmentData.role === 'staff' ? 'staff_id' : 'vol_id'] = this.assignmentData.id
          newAssignmentData.push(assignment)
        }
        const variables = {
          assignments: newAssignmentData,
          project_id: this.project.id
        }
        variables[this.assignmentData.role === 'staff' ? 'staff_id' : 'vol_id'] = this.assignmentData.id
        console.log(variables)
        const mutationQuery = this.assignmentData.role === 'staff' ? CreateAndUpdateStaffProjectAssignment : CreateAndUpdateVolProjectAssignment
        this.$apollo.mutate({
          mutation: mutationQuery,
          variables
        }).then((data) => {
          this.isSubmitting = false
          if (!update) {
            this.assignmentData = {
              role: null,
              id: -1,
              pwas: []
            }
          }
          this.isOpen = false
          this.$store.commit('notification/newNotification', [`Project Assignment successfully ${update ? 'updated' : 'created'}`, 'success'])
        }).catch((error) => {
          this.isSubmitting = false
          this.$store.commit('notification/newNotification', [error.message, 'error'])
        })
      }
    }
  },
  computed: {
    vonlunteerLabel () {
      if (this.assignmentData.role === 'staff') {
        return 'Staff'
      }
      if (this.assignmentData.role === 'volunteer') {
        return 'Volunteer'
      }
      return ''
    },
    vonlunteerItems () {
      if (this.assignmentData.role === 'staff') {
        return this.project.staffs.map((item) => {
          return {
            id: item.staff.id,
            name: item.staff.name
          }
        })
      }
      if (this.assignmentData.role === 'volunteer') {
        return this.project.volunteers.map((item) => {
          return {
            id: item.volunteer.general_info.id,
            name: item.volunteer.general_info.name
          }
        })
      }
      return []
    },
    pwaItems () {
      return this.project.pwas.map((item) => {
        return {
          id: item.pwa.general_info.id,
          name: item.pwa.general_info.name
        }
      })
    },
    formSubmitMethod () {
      if (this.assignment) {
        return () => this.CreateAndUpdateAssignment(true)
      } else {
        return () => this.CreateAndUpdateAssignment(false)
      }
    }
  }
}
</script>
