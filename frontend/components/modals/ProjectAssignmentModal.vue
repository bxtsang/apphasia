<template>
  <v-dialog
    v-model="isOpen"
    width="500"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" v-bind="attrs" v-on="on">
        Add Assignment
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
              <v-select
                :items="ASSIGNMENT_TYPE_OPTIONS"
                v-model="assignmentData.role"
                label="Which type of volunteer to assign to"
              />
            </v-col>
          </v-row>
          <v-row v-if="assignmentData.role !== null">
            <v-col class="py-0">
              <v-autocomplete
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
                label="PWAs"
                :items="pwaItems"
                multiple
                chips
                item-text="name"
                item-value="id"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card>
  </v-dialog>
</template>
<script>

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
      isOpen: false,
      ASSIGNMENT_TYPE_OPTIONS: [
        { text: 'Staff', value: 'staff' },
        { text: 'Volunteer', value: 'volunteer' }
      ],
      assignmentData: {
        role: null,
        id: '',
        pwas: []
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
        return []
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
    }
  }
  // NEED TO WATCH FOR PWA AND VOLUNTEER CHANGES IN PROJECT DETAILS
}
</script>
